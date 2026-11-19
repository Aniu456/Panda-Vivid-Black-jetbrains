"""Panda Flutter Dark: JetBrains / Android Studio attribute keys.

Recreates the official DartPad / Flutter dark editor (dart-lang/dart-pad
pkgs/dartpad_ui/web/styles/cm-dartpad-dark.css). Source of truth for the
VS Code side: vscode/panda-vivid-black/themes/panda-flutter-dark-color-theme.json.
Reuses the key tables of panda_jetbrains_extras with the Flutter palette.
DartPad uses no italics, so every italic is dropped.
"""
import re
from pathlib import Path

KW, TYPE, CY = "#50E191", "#FF916E", "#00D2FA"
STR, STR2, NUM, COM, META, NS = "#FA557D", "#FF00FA", "#909090", "#909CC3", "#909090", "#FF9B00"
BG = "#0C0C0C"  # same near-black as Modern Dark / Modern Cyan

# UI (.theme.json / Islands) text uses Modern Cyan's #E8E8E8; the editor scheme
# keeps the DartPad white default text (editor.foreground #FFFFFF).
UI_COLOR_OVERRIDES = {"editor.foreground": "#E8E8E8"}

P = dict(
    _name="flutter-dark", kw=KW, fn=CY, type=TYPE, enum=TYPE, var=CY,
    param=CY, prop=CY, str=STR, num=NUM, regexp=STR2,
    op="#FFFFFF", comment=COM, const=CY, esc=STR2, tag=KW,
    attr=CY, orange=STR2, storage=META, deco=META,
    dart_anno=META, doc_tag=COM, doc_val=COM, purple=NS,
    err="#FF2D64", warn="#FFA618", gray="#909090", ignored="#898076",
    added="#59CC8A", modified="#006BCD", deleted="#FF8330",
)

_src = (Path(__file__).with_name("panda_jetbrains_extras.py")).read_text()
_src = re.sub(r"^P = dict\(.*?^\)\n", "P = _P\n", _src, count=1, flags=re.S | re.M)
_ns = {"_P": P}
exec(compile(_src, "panda_jetbrains_extras(flutter)", "exec"), _ns)

def _noitalic(ft):
    if ft is None: return None
    return ft & ~2

