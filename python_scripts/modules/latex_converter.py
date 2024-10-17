"""This module contains the LatexMathConverter class that is used to convert a \
    latex math strings into a png image.

Requirements:
    - pdflatex
    - convert (imagemagick)
"""

from __future__ import annotations

import glob
import os
import subprocess
from datetime import datetime


class LatexMathConverter:
    """LatexMathConverter class."""

    _template: list[str]

    def __init__(self) -> LatexMathConverter:
        """Create a new LatexMathConverter instance."""
        self._template = [
            r"\documentclass[preview, border=0.5pt]{standalone}\begin{document}\[",
            r"\]\end{document}",
        ]

        # check if pdflatex is installed
        if (
            subprocess.run(
                ["pdflatex", "--version"],
                stdout=subprocess.DEVNULL,
            ).returncode
            != 0
        ):
            raise Exception("pdflatex is not installed.")

        # check if convert is installed
        if (
            subprocess.run(
                ["magick", "--version"],
                stdout=subprocess.DEVNULL,
            ).returncode
            != 0
        ):
            raise Exception("convert is not installed.")

    def _createTempDir(self) -> str:
        temp_dir = f"temp-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir

    def _deleteTempDir(self, temp_dir: str) -> None:
        for file in glob.glob(f"{temp_dir}/*"):
            os.remove(file)
        os.rmdir(temp_dir)

    def convert(self, formula: str, output_path: str):
        """Convert the latex formula into a png image.

        Args:
            formula (str): The latex formula to convert.
            output_path (str): The path to save the output png image.
        """
        input_string = "".join(self._template[:1] + [formula] + self._template[1:])
        temp_dir = self._createTempDir()

        p1 = subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-output-directory",
                temp_dir,
                "-jobname",
                "temp",
            ],
            input=input_string.encode("utf-8"),
            stdout=subprocess.DEVNULL,
        )

        if p1.returncode != 0:
            raise Exception("pdflatex failed to compile the formula.")

        p2 = subprocess.run(
            [
                "magick",
                "-density",
                "300",
                "-units",
                "PixelsPerInch",
                f"{temp_dir}/temp.pdf",
                "-quality",
                "90",
                "-trim",
                "-border",
                "5",
                "-channel",
                "RGB",
                "-negate",
                output_path,
            ],
            stdout=subprocess.DEVNULL,
        )

        if p2.returncode != 0:
            raise Exception("convert failed to convert the pdf to png.")

        self._deleteTempDir(temp_dir)
