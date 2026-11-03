#!/usr/bin/env python3
"""Check idea PandaModernDark colors match vscode Panda Modern Dark."""
import json, unittest, xml.etree.ElementTree as ET
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
VS = json.loads((ROOT/"vscode/panda-vivid-black/themes/panda-modern-dark-color-theme.json").read_text())
RES = ROOT/"idea/panda-vivid-black/src/main/resources"
X = ET.parse(RES/"themes/PandaModernDark.xml").getroot()
H = lambda v: v.lstrip("#").upper()[:6]

def attr(name):
    for o in X.find("attributes"):
        if o.get("name") == name:
            v = o.find("value")
            return {c.get("name"): c.get("value").upper() for c in v} if v is not None else {}
    raise AssertionError(f"missing {name}")

def sem(k):
    v = VS["semanticTokenColors"][k]
    return H(v["foreground"] if isinstance(v, dict) else v)

class T(unittest.TestCase):
    def fg(self, key, exp):
        self.assertEqual(attr(key).get("FOREGROUND"), exp, key)

    def test_registered_and_valid(self):
        p = (RES/"META-INF/plugin.xml").read_text()
        self.assertIn("/themes/PandaModernDark.theme.json", p)
        self.assertIn("/themes/PandaModernDarkIslands.theme.json", p)
        for f in ("PandaModernDark.theme.json", "PandaModernDarkIslands.theme.json"):
            t = json.loads((RES/"themes"/f).read_text())
            self.assertEqual(t["editorScheme"], "/themes/PandaModernDark.xml")

    def test_editor(self):
        t = attr("TEXT")
        self.assertEqual(t["BACKGROUND"], H(VS["colors"]["editor.background"]))
        self.assertEqual(t["FOREGROUND"], H(VS["colors"]["editor.foreground"]))

    def test_semantic_defaults(self):
        for key, s in [("DEFAULT_KEYWORD","keyword"),("DEFAULT_STRING","string"),("DEFAULT_NUMBER","numberLiteral"),
                       ("DEFAULT_FUNCTION_DECLARATION","function"),("DEFAULT_FUNCTION_CALL","method"),
                       ("DEFAULT_CLASS_NAME","class"),("DEFAULT_INTERFACE_NAME","interface"),
                       ("DEFAULT_COMMENT","comment"),("DEFAULT_PARAMETER","parameter"),
                       ("DEFAULT_LOCAL_VARIABLE","variable"),("DEFAULT_INSTANCE_FIELD","property"),
                       ("DEFAULT_OPERATION_SIGN","operator")]:
            self.fg(key, sem(s))

    def test_no_italics(self):
        for o in X.find("attributes"):
            v = o.find("value")
            if v is not None:
                for c in v:
                    if c.get("name") == "FONT_TYPE" and "MARKUP_ITALIC" not in o.get("name"):
                        self.assertFalse(int(c.get("value")) & 2, o.get("name"))

    def test_kotlin(self):
        self.fg("KOTLIN_KEYWORD", sem("keyword")); self.fg("KOTLIN_CLASS", sem("class"))
        self.fg("KOTLIN_FUNCTION_CALL", sem("function")); self.fg("KOTLIN_EXTENSION_FUNCTION_CALL", sem("function"))
        self.fg("KOTLIN_PARAMETER", sem("parameter")); self.fg("KOTLIN_INSTANCE_PROPERTY", sem("property"))
        self.fg("KOTLIN_ANNOTATION", sem("annotation:dart"))
        self.fg("KOTLIN_STRING", sem("string")); self.fg("KOTLIN_NUMBER", sem("numberLiteral"))

    def test_dart(self):
        self.fg("DART_KEYWORD", sem("keyword")); self.fg("DART_ANNOTATION", sem("annotation:dart"))
        self.fg("DART_CLASS", sem("class")); self.fg("DART_CONSTRUCTOR", sem("class"))
        self.fg("DART_INSTANCE_METHOD_REFERENCE", sem("method")); self.fg("DART_TOP_LEVEL_FUNCTION_DECLARATION", sem("function"))
        self.fg("DART_PARAMETER_REFERENCE", sem("parameter.label:dart")); self.fg("DART_PARAMETER_DECLARATION", sem("parameter")); self.fg("DART_STATIC_GETTER_REFERENCE", sem("property"))
        self.fg("DART_INSTANCE_FIELD_REFERENCE", sem("property")); self.fg("DART_STRING", sem("stringLiteral"))

    def test_xml_json_toml(self):
        self.fg("XML_TAG_NAME", "7EE787"); self.fg("XML_ATTRIBUTE_NAME", "96D2FF"); self.fg("XML_ATTRIBUTE_VALUE", sem("string"))
        self.fg("JSON_PROPERTY_KEY", sem("property")); self.fg("org.toml.KEY", sem("property"))

    def test_vcs_diff(self):
        cols = {o.get("name"): (o.get("value") or "").upper() for o in X.find("colors")}
        c = VS["colors"]
        self.assertEqual(cols["ADDED_LINES_COLOR"], H(c["editorGutter.addedBackground"]))
        self.assertEqual(cols["MODIFIED_LINES_COLOR"], H(c["editorGutter.modifiedBackground"]))
        self.assertEqual(cols["DELETED_LINES_COLOR"], H(c["editorGutter.deletedBackground"]))
        self.assertIn("BACKGROUND", attr("DIFF_INSERTED")); self.assertIn("BACKGROUND", attr("DIFF_DELETED"))

    def test_logcat(self):
        for k in ("LOGCAT_V2_MESSAGE_ERROR", "LOGCAT_V2_MESSAGE_WARNING", "LOGCAT_V2_MESSAGE_INFO"):
            attr(k)

if __name__ == "__main__":
    unittest.main()


class RealKeys121(unittest.TestCase):
    def test_dart_named_label_and_static_getter_cyan(self):
        import xml.etree.ElementTree as ET, os
        x = ET.parse(os.path.join(os.path.dirname(__file__), "panda-vivid-black/src/main/resources/themes/PandaModernDark.xml"))
        fg = {o.get("name"): o.find("value/option[@name='FOREGROUND']") for o in x.getroot().find("attributes")}
        for k in ("DART_PARAMETER_REFERENCE", "DART_STATIC_GETTER_REFERENCE", "LOGCAT_V2_MESSAGE_ERROR"):
            self.assertIn(k, fg)
        self.assertEqual(fg["DART_PARAMETER_REFERENCE"].get("value").upper(), "00D2F9")
        self.assertEqual(fg["DART_STATIC_GETTER_REFERENCE"].get("value").upper(), "00D2F9")
        for bad in ("DART_NAMED_PARAMETER", "KOTLIN_MODIFIER", "DART_INSTANCE_MEMBER_FUNCTION"):
            self.assertNotIn(bad, fg)
