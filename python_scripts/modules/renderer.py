"""This module contains the Renderer class, which is responsible for rendering."""

from __future__ import annotations

import logging
import re

import jinja2

from modules.formatter import HTMLFormatter
from modules.settings import Settings


class Renderer:
    """This class is responsible for rendering the templates."""

    _settings: Settings
    _environment: jinja2.Environment
    _list_container: str = "output"

    def __init__(self, settings_path="settings.toml") -> None:
        """Create a new Renderer instance.

        Args:
            settings_path (str, optional): Settings path. Defaults to "settings.toml".
        """
        self._settings = Settings.from_toml(settings_path, self.__class__.__name__)
        self._environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self._settings.templates_path)
        )

    def renderFile(
        self,
        template_name: str,
        context_dict: dict | None = None,
        format: bool = True,
        output_path: str | None = None,
    ) -> str:
        """Render the template.

        Args:
            template_name (str): The name of the template
            context (dict, optional): Custom context for the template. Defaults to None.
            format (bool, optional): Auto format the rendered page. Defaults to True.
            output_path (str, optional): The path to save the rendered page. \
                Defaults to None.

        Returns:
            str: rendered page
        """
        logging.info("Rendering file %s ...", template_name)
        template = self._environment.get_template(template_name)
        template_path = self._settings.templates_path + template_name
        logging.info("Template loaded from %s.", template_path)

        content = template.render(
            **(context_dict if context_dict is not None else {}),
        )

        if format:
            content = HTMLFormatter.format(content)

        if output_path:
            logging.info("Saving rendered page to %s...", output_path)
            with open(output_path, "w") as f:
                f.write(content)
            logging.info("Saved.")

        return content
