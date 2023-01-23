from __future__ import annotations

import re

from .statements import ControlStatement, Statement


class StatementFactory:

    _indentMap = {
        "if": 0,
        "elif": -2,
        "else": -2,
        "for": 0,
        "end": -2,
    }

    _nextIndentMap = {
        "if": 2,
        "elif": 2,
        "else": 2,
        "for": 2,
        "end": -2,
    }

    _hasCondition = {
        "if": True,
        "elif": True,
        "else": False,
        "for": True,
        "end": False,
    }

    _hasContent = {
        "if": True,
        "elif": True,
        "else": True,
        "for": True,
        "end": False,
    }

    @staticmethod
    def create(line: str, indent: int, list_container: str = "output") -> Statement:
        if "{%" and "%}" in line:
            return StatementFactory.createControlStatement(line, indent)
        return StatementFactory.createStatement(line, indent, list_container)

    @staticmethod
    def createControlStatement(line: str, indent: int) -> Statement:
        groups = re.search(r"{% ([a-z]+)\s?(.*)? %}", line)
        if not groups:
            raise ValueError(f"Statement not found in line: {line}")

        operation = groups.group(1)
        condition = groups.group(2)

        if operation not in StatementFactory._indentMap:
            raise ValueError(f"Statement {operation} not found")

        if StatementFactory._hasCondition[operation] != (condition != ""):
            raise ValueError(f"Statement {operation} has an invalid condition")

        current_indent = indent + StatementFactory._indentMap[operation]
        next_indent = indent + StatementFactory._nextIndentMap[operation]

        if not StatementFactory._hasContent[operation]:
            content = "..."  # NOP
        elif condition:
            content = f"{operation} {condition}:"
        else:
            content = f"{operation}:"

        return ControlStatement(
            content=content,
            indent=current_indent,
            next_indent=next_indent,
        )

    @staticmethod
    def createStatement(line: str, indent: int, list_container: str) -> Statement:
        return Statement(
            content=line,
            indent=indent,
            next_indent=indent,
            list_container=list_container,
        )
