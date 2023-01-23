from __future__ import annotations


class Statement:
    def __init__(
        self,
        content: str,
        indent: int,
        next_indent: int = None,
        token_delimiters: str = "{{",
        list_container: str = "output",
    ) -> Statement:
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
        escaped_content = self._escapeCode(self._content)

        if self._token_delimiters in escaped_content:
            return (
                f"{self._indent * ' '}{self._list_container}."
                f'append(f"{escaped_content}")'
            )

        return (
            f"{self._indent * ' '}{self._list_container}.append(\"{escaped_content}\")"
        )

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def indent(self) -> int:
        return self._indent

    @property
    def next_indent(self) -> int:
        return self._next_indent

    @property
    def content(self) -> str:
        return self._content

    @property
    def list_container(self) -> str:
        return self._list_container


class ControlStatement(Statement):
    def __init__(
        self, content: str, indent: int, next_indent: int = None
    ) -> ControlStatement:
        super().__init__(content, indent, next_indent)

    def __repr__(self) -> str:
        return f"{self._indent * ' '}{self._content}"