COMMON = {k: (fg, bg, _noitalic(ft)) for k, (fg, bg, ft) in _ns["COMMON"].items()}
COMMON.update({
    "DEFAULT_CONSTANT": (TYPE, None, None),                # true / false / null atoms
    "DEFAULT_STATIC_FIELD": (CY, None, None),
    "DEFAULT_LABEL": (CY, None, None),
    "KOTLIN_ANNOTATION": (META, None, None),
    "KOTLIN_NAMED_ARGUMENT": (CY, None, None),
    "KOTLIN_STRING_TEMPLATE_ENTRY": (STR2, None, None),
    "KOTLIN_SMART_CAST_VALUE": (CY, "#0E2A35", None),
    "KOTLIN_SMART_CAST_RECEIVER": (CY, "#0E2A35", None),
    "KOTLIN_SMART_CONSTANT": (NUM, "#0E2A35", None),
    "KOTLIN_PACKAGE_PROPERTY": (CY, None, None),
    "KOTLIN_CLOSURE_DEFAULT_PARAMETER": (CY, None, None),
    "KOTLIN_LABEL": (CY, None, None),
    # Dart / Flutter
    "DART_KEYWORD": (KW, None, None),
    "DART_ANNOTATION": (META, None, None),
    "DART_SYMBOL_LITERAL": (STR2, None, None),
    "DART_VALID_STRING_ESCAPE": (STR2, None, None),
    "DART_DOC_COMMENT": (COM, None, None),
    "DART_TYPE_NAME_DYNAMIC": (TYPE, None, None),
    "DART_ENUM": (TYPE, None, None), "DART_ENUM_CONSTANT": (CY, None, None),
    "DART_IMPORT_PREFIX": (NS, None, None), "DART_LIBRARY_NAME": (NS, None, None),
    "DART_LABEL": (CY, None, None),
    "DART_NAMED_PARAMETER": (CY, None, None),
    "XML_NS_PREFIX": (NS, None, None),
    "XML_TAG": ("#FFFFFF", None, None),
    "XML_TAG_NAME": (KW, None, None), "XML_CUSTOM_TAG_NAME": (KW, None, None),
    "XML_PROLOGUE": (META, None, None), "XML_ENTITY_REFERENCE": (STR2, None, None),
    "DEFAULT_TAG": (KW, None, None),
    "JSON_KEYWORD": (TYPE, None, None),                    # true / false / null
    "YAML_SCALAR_KEY": (CY, None, None),
    # JavaScript / TypeScript (only when the JS plugin is present)
    "JS.INSTANCE_MEMBER_FUNCTION": (CY, None, None), "JS.STATIC_MEMBER_FUNCTION": (CY, None, None),
    "JS.GLOBAL_FUNCTION": (CY, None, None), "JS.LOCAL_FUNCTION": (CY, None, None),
    "JS.INSTANCE_MEMBER_VARIABLE": (CY, None, None), "JS.STATIC_MEMBER_VARIABLE": (CY, None, None),
    "JS.GLOBAL_VARIABLE": (CY, None, None), "JS.LOCAL_VARIABLE": (CY, None, None),
    "JS.PARAMETER": (CY, None, None),
    # console ANSI: VS Code built-in dark defaults
    "CONSOLE_NORMAL_OUTPUT": ("#FFFFFF", None, None), "CONSOLE_ERROR_OUTPUT": ("#F14C4C", None, None),
    "CONSOLE_SYSTEM_OUTPUT": ("#909090", None, None), "CONSOLE_USER_INPUT": ("#50E191", None, None),
    "CONSOLE_BLACK_OUTPUT": ("#000000", None, None), "CONSOLE_RED_OUTPUT": ("#CD3131", None, None),
    "CONSOLE_GREEN_OUTPUT": ("#0DBC79", None, None), "CONSOLE_YELLOW_OUTPUT": ("#E5E510", None, None),
    "CONSOLE_BLUE_OUTPUT": ("#2472C8", None, None), "CONSOLE_MAGENTA_OUTPUT": ("#BC3FBC", None, None),
    "CONSOLE_CYAN_OUTPUT": ("#11A8CD", None, None), "CONSOLE_GRAY_OUTPUT": ("#E5E5E5", None, None),
    "CONSOLE_DARKGRAY_OUTPUT": ("#666666", None, None),
    # search / highlight: same values as Modern Cyan (VS Code alphas on #0C0C0C)
    "TEXT_SEARCH_RESULT_ATTRIBUTES": (None, "#063A4D", None),
    "SEARCH_RESULT_ATTRIBUTES": (None, "#063A4D", None),
    "IDENTIFIER_UNDER_CARET_ATTRIBUTES": (None, "#082731", None),
    "WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES": (None, "#0A3442", None),
    "TODO_DEFAULT_ATTRIBUTES": ("#FFA618", None, 1),
    "NOT_USED_ELEMENT_ATTRIBUTES": ("#909090", None, None),
})
COMMON.pop("MATCHED_BRACE_ATTRIBUTES", None)   # emitted below with a box effect
for lvl, c in dict(ERROR="#F14C4C", WARNING="#FFA618", INFO="#50E191", DEBUG="#00D2FA", VERBOSE="#909090").items():
    COMMON[f"LOG_{lvl}_OUTPUT"] = (c, None, None)

