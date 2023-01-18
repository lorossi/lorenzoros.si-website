from __future__ import annotations

import logging

import toml


class Renderer:
    def __init__(self, settings_path: str = "settings.toml"):
        logging.info(f"Initializing {self.__class__.__name__}...")
        self._settings_path = settings_path
        self._loadSettings(settings_path)
        self._loadBase()

    def _loadSettings(self, path: str) -> None:
        logging.info(f"Loading settings from {path}")
        with open(path, "r") as f:
            self._settings = toml.load(f)[self.__class__.__name__]
        logging.info("Loaded settings")

    def _loadBase(self):
        full_path = self._settings["resources_path"] + self._settings["base_filename"]
        logging.info(f"Loading base from {full_path}...")
        with open(full_path, "r") as f:
            self._base = f.read()
        logging.info("Base file loaded")

    def embedContent(self, content: str, token: str) -> None:
        html_token = "{{ " + token + " }}"
        logging.info(f"Embedding {html_token}...")
        self._base = self._base.replace(html_token, content)

    def saveHTML(self, base_path: str, filename: str = "index.html") -> None:
        full_path = base_path + filename
        logging.info(f"Saving HTML to {full_path} for {self.__class__.__name__}")
        with open(full_path, "w") as f:
            f.write(self._base)
        logging.info("Saved HTML")
