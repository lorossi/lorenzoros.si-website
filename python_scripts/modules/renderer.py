"""This module contains the Renderer class, which is responsible for rendering."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import jinja2

logger = logging.getLogger(__name__)


class Renderer:
    """This class is responsible for rendering the templates."""

    def __init__(self, templates_path: Path, **template_globals: Any) -> None:
        """Create a new Renderer instance.

        Args:
            templates_path (Path): folder containing the templates.
            **template_globals: variables available to every template.
        """
        self._environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_path),
            autoescape=jinja2.select_autoescape(),
            undefined=jinja2.StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self._environment.globals.update(template_globals)

    def render_file(
        self,
        template_name: str,
        output_path: Path,
        data: dict[str, Any] | None = None,
    ) -> str:
        """Render a template and save it to a file.

        Args:
            template_name (str): The name of the template.
            output_path (Path): The path to save the rendered page to.
            data (dict[str, Any] | None, optional): The data to render the
                template with. Defaults to None.

        Returns:
            str: rendered page
        """
        logger.info("Rendering %s to %s", template_name, output_path)
        template = self._environment.get_template(template_name)
        content = template.render(**(data or {}))

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        return content