EFFECTS = {"ERRORS_ATTRIBUTES": "#F14C4C", "WARNING_ATTRIBUTES": "#CCA700",
           "WEAK_WARNING_ATTRIBUTES": "#909090", "INFO_ATTRIBUTES": "#3794FF",
           "DEPRECATED_ATTRIBUTES": "#909090", "MARKED_FOR_REMOVAL_ATTRIBUTES": "#F14C4C"}
COLORS = {
    "GUTTER_BACKGROUND": BG,
    "ADDED_LINES_COLOR": "#59CC8A", "MODIFIED_LINES_COLOR": "#006BCD",
    "DELETED_LINES_COLOR": "#FF8330", "WHITESPACES_MODIFIED_LINES_COLOR": "#006BCD",
    "IGNORED_ADDED_LINES_BORDER_COLOR": "#59CC8A", "IGNORED_MODIFIED_LINES_BORDER_COLOR": "#006BCD",
    "IGNORED_DELETED_LINES_BORDER_COLOR": "#FF8330",
    "FILESTATUS_ADDED": "#59CC8A", "FILESTATUS_MODIFIED": "#4FA3E6",
    "FILESTATUS_DELETED": "#FF8330", "FILESTATUS_UNKNOWN": "#5ACD88",
    "FILESTATUS_IDEA_FILESTATUS_IGNORED": "#898076", "FILESTATUS_MERGED": "#B669C7",
    "FILESTATUS_NOT_CHANGED_IMMEDIATE": "#00D2FA", "FILESTATUS_NOT_CHANGED_RECURSIVE": "#00D2FA",
    "ANNOTATIONS_COLOR": "#909090", "VCS_ANNOTATIONS_COLOR_1": "#1A1B1B",
    "ERROR_STRIPE_COLOR": "#F14C4C",
}
# same as Modern Cyan: #38AD454d / #FF6B2B4d blended on #0C0C0C
DIFF = {"DIFF_INSERTED": ("#173D1D", "#59CC8A"), "DIFF_DELETED": ("#57291A", "#FF8330"),
        "DIFF_MODIFIED": ("#0A2638", "#006BCD"), "DIFF_CONFLICT": ("#3D2A0B", "#FFA618")}

_ns.update(COMMON=COMMON, EFFECTS=EFFECTS, COLORS=COLORS, DIFF=DIFF)
extra_colors_xml = _ns["extra_colors_xml"]
_base_attrs_xml = _ns["extra_attrs_xml"]

def extra_attrs_xml(existing):
    out = _base_attrs_xml(existing)
    # DartPad: matching bracket text #FF2D64 with a 1px #606060 outline (BOXED).
    out.append('    <option name="MATCHED_BRACE_ATTRIBUTES">\n      <value>\n'
               '        <option name="FOREGROUND" value="FF2D64"/>\n'
               '        <option name="EFFECT_COLOR" value="606060"/>\n'
               '        <option name="EFFECT_TYPE" value="0"/>\n'
               '      </value>\n    </option>')
    return out

# Semantic tokens override the textmate-derived DEFAULT_* values.
FORCE = {}
for k, c in dict(CLASS_NAME=TYPE, INTERFACE_NAME=TYPE, CLASS_REFERENCE=TYPE,
                 LOCAL_VARIABLE=CY, PARAMETER=CY, REASSIGNED_LOCAL_VARIABLE=CY,
                 REASSIGNED_PARAMETER=CY, OPERATION_SIGN="#FFFFFF", FUNCTION_CALL=CY,
                 FUNCTION_DECLARATION=CY, INSTANCE_METHOD=CY, STATIC_METHOD=CY,
                 INSTANCE_FIELD=CY, STATIC_FIELD=CY, GLOBAL_VARIABLE=CY,
                 CONSTANT=TYPE, ANNOTATION_NAME=META, METADATA=META,
                 IDENTIFIER=CY, KEYWORD=KW, STRING=STR, NUMBER=NUM,
                 COMMENT=COM, LINE_COMMENT=COM, BLOCK_COMMENT=COM,
                 DOC_COMMENT=COM).items():
    FORCE["DEFAULT_" + k] = (c, None, None)
    FORCE[k] = (c, None, None)
