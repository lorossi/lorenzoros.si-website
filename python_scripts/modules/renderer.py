"""This module contains the Renderer class, which is responsible for rendering."""

from __future__ import annotations

import logging

import jinja2
import jinja2.sandbox
from lxml.html import fromstring, tostring

from modules.settings import Settings


class Renderer:
    """This class is responsible for rendering the templates."""

    _settings: Settings
    _environment: jinja2.sandbox.SandboxedEnvironment
    _list_container: str = "output"

    def __init__(self, settings_path="settings.toml") -> None:
        """Create a new Renderer instance.

        Args:
            settings_path (str, optional): Settings path. Defaults to "settings.toml".
        """
        self._settings = Settings.from_toml(settings_path, self.__class__.__name__)
        self._environment = jinja2.sandbox.SandboxedEnvironment(
            loader=jinja2.FileSystemLoader(self._settings.templates_path)
        )

    def renderFile(
        self,
        template_name: str,
        data: dict | None = None,
        format: bool = True,
        output_path: str | None = None,
    ) -> str:
        """Render the template.

        Args:
            template_name (str): The name of the template
            data (dict, optional): The data to render the template with. Defaults to None.
            format (bool, optional): Auto format the rendered page. Defaults to True.
        output_path (str, optional): The path to save the rendered page.
                Defaults to None.

        Returns:
            str: rendered page
        """
        logging.info("Rendering file %s ...", template_name)
        template = self._environment.get_template(template_name)
        template_path = self._settings.templates_path + template_name
        logging.info("Template loaded from %s.", template_path)

        content = template.render(data if data is not None else {})

        if format:
            root = fromstring(content)
            content = tostring(root, pretty_print=True, encoding="unicode").strip()

        if output_path:
            logging.info("Saving rendered page to %s...", output_path)
            with open(output_path, "w") as f:
                f.write(content)  # type: ignore
            logging.info("Saved.")

        return content  # type: ignore
