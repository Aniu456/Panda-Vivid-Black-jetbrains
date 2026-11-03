#!/usr/bin/env python3
"""Check idea/panda-vivid-black colors match vscode/panda-vivid-black."""
import json, re, unittest, xml.etree.ElementTree as ET
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
VS = json.loads((ROOT/"vscode/panda-vivid-black/themes/panda-vivid-black-color-theme.json").read_text())
RES = ROOT/"idea/panda-vivid-black/src/main/resources"
X = ET.parse(RES/"themes/PandaVividBlack.xml").getroot()

def attr(name):
    for o in X.find("attributes"):
        if o.get("name") == name:
            v = o.find("value")
            return {c.get("name"): c.get("value") for c in v} if v is not None else {}
    raise AssertionError(f"missing {name}")

def sem(k):
    v = VS["semanticTokenColors"][k]
    return (v["foreground"] if isinstance(v, dict) else v).lstrip("#").upper()

class T(unittest.TestCase):
    def fg(self, key, exp, italic=None):
        a = attr(key)
        got = a.get("FOREGROUND", "").upper()
        d = max(abs(int(got[i:i+2], 16) - int(exp[i:i+2], 16)) for i in (0, 2, 4))
        self.assertLessEqual(d, 24, f"{key}: {got} vs {exp}")  # tolerate hand-tuned nudges
        if italic is not None:
            self.assertEqual(a.get("FONT_TYPE") == "2", italic, key + " italic")

    def test_files_valid(self):
        ET.parse(RES/"META-INF/plugin.xml")
        for f in (RES/"themes").glob("*.theme.json"):
            json.loads(f.read_text())

    def test_editor_bg(self):
        # hand-tuned to pure black in IDEA (VS Code #0B0B0E): accept either
        self.assertIn(attr("TEXT")["BACKGROUND"].upper(), {"000000", VS["colors"]["editor.background"].lstrip("#").upper()})

    def test_semantic_defaults(self):
        for key, s in [("DEFAULT_KEYWORD","keyword"),("DEFAULT_STRING","string"),("DEFAULT_NUMBER","number"),
                       ("DEFAULT_FUNCTION_DECLARATION","function"),("DEFAULT_COMMENT","comment")]:
            self.fg(key, sem(s))

    def test_kotlin(self):
        self.fg("KOTLIN_KEYWORD", sem("keyword")); self.fg("KOTLIN_CLASS", sem("class"), True)
        self.fg("KOTLIN_FUNCTION_CALL", sem("function")); self.fg("KOTLIN_PARAMETER", sem("parameter"), True)
        self.fg("KOTLIN_NAMED_ARGUMENT", sem("parameter"), True)
        self.fg("KOTLIN_INSTANCE_PROPERTY", sem("property")); self.fg("KOTLIN_ENUM_ENTRY", sem("enumMember"))
        self.fg("KOTLIN_EXTENSION_FUNCTION_CALL", sem("function"), True)
        self.fg("KOTLIN_ANNOTATION", "FFA647")  # textmate `storage`

    def test_dart(self):
        self.fg("DART_KEYWORD", "FF4F9D"); self.fg("DART_ANNOTATION", "00CFFF")  # storage.type.annotation.dart
        self.fg("DART_CLASS", sem("class"), True); self.fg("DART_CONSTRUCTOR", sem("class"), True)
        self.fg("DART_INSTANCE_METHOD_REFERENCE", sem("method")); self.fg("DART_PARAMETER_REFERENCE", sem("parameter"), True); self.fg("DART_STATIC_GETTER_REFERENCE", sem("property"))
        self.fg("DART_INSTANCE_FIELD_REFERENCE", sem("property")); self.fg("DART_ENUM_CONSTANT", sem("enumMember"))

    def test_xml_json(self):
        self.fg("XML_TAG_NAME", "FF2D8D"); self.fg("XML_ATTRIBUTE_NAME", "FFA647"); self.fg("XML_ATTRIBUTE_VALUE", sem("string"))
        self.fg("JSON_PROPERTY_KEY", sem("property"))

    def test_console_ansi(self):
        c = VS["colors"]
        for k, v in [("CONSOLE_RED_OUTPUT","terminal.ansiRed"),("CONSOLE_GREEN_OUTPUT","terminal.ansiGreen"),
                     ("CONSOLE_BLUE_OUTPUT","terminal.ansiBlue"),("CONSOLE_YELLOW_OUTPUT","terminal.ansiYellow")]:
            self.fg(k, c[v].lstrip("#").upper())

    def test_vcs(self):
        cols = {o.get("name"): o.get("value") for o in X.find("colors")}
        c = VS["colors"]
        self.assertEqual(cols["ADDED_LINES_COLOR"], c["editorGutter.addedBackground"].lstrip("#").upper())
        self.assertEqual(cols["MODIFIED_LINES_COLOR"], c["editorGutter.modifiedBackground"].lstrip("#").upper())
        self.assertEqual(cols["DELETED_LINES_COLOR"], c["editorGutter.deletedBackground"].lstrip("#").upper())

if __name__ == "__main__":
    unittest.main()
