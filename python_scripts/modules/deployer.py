"""Deployer module."""

from __future__ import annotations

import hashlib
import io
import logging
import posixpath
import stat
from pathlib import Path
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
        for key_class in KEY_CLASSES:
            try:
                return key_class.from_private_key(io.StringIO(content), passphrase)
            except paramiko.SSHException:
                continue
        raise ValueError("Cannot parse private_key")

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

    def disconnect(self) -> None:
        """Disconnect from the remote server."""
        if hasattr(self, "_sftp"):
            self._sftp.close()
        if hasattr(self, "_client"):
            self._client.close()

    def deploy(self, local_path: Path) -> None:
        """Upload the content of a local folder to the remote path.

        Remote files that do not exist locally are left untouched.

        Args:
            local_path (Path): local folder to deploy.
        """
        for path in sorted(local_path.rglob("*")):
            relative = path.relative_to(local_path).as_posix()
            remote_path = posixpath.join(self._settings.remote_path, relative)

            if path.is_dir():
                self.create_folder(remote_path)
            else:
                self.upload_file(path, remote_path)

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
        self._sftp.put(str(local_path), remote_path)
