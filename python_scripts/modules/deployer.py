"""Deployer module."""

from __future__ import annotations

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

    def __init__(self, settings_path="settings.toml") -> Deployer:
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
            logging.info(f"Uploading {local_path} ... to {remote_path}")

            if os.path.isdir(local_path):
                self._createFolder(remote_path)
            else:
                self._uploadFile(local_path, remote_path)

    def _createFolder(self, remote_path: str) -> None:
        """Create a folder on the remote server."""
        try:
            self._sftp.mkdir(remote_path)
        except IOError:
            logging.info(f"Folder {remote_path} already exists.")

    def _getRemoteMtime(self, remote_path: str) -> int | None:
        """Get the mtime of a remote file."""
        try:
            return self._sftp.stat(remote_path).st_mtime
        except IOError:
            return None

    def _getLocalMtime(self, local_path: str) -> int:
        """Get the mtime of a local file."""
        return int(os.path.getmtime(local_path))

    def _uploadFile(self, local_path: str, remote_path: str) -> None:
        """Upload a file to the remote server."""
        local_mtime = self._getLocalMtime(local_path)
        remote_mtime = self._getRemoteMtime(remote_path)

        if remote_mtime is None or local_mtime > remote_mtime:
            self._uploadSingleFile(local_path, remote_path, local_mtime)
        else:
            time_diff = remote_mtime - local_mtime
            if time_diff == 0:
                logging.info("File skipped (remote file has the same mtime).")
            else:
                logging.info(
                    f"File skipped (remote file is {time_diff} seconds newer)."
                )

    def _uploadSingleFile(self, local_path: str, remote_path: str, mtime: int):
        """Upload a single file to the remote server."""
        self._sftp.put(local_path, remote_path)
        self._sftp.utime(remote_path, (mtime, mtime))
        logging.info("File uploaded.")
