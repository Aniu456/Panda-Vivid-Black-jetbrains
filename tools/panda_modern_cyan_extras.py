"""Panda Modern Cyan: JetBrains / Android Studio attribute keys.

Reuses the key tables of panda_jetbrains_extras with the Modern Dark palette
(source of truth: vscode/panda-vivid-black/themes/panda-modern-cyan-color-theme.json,
semanticTokenColors first, then the last matching tokenColors rule).
Modern Dark uses no italics, so every italic is dropped.
"""
import re
from pathlib import Path

P = dict(
    _name="modern-cyan", kw="#FF804F", fn="#B084FF", type="#00C9B0", enum="#00C9B0", var="#E8E8E8",
    param="#E8E8E8", prop="#79B8FF", str="#7EE787", num="#AFCEA2", regexp="#9FCBFF",
    op="#FF804F", comment="#888888", const="#79B8FF", esc="#D8B65E", tag="#7EE787",
    attr="#96D2FF", orange="#3B90E6", storage="#FF804F", deco="#FFA618",
    dart_anno="#FFA618", doc_tag="#888888", doc_val="#888888", purple="#B669C7",
    err="#F14C4C", warn="#CCA700", gray="#7D756B", ignored="#898076",
    added="#59CC8A", modified="#006BCD", deleted="#FF8330",
)

_src = (Path(__file__).with_name("panda_jetbrains_extras.py")).read_text()
_src = re.sub(r"^P = dict\(.*?^\)\n", "P = _P\n", _src, count=1, flags=re.S | re.M)
_ns = {"_P": P}
exec(compile(_src, "panda_jetbrains_extras(modern)", "exec"), _ns)

def _noitalic(ft):
    if ft is None: return None
    return ft & ~2

COMMON = {k: (fg, bg, _noitalic(ft)) for k, (fg, bg, ft) in _ns["COMMON"].items()}
COMMON.update({
    # Kotlin vs Dart differences in Modern Dark
    "KOTLIN_ANNOTATION": (P["deco"], None, None),          # @Composable etc. (orange-gold, like Dart)
    "KOTLIN_NAMED_ARGUMENT": (P["prop"], None, None),      # mirrors Dart parameter.label blue
    "KOTLIN_STRING_TEMPLATE_ENTRY": ("#3B90E6", None, None),  # punctuation.definition.template-expression
    "KOTLIN_EXTENSION_FUNCTION_CALL": (P["fn"], None, None),
    "KOTLIN_SMART_CAST_VALUE": (P["var"], "#0E2A35", None),
    "KOTLIN_SMART_CAST_RECEIVER": (P["var"], "#0E2A35", None),
    "KOTLIN_SMART_CONSTANT": (P["num"], "#0E2A35", None),
    "KOTLIN_PACKAGE_PROPERTY": (P["const"], None, None),
    "KOTLIN_CLOSURE_DEFAULT_PARAMETER": (P["var"], None, None),
    "DART_NAMED_PARAMETER": (P["prop"], None, None),       # semantic parameter.label:dart
    "DART_TYPE_NAME_DYNAMIC": (P["type"], None, None),
    "DART_ANNOTATION": (P["dart_anno"], None, None),
    "DART_DOC_COMMENT": (P["comment"], None, None),
    "XML_NS_PREFIX": (P["purple"], None, None),
    "XML_TAG": (P["gray"], None, None),                    # punctuation.definition.tag #7D756B
    "DEFAULT_TAG": (P["tag"], None, None),
    # console ANSI: theme defines none -> VS Code built-in dark defaults
    "CONSOLE_NORMAL_OUTPUT": ("#EBE3DB", None, None), "CONSOLE_ERROR_OUTPUT": ("#F14C4C", None, None),
    "CONSOLE_SYSTEM_OUTPUT": ("#888888", None, None), "CONSOLE_USER_INPUT": ("#7EE787", None, None),
    "CONSOLE_BLACK_OUTPUT": ("#000000", None, None), "CONSOLE_RED_OUTPUT": ("#CD3131", None, None),
    "CONSOLE_GREEN_OUTPUT": ("#0DBC79", None, None), "CONSOLE_YELLOW_OUTPUT": ("#E5E510", None, None),
    "CONSOLE_BLUE_OUTPUT": ("#2472C8", None, None), "CONSOLE_MAGENTA_OUTPUT": ("#BC3FBC", None, None),
    "CONSOLE_CYAN_OUTPUT": ("#11A8CD", None, None), "CONSOLE_GRAY_OUTPUT": ("#E5E5E5", None, None),
    "CONSOLE_DARKGRAY_OUTPUT": ("#666666", None, None),
    # search / highlight: VS Code alpha colors blended on #0C0C0C
    "TEXT_SEARCH_RESULT_ATTRIBUTES": (None, "#063A4D", None),
    "SEARCH_RESULT_ATTRIBUTES": (None, "#063A4D", None),
    "IDENTIFIER_UNDER_CARET_ATTRIBUTES": (None, "#082731", None),
    "WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES": (None, "#0A3442", None),
    "MATCHED_BRACE_ATTRIBUTES": (None, "#07364B", 1),
    "TODO_DEFAULT_ATTRIBUTES": ("#FFA618", None, 1),
})
for lvl, c in dict(ERROR="#F14C4C", WARNING="#FFA618", INFO="#7EE787", DEBUG="#79B8FF", VERBOSE="#888888").items():
    COMMON[f"LOG_{lvl}_OUTPUT"] = (c, None, None)

