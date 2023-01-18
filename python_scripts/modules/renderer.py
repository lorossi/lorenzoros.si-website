from __future__ import annotations

import logging
from datetime import datetime

import toml


class Renderer:
    def __init__(self, settings_path: str = "settings.toml"):
        logging.info(f"Initializing {self.__class__.__name__}...")
        self._settings_path = settings_path
        self._loadSettings(settings_path)

    def _loadSettings(self, path: str) -> None:
        logging.info(f"Loading settings from {path}")
        with open(path, "r") as f:
            self._settings = toml.load(f)[self.__class__.__name__]
        logging.info("Loaded settings")

    def _extendContext(self, context: dict) -> dict:
        logging.info("Extending context")

        if "date" not in context:
            context["date"] = datetime.now().strftime("%Y%m%d")

        if "isodate" not in context:
            context["isodate"] = datetime.now().isoformat()

        logging.info("Extended context")
        return context

    def _replaceTokens(self, template: str, context: dict) -> str:
        logging.info("Replacing tokens")

        for key, value in context.items():
            token = "{{ " + key + " }}"
            template = template.replace(token, str(value))

        logging.info("Replaced tokens")
        return template

    def render(self, template: str, context: dict, out_path: str) -> None:
        logging.info(f"Rendering {template} to {out_path}")
        with open(template, "r") as f:
            template = f.read()

        context = self._extendContext(context)
        template = self._replaceTokens(template, context)

        with open(out_path, "w") as f:
            f.write(template)
        logging.info("Rendered")
