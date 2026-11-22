"""Deployer module."""

from __future__ import annotations

import hashlib
import io
import logging
import posixpath
import stat
from pathlib import Path, PurePosixPath
from types import TracebackType

import paramiko
from paramiko.hostkeys import HostKeyEntry, InvalidHostKey

from modules.settings import DeployerSettings

logger = logging.getLogger(__name__)

KEY_CLASSES: tuple[type[paramiko.PKey], ...] = (
    paramiko.Ed25519Key,
    paramiko.ECDSAKey,
    paramiko.RSAKey,
)


class Deployer:
    """Uploads a local folder to the remote server via SFTP.

    Use it as a context manager, so the connection is always closed:

        with Deployer(settings) as d:
            d.deploy(local_path)
    """

    _client: paramiko.SSHClient
    _sftp: paramiko.SFTPClient

    def __init__(self, settings: DeployerSettings) -> None:
        """Create a new Deployer instance.

        Args:
            settings (DeployerSettings): deployer settings.
        """
        self._settings = settings

    def __enter__(self) -> Deployer:
        """Connect to the remote server.

        Returns:
            Deployer: the connected deployer.
        """
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Disconnect from the remote server."""
        self.disconnect()

    def _load_key(self) -> paramiko.PKey | None:
        """Load the private key from its text content, if provided.

        Returns:
            paramiko.PKey | None: the key, or None if no content is set.

        Raises:
            ValueError: if the key cannot be parsed.
        """
        content = self._settings.private_key
        if not content:
            return None

        passphrase = self._settings.private_key_passphrase or None
        errors: list[str] = []
        for key_class in KEY_CLASSES:
            try:
                return key_class.from_private_key(io.StringIO(content), passphrase)
            except paramiko.PasswordRequiredException as e:
                raise ValueError(
                    "The private_key is encrypted: set the passphrase"
                ) from e
            except paramiko.SSHException as e:
                errors.append(f"{key_class.__name__}: {e}")
        raise ValueError(
            "Cannot parse private_key (wrong passphrase or unsupported key?): "
            + "; ".join(errors)
        )

    def connect(self) -> None:
        """Connect to the remote server.

        If `server_public_key` is set, the server must present that key;
        otherwise any key is accepted (and a warning is logged).

        Raises:
            ValueError: if `server_public_key` cannot be parsed.
        """
        hostname = self._settings.hostname
        logger.info("Connecting to %s...", hostname)
        self._client = paramiko.SSHClient()

        if server_key := self._settings.server_public_key:
            error = (
                "Cannot parse server_public_key: it must be the server's public "
                'key, e.g. "ssh-ed25519 AAAA..." as printed by ssh-keyscan'
            )
            try:
                entry = HostKeyEntry.from_line(f"{hostname} {server_key}")
            except InvalidHostKey as e:
                raise ValueError(error) from e
            if entry is None or entry.key is None:
                raise ValueError(error)
            self._client.get_host_keys().add(hostname, entry.key.get_name(), entry.key)
            self._client.set_missing_host_key_policy(paramiko.RejectPolicy())
        else:
            logger.warning(
                "No server_public_key set: the server identity will NOT be verified."
            )
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        key_path = self._settings.private_key_path
        self._client.connect(
            hostname=hostname,
            username=self._settings.username or None,
            pkey=self._load_key(),
            key_filename=key_path and str(key_path),
            passphrase=self._settings.private_key_passphrase or None,
            allow_agent=False,
            look_for_keys=False,
        )
        self._sftp = self._client.open_sftp()
        logger.info("Connected.")

    def check(self) -> None:
        """Check that the remote path is reachable on the connected server.

        Raises:
            ValueError: if the remote path is not a folder.
        """
        remote_path = self._settings.remote_path or "."
        if not stat.S_ISDIR(self._sftp.stat(remote_path).st_mode or 0):
            raise ValueError(f"Remote path {remote_path} is not a folder")
        logger.info("SSH key OK, remote path %s is reachable", remote_path)

    def disconnect(self) -> None:
        """Disconnect from the remote server."""
        if hasattr(self, "_sftp"):
            self._sftp.close()
        if hasattr(self, "_client"):
            self._client.close()

    def deploy(self, local_path: Path) -> None:
        """Upload the content of a local folder to the remote path.

        Remote files that do not exist locally are left untouched, except
        inside the folders listed in `prune_paths`, which are pruned after
        the upload.

        Args:
            local_path (Path): local folder to deploy.

        Raises:
            ValueError: if the folder does not look like a complete build, since
                pruning it would delete live files.
        """
        for required in ("index.html", "blog/index.html"):
            if not (local_path / required).is_file():
                raise ValueError(
                    f"Refusing to deploy {local_path}: {required} is missing "
                    "(run a full build first)"
                )

        for path in sorted(local_path.rglob("*")):
            relative = path.relative_to(local_path).as_posix()
            remote_path = posixpath.join(self._settings.remote_path, relative)

            if path.is_dir():
                self.create_folder(remote_path)
            else:
                self.upload_file(path, remote_path)

        for folder in self._settings.prune_paths:
            self.prune(local_path, folder)

    def prune(self, local_path: Path, folder: str) -> None:
        """Delete the remote files in a folder that do not exist locally.

        Args:
            local_path (Path): local folder that was deployed.
            folder (str): folder to prune, relative to both `local_path` and
                the remote path.

        Raises:
            ValueError: if `folder` is not a plain relative subfolder, or if
                it does not exist locally (which would empty it remotely).
        """
        relative = PurePosixPath(folder)
        if relative.is_absolute() or ".." in relative.parts or not relative.parts:
            raise ValueError(f"Invalid prune path {folder!r}: use a subfolder")

        local_folder = local_path / relative
        if not local_folder.is_dir():
            raise ValueError(
                f"Refusing to prune {folder!r}: {local_folder} does not exist"
            )

        remote_folder = posixpath.join(self._settings.remote_path, relative.as_posix())
        logger.info("Pruning %s", remote_folder)
        self._prune_folder(local_folder, remote_folder)

    def _prune_folder(self, local_folder: Path, remote_folder: str) -> None:
        """Recursively delete remote entries missing from the local folder.

        Args:
            local_folder (Path): local counterpart of `remote_folder`. It may
                not exist, in which case everything inside is deleted.
            remote_folder (str): remote folder to prune.
        """
        try:
            entries = self._sftp.listdir_attr(remote_folder)
        except FileNotFoundError:
            return

        for entry in entries:
            local = local_folder / entry.filename
            remote = posixpath.join(remote_folder, entry.filename)

            if stat.S_ISDIR(entry.st_mode or 0):
                self._prune_folder(local, remote)
                if not local.is_dir():
                    logger.info("Deleting folder %s", remote)
                    self._sftp.rmdir(remote)
            elif not local.is_file():
                logger.info("Deleting %s", remote)
                self._sftp.remove(remote)

    def create_folder(self, remote_path: str) -> None:
        """Create a folder on the remote server, if it does not exist."""
        try:
            if stat.S_ISDIR(self._sftp.stat(remote_path).st_mode or 0):
                return
        except FileNotFoundError:
            pass
        logger.info("Creating folder %s", remote_path)
        self._sftp.mkdir(remote_path)

    def _remote_is_identical(self, local_path: Path, remote_path: str) -> bool:
        """Check whether the remote file has the same content as the local one.

        Args:
            local_path (Path): local file.
            remote_path (str): remote file.

        Returns:
            bool: True if the remote file exists and has the same content.
        """
        try:
            remote_size = self._sftp.stat(remote_path).st_size
        except FileNotFoundError:
            return False

        if remote_size != local_path.stat().st_size:
            return False

        with self._sftp.open(remote_path, "rb") as f:
            remote_hash = hashlib.sha256(f.read()).hexdigest()
        local_hash = hashlib.sha256(local_path.read_bytes()).hexdigest()
        return remote_hash == local_hash

    def upload_file(self, local_path: Path, remote_path: str) -> None:
        """Upload a file to the remote server, unless it is unchanged."""
        if self._remote_is_identical(local_path, remote_path):
            logger.debug("Skipping %s (unchanged)", remote_path)
            return

        logger.info("Uploading %s to %s", local_path, remote_path)
        # upload next to the target and rename, so visitors never see (and a
        # dropped connection never leaves) a partial file
        temporary = f"{remote_path}.tmp"
        try:
            self._sftp.put(str(local_path), temporary)
            self._sftp.posix_rename(temporary, remote_path)
        except Exception:
            try:
                self._sftp.remove(temporary)
            except OSError:
                pass
            raise
