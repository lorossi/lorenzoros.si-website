"""This module contains the Statement and ControlStatement classes."""


class Statement:
    """Statement class."""

    def __init__(
        self,
        content: str,
        indent: int,
        next_indent: int | None = None,
        token_delimiters: str = "{{",
        list_container: str = "output",
    ) -> None:
        """Create a new Statement instance.

        Args:
            content (str): content of the statement
            indent (int): indent level of the statement
            next_indent (int, optional): indent of the next statement. Defaults to None.
            token_delimiters (str, optional): delimiters for the tokens contained \
                in code.\
                Defaults to "{{".
            list_container (str, optional): name for the generated code container. \
                Defaults to "output".

        Returns:
            Statement: _description_
        """
        self._content = content
        self._indent = indent

        if not next_indent:
            self._next_indent = indent
        else:
            self._next_indent = next_indent

        self._token_delimiters = token_delimiters
        self._list_container = list_container

    def _escapeCode(self, content: str) -> str:
        to_escape = ["'", '"']
        for char in to_escape:
            content = content.replace(char, "\\" + char)

        return content

    def __repr__(self) -> str:
        """Return a string representation of the statement."""
        escaped_content = self._escapeCode(self._content)

        if self._token_delimiters in escaped_content:
            return (
                f"{self._indent * ' '}{self._list_container}."
                f'append(f"""{escaped_content}""")'
            )

        return f'{self._indent * " "}{self._list_container}.append("{escaped_content}")'

    def __str__(self) -> str:
        """Return a string representation of the statement."""
        return self.__repr__()

    @property
    def indent(self) -> int:
        """Indent level of the statement."""
        return self._indent

    @property
    def next_indent(self) -> int:
        """Indent level of the next statement."""
        return self._next_indent

    @property
    def content(self) -> str:
        """Content of the statement."""
        return self._content

    @property
    def list_container(self) -> str:
        """Name of the generated code container."""
        return self._list_container


class ControlStatement(Statement):
    """ControlStatement class."""

    def __init__(
        self,
        content: str,
        indent: int,
        next_indent: int | None = None,
    ) -> None:
        """Create a new ControlStatement instance.

        Args:
            content (str): content of the statement
            indent (int): indent level of the statement
            next_indent (int, optional): indent of the next statement. \
                 Defaults to None.

        Returns:
            ControlStatement
        """
        super().__init__(content, indent, next_indent)

    def __repr__(self) -> str:
        """Return a string representation of the statement."""
        return f"{self._indent * ' '}{self._content}"