EFFECTS = {"ERRORS_ATTRIBUTES": "#F14C4C", "WARNING_ATTRIBUTES": "#CCA700",
           "WEAK_WARNING_ATTRIBUTES": "#888888", "INFO_ATTRIBUTES": "#3794FF",
           "DEPRECATED_ATTRIBUTES": "#888888", "MARKED_FOR_REMOVAL_ATTRIBUTES": "#F14C4C"}
COLORS = {
    "ADDED_LINES_COLOR": "#59CC8A", "MODIFIED_LINES_COLOR": "#006BCD",
    "DELETED_LINES_COLOR": "#FF8330", "WHITESPACES_MODIFIED_LINES_COLOR": "#006BCD",
    "IGNORED_ADDED_LINES_BORDER_COLOR": "#59CC8A", "IGNORED_MODIFIED_LINES_BORDER_COLOR": "#006BCD",
    "IGNORED_DELETED_LINES_BORDER_COLOR": "#FF8330",
    "FILESTATUS_ADDED": "#59CC8A", "FILESTATUS_MODIFIED": "#4FA3E6",
    "FILESTATUS_DELETED": "#FF8330", "FILESTATUS_UNKNOWN": "#5ACD88",
    "FILESTATUS_IDEA_FILESTATUS_IGNORED": "#898076", "FILESTATUS_MERGED": "#B669C7",
    "FILESTATUS_NOT_CHANGED_IMMEDIATE": "#79B8FF", "FILESTATUS_NOT_CHANGED_RECURSIVE": "#79B8FF",
    "ANNOTATIONS_COLOR": "#888888", "VCS_ANNOTATIONS_COLOR_1": "#1A1B1B",
    "ERROR_STRIPE_COLOR": "#F14C4C",
}
# #38AD454d / #FF6B2B4d blended on #0C0C0C
DIFF = {"DIFF_INSERTED": ("#173D1D", "#59CC8A"), "DIFF_DELETED": ("#57291A", "#FF8330"),
        "DIFF_MODIFIED": ("#0A2638", "#006BCD"), "DIFF_CONFLICT": ("#3D2A0B", "#FFA618")}

_ns.update(COMMON=COMMON, EFFECTS=EFFECTS, COLORS=COLORS, DIFF=DIFF)
extra_colors_xml = _ns["extra_colors_xml"]
extra_attrs_xml = _ns["extra_attrs_xml"]

# Semantic tokens (what VS Code actually shows with semantic highlighting on)
# override the textmate-derived DEFAULT_* values produced by convert.py.
FORCE = {}
for k, c in dict(CLASS_NAME=P["type"], INTERFACE_NAME=P["type"], CLASS_REFERENCE=P["type"],
                 LOCAL_VARIABLE=P["var"], PARAMETER=P["param"], REASSIGNED_LOCAL_VARIABLE=P["var"],
                 REASSIGNED_PARAMETER=P["param"], OPERATION_SIGN=P["op"], FUNCTION_CALL=P["fn"],
                 FUNCTION_DECLARATION=P["fn"], INSTANCE_METHOD=P["fn"], STATIC_METHOD=P["fn"],
                 INSTANCE_FIELD=P["prop"], STATIC_FIELD=P["const"], GLOBAL_VARIABLE=P["const"],
                 CONSTANT=P["const"], ANNOTATION_NAME=P["deco"], METADATA=P["deco"],
                 IDENTIFIER=P["var"], KEYWORD=P["kw"], STRING=P["str"], NUMBER=P["num"],
                 COMMENT=P["comment"], LINE_COMMENT=P["comment"], BLOCK_COMMENT=P["comment"],
                 DOC_COMMENT=P["comment"]).items():
    FORCE["DEFAULT_" + k] = (c, None, None)
    FORCE[k] = (c, None, None)
COMMON.update(FORCE)

# 1.2.1: real Android Studio key names. Named-argument labels (`tag:`) are
# DART_PARAMETER_REFERENCE -> blue like VS Code's parameter.label:dart.
_ns["apply_real_keys"](COMMON, P, italic=0, named_label=P["prop"], bg="#0C0C0C",
                       logcat=dict(VERBOSE="#888888", DEBUG="#79B8FF", INFO="#7EE787",
                                   WARNING="#FFA618", ERROR="#F14C4C", ASSERT="#B669C7"))
