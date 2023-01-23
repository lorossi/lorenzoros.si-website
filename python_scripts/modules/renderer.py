"""This module contains the Renderer class, which is responsible for rendering."""
from __future__ import annotations

import logging
import re

from typing_extensions import Any

from .context import Context
from .formatter import HTMLFormatter
from .function_factory import FunctionFactory
from .settings import Settings
from .statements import Statement
from .statements_factory import StatementFactory


class Renderer:
    """This class is responsible for rendering the templates."""

    _settings: Settings
    _context: Context
    _list_container = "output"

    def __init__(self, settings_path="settings.toml") -> Renderer:
        """Create a new Renderer instance.

        Args:
            settings_path (str, optional): Settings path. Defaults to "settings.toml".
        """
        self._settings = Settings.from_toml(settings_path, self.__class__.__name__)

    def _nullEmptyStr(self, text: str) -> str:
        if text == "":
            return "None"
        return text

    def _extractAttribute(self, context: Context, item: Any, attribute: Any) -> Any:
        if attribute and hasattr(context.get(item), attribute):
            return str(getattr(context.get(item), attribute))

        return str(context.get(item))

    def _replaceTokensInCode(self, text: str, context: Context) -> str:
        new_value = ""

        for match in re.finditer(
            r"\{\{([a-z_]+)(\.[a-z_]+)?(\|([a-z_\|]+))*\}\}", text
        ):
            item = self._nullEmptyStr(match.group(1))
            attribute = self._nullEmptyStr(match.group(2))

            if attribute:
                new_value = self._extractAttribute(context, item, attribute)
            else:
                new_value = str(context.get(item))

            if match.group(3):
                functions = match.group(3)[1:].split("|")
            else:
                functions = []

            if item in context:
                for function in functions:
                    new_value = FunctionFactory.create(function)(new_value)
                text = text.replace(match.group(), new_value)
            else:
                text = text.replace(match.group(), match.group()[1:-1])

        return text, new_value

    def _createStatements(self, template: str) -> list[Statement]:
        """Create statements from the text.

        Args:
            text (str): The text to be parsed
            indent (int): The current indent

        Returns:
            list[Statement]: The statements
        """
        statements = []
        for line in template.split("\n"):
            if len(statements) == 0:
                indent = 0
            else:
                indent = statements[-1].next_indent

            statements.append(
                StatementFactory.create(
                    line, indent=indent, list_container=self._list_container
                )
            )

        return statements

    def _createInstructions(self, statements: list[Statement], context) -> list[str]:
        """Create instructions from the statements.

        Args:
            statements (list[Statement]): The statements

        Returns:
            list[str]: The instructions
        """
        instructions = []
        for statement in statements:
            instruction, replaced = self._replaceTokensInCode(str(statement), context)

            if "\n" in replaced:
                # if newline was found in the code, it means that it was replaced
                # we need to create new statements recursively
                new_statements = [
                    self._createStatements(line) for line in replaced.split("\n")
                ]
                instructions.append(self._createInstructions(new_statements, context))
            else:
                instructions.append(instruction)
        ...
        return "\n".join(instructions)

    def _runCode(self, code: str, context: Context) -> str:
        """Run code and return the output.

        Args:
            instructions (list[str]): The code to be ran

        Returns:
            str
        """
        local_variables = {
            **context,
            self._list_container: [],
        }
        exec(code, local_variables)
        return "\n".join(local_variables["output"])

    def _format(self, text: str) -> str:
        """Format the text.

        Args:
            text (str): The text to be formatted

        Returns:
            str: The formatted text
        """
        return HTMLFormatter.format(text)

    def renderFile(
        self,
        template_name: str,
        context_dict: dict = None,
        context: Context = None,
        format: bool = False,
        output_path: str = None,
    ) -> str:
        """Render the template.

        Args:
            template_name (str): The name of the template
            context (dict, optional): Custom context for the template. Defaults to None.
            format (bool, optional): Auto format the rendered page. Defaults to False.
            output_path (str, optional): The path to save the rendered page. \
                Defaults to None.

        Returns:
            str: rendered page
        """
        logging.info(f"Rendering file {template_name} ...")
        template_path = self._settings.templates_path + template_name
        with open(template_path, "r") as f:
            template = f.read()
        logging.info(f"Template loaded from {template_path}.")

        rendered = self.renderString(
            template, context_dict=context_dict, context=context, format=format
        )

        if output_path:
            logging.info(f"Saving rendered page to {output_path}...")
            with open(output_path, "w") as f:
                f.write(rendered)
            logging.info("Saved.")

        return rendered

    def renderString(
        self,
        template: str,
        context_dict: dict = None,
        context: Context = None,
        format: bool = False,
    ) -> str:
        """Render the template.

        Args:
            template (str): The template
            context (dict, optional): Custom context for the template. Defaults to None.
            format (bool, optional): Auto format the rendered page. Defaults to False.

        Returns:
            str: rendered page
        """
        logging.info(f"Rendering string of length {len(template)}")
        if context is None:
            context = Context()

        if context_dict is not None:
            context.update(Context(**context_dict))

        logging.info("Solving includes...")
        # solve the include first
        for match in re.findall(r"\{% include ([a-z.]+) %\}", template):
            logging.info(f"Including: {match}")
            template = template.replace(
                "{% include " + match + " %}", self.renderFile(match, context=context)
            )
        logging.info("Includes solved")

        logging.info("Creating statements...")
        statements = self._createStatements(template)
        instructions = self._createInstructions(statements, context)

        logging.info("Running code...")
        output = self._runCode(instructions, context)

        if format:
            logging.info("Formatting...")
            output = self._format(output)

        logging.info("Rendering finished")
        return output
