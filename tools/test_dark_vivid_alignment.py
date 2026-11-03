#!/usr/bin/env python3
import importlib.util
import json
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
CONVERTER_PATH = ROOT_DIR / "idea" / "convert.py"
VSCODE_PATH = (
    ROOT_DIR
    / "vscode"
    / "glass-dracula"
    / "themes"
    / "dracula-dark-vivid-black-color-theme.json"
)
IDEA_THEME_PATH = (
    ROOT_DIR
    / "idea"
    / "glass-dracula-idea"
    / "src"
    / "main"
    / "resources"
    / "themes"
    / "DraculaDarkVividBlack.theme.json"
)
IDEA_XML_PATH = IDEA_THEME_PATH.with_name("DraculaDarkVividBlack.xml")
ZED_PATH = (
    ROOT_DIR
    / "zed"
    / "glass-dracula"
    / "themes"
    / "dracula-dark-vivid-black.json"
)

spec = importlib.util.spec_from_file_location("idea_theme_converter", CONVERTER_PATH)
converter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(converter)


class DarkVividAlignmentTest(unittest.TestCase):
    def test_idea_theme_matches_current_vscode_theme(self):
        vscode_theme = json.loads(VSCODE_PATH.read_text(encoding="utf-8"))
        expected_theme = {
            "name": "Dracula Dark Vivid Black",
            "dark": True,
            "author": "BennyWu",
            "parentTheme": "Darcula",
            "editorScheme": "/themes/DraculaDarkVividBlack.xml",
            "ui": converter.build_ui_colors(
                vscode_theme["colors"], True, preserve_source_contrast=True
            ),
        }
        actual_theme = json.loads(IDEA_THEME_PATH.read_text(encoding="utf-8"))
        self.assertEqual(actual_theme, expected_theme)

        zed_style = json.loads(ZED_PATH.read_text(encoding="utf-8"))["themes"][0]["style"]
        expected_background = converter.alpha_blend(
            zed_style["editor.background"], "#000000"
        )
        self.assertEqual(actual_theme["ui"]["*.background"], expected_background)
        self.assertEqual(
            actual_theme["ui"]["*.borderColor"],
            converter.alpha_blend(zed_style["border"], expected_background),
        )
        self.assertEqual(
            actual_theme["ui"]["*.selectionBackground"],
            converter.alpha_blend(zed_style["element.selected"], expected_background),
        )

        expected_xml = converter.build_color_scheme_xml(
            "Dracula Dark Vivid Black",
            True,
            vscode_theme["colors"],
            vscode_theme["tokenColors"],
        )
        self.assertEqual(IDEA_XML_PATH.read_text(encoding="utf-8"), expected_xml)


if __name__ == "__main__":
    unittest.main()