COMMON.update(FORCE)

_ns["apply_real_keys"](COMMON, P, italic=0, named_label=CY, bg=BG,
                       logcat=dict(VERBOSE="#909090", DEBUG="#00D2FA", INFO="#50E191",
                                   WARNING="#FFA618", ERROR="#F14C4C", ASSERT="#FF00FA"))

# apply_real_keys pins a few Dart keys to generic palette slots; re-pin the
# ones that DartPad colours differently. Every Dart identifier key is cyan.
for k in ("DART_INSTANCE_METHOD_DECLARATION", "DART_INSTANCE_METHOD_REFERENCE",
          "DART_INSTANCE_METHOD_TEAR_OFF", "DART_STATIC_METHOD_DECLARATION",
          "DART_STATIC_METHOD_REFERENCE", "DART_STATIC_METHOD_TEAR_OFF",
          "DART_TOP_LEVEL_FUNCTION_DECLARATION", "DART_TOP_LEVEL_FUNCTION_REFERENCE",
          "DART_TOP_LEVEL_FUNCTION_TEAR_OFF", "DART_LOCAL_FUNCTION_DECLARATION",
          "DART_LOCAL_FUNCTION_REFERENCE", "DART_LOCAL_FUNCTION_TEAR_OFF",
          "DART_INSTANCE_FIELD_DECLARATION", "DART_INSTANCE_FIELD_REFERENCE",
          "DART_INSTANCE_GETTER_DECLARATION", "DART_INSTANCE_GETTER_REFERENCE",
          "DART_INSTANCE_SETTER_DECLARATION", "DART_INSTANCE_SETTER_REFERENCE",
          "DART_STATIC_FIELD_DECLARATION", "DART_STATIC_GETTER_DECLARATION",
          "DART_STATIC_GETTER_REFERENCE", "DART_STATIC_SETTER_DECLARATION",
          "DART_STATIC_SETTER_REFERENCE", "DART_TOP_LEVEL_VARIABLE_DECLARATION",
          "DART_TOP_LEVEL_GETTER_DECLARATION", "DART_TOP_LEVEL_GETTER_REFERENCE",
          "DART_TOP_LEVEL_SETTER_DECLARATION", "DART_TOP_LEVEL_SETTER_REFERENCE",
          "DART_LOCAL_VARIABLE_DECLARATION", "DART_LOCAL_VARIABLE_REFERENCE",
          "DART_DYNAMIC_LOCAL_VARIABLE_DECLARATION", "DART_DYNAMIC_LOCAL_VARIABLE_REFERENCE",
          "DART_PARAMETER_DECLARATION", "DART_PARAMETER_REFERENCE",
          "DART_DYNAMIC_PARAMETER_DECLARATION", "DART_DYNAMIC_PARAMETER_REFERENCE",
          "DART_UNRESOLVED_INSTANCE_MEMBER_REFERENCE", "DART_IDENTIFIER"):
    COMMON[k] = (CY, None, None)
for k in ("DART_CLASS", "DART_EXTENSION", "DART_EXTENSION_TYPE", "DART_MIXIN",
          "DART_TYPE_ALIAS", "DART_FUNCTION_TYPE_ALIAS", "DART_TYPE_PARAMETER",
          "DART_CONSTRUCTOR", "DART_CONSTRUCTOR_TEAR_OFF", "DART_TYPE_NAME_DYNAMIC", "DART_ENUM"):
    COMMON[k] = (TYPE, None, None)
for k in ("DART_FAT_ARROW", "DART_OPERATION_SIGN", "DART_COLON", "DART_COMMA", "DART_DOT",
          "DART_SEMICOLON", "DART_BRACES", "DART_BRACKETS", "DART_PARENTH"):
    COMMON[k] = ("#FFFFFF", None, None)
