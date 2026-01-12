"""Deployer module."""

from __future__ import annotations

import hashlib
import logging
import os
import re
from glob import glob

import paramiko

from modules.settings import Settings


class Deployer:
    """Deployer class."""

    _settings: Settings
    _client: paramiko.SSHClient
    _sftp: paramiko.SFTPClient

    def __init__(self, settings_path="settings.toml") -> None:
        """Create a new Renderer instance.

        Args:
            settings_path (str, optional): Settings path. Defaults to "settings.toml".
        """
        self._settings = Settings.from_toml(settings_path, self.__class__.__name__)

    def connect(self):
        """Connect to the remote server."""
        logging.info("Connecting to remote server...")
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._client.connect(
            hostname=self._settings.hostname,
            key_filename=self._settings.key_filename,
            username=self._settings.username,
            password=self._settings.password,
        )
        logging.info("Connected.")
        self._sftp = self._client.open_sftp()

    def disconnect(self):
        """Disconnect from the remote server."""
        self._sftp.close()
        self._client.close()

    def deploy(self):
        """Deploy local files to the remote server."""
        for local_path in glob(self._settings.local_path + "/**/*", recursive=True):
            remote_path = self._settings.remote_path + re.sub(
                r".*" + self._settings.local_path, "", local_path
            )
            logging.info("Uploading %s to %s", local_path, remote_path)

            if os.path.isdir(local_path):
                self._createFolder(remote_path)
            else:
                self._uploadFile(local_path, remote_path)

    def _createFolder(self, remote_path: str) -> None:
        """Create a folder on the remote server."""
        try:
            self._sftp.mkdir(remote_path)
        except IOError:
            logging.info("Folder %s already exists.", remote_path)

    def _hashRemoteFile(self, remote_path: str) -> str | None:
        """Get the SHA256 hash of a remote file."""
        try:
            with self._sftp.open(remote_path, "rb") as f:
                file_data = f.read()
                return hashlib.sha256(file_data).hexdigest()
        except IOError:
            return None

    def _hashLocalFile(self, local_path: str) -> str:
        """Get the SHA256 hash of a local file."""
        with open(local_path, "rb") as f:
            file_data = f.read()
            return hashlib.sha256(file_data).hexdigest()

    def _uploadFile(self, local_path: str, remote_path: str) -> None:
        """Upload a file to the remote server."""
        local_hash = self._hashLocalFile(local_path)
        remote_hash = self._hashRemoteFile(remote_path)

        if remote_hash is None or local_hash != remote_hash:
            self._uploadSingleFile(local_path, remote_path)
        else:
            logging.info("File skipped (remote file has the same hash).")

    def _uploadSingleFile(self, local_path: str, remote_path: str) -> None:
        """Upload a single file to the remote server."""
        self._sftp.put(local_path, remote_path)
        logging.info("File uploaded.")
