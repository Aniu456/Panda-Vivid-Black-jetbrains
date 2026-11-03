"""Panda Vivid Black: explicit JetBrains / Android Studio attribute keys.

convert.py only maps generic DEFAULT_* keys from TextMate scopes. Language
plugins (Kotlin, Dart, XML, Groovy, JSON, Logcat, diff/VCS) use their own keys,
so we pin them here to the VS Code panda-vivid-black palette (semanticTokenColors
first, then the language-specific tokenColors rules).
"""
P = dict(
    kw="#FF4F9D", fn="#4FB6FF", type="#19F9D8", enum="#FFA850", var="#E6E6E6",
    param="#FF8A3D", prop="#00CFFF", str="#19F9D8", num="#A970FF", regexp="#FF3B5C",
    op="#E6E6E6", comment="#898DA5", const="#FF619E", esc="#FF2D8D", tag="#FF2D8D",
    attr="#FFA647", orange="#FFAF59", storage="#FFA647", deco="#40ADFF",
    dart_anno="#00CFFF", doc_tag="#FFE172", doc_val="#FF7CCB", purple="#9C5CF2",
    err="#FF3B5C", warn="#FFD24A", gray="#757575", ignored="#969696",
    added="#19F9D8", modified="#FFCC95", deleted="#FF4B82",
)
I, B, N = 2, 1, 0  # FONT_TYPE: italic, bold, plain

# key -> (fg, bg, font_type)
COMMON = {
    # general fallbacks convert.py doesn't emit
    "DEFAULT_IDENTIFIER": (P["var"], None, None),
    "DEFAULT_STATIC_FIELD": (P["const"], None, None),
    "DEFAULT_INSTANCE_METHOD": (P["fn"], None, None),
    "DEFAULT_CLASS_REFERENCE": (P["type"], None, I),
    "DEFAULT_REASSIGNED_LOCAL_VARIABLE": (P["var"], None, None),
    "DEFAULT_REASSIGNED_PARAMETER": (P["param"], None, I),
    "DEFAULT_LABEL": (P["kw"], None, None),
    "DEFAULT_METADATA": (P["deco"], None, None),
    "DEFAULT_DOC_COMMENT_TAG": (P["doc_tag"], None, None),
    "DEFAULT_DOC_COMMENT_TAG_VALUE": (P["doc_val"], None, None),
    "DEFAULT_DOC_MARKUP": (P["comment"], None, I),
    "DEFAULT_INVALID_STRING_ESCAPE": (P["err"], None, None),
    "DEFAULT_ENTITY": (P["const"], None, None),
    "DEFAULT_TAG": (P["tag"], None, None),
    "DEFAULT_ATTRIBUTE": (P["attr"], None, None),
    "DEFAULT_BRACES": (P["var"], None, None), "DEFAULT_BRACKETS": (P["var"], None, None),
    "DEFAULT_PARENTHS": (P["var"], None, None), "DEFAULT_COMMA": (P["var"], None, None),
    "DEFAULT_DOT": (P["var"], None, None), "DEFAULT_SEMICOLON": (P["var"], None, None),
    # Java
    "ENUM_CONST": (P["enum"], None, None),
    "STATIC_FINAL_FIELD_ATTRIBUTES": (P["const"], None, None),
    "STATIC_FIELD_ATTRIBUTES": (P["const"], None, None),
    "INSTANCE_FIELD_ATTRIBUTES": (P["prop"], None, None),
    "JAVA_KEYWORD": (P["kw"], None, None), "JAVA_STRING": (P["str"], None, None),
    "JAVA_NUMBER": (P["num"], None, None), "JAVA_LINE_COMMENT": (P["comment"], None, I),
    "ANNOTATION_NAME_ATTRIBUTES": (P["storage"], None, None),
    "ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES": (P["param"], None, I),
    "METHOD_CALL_ATTRIBUTES": (P["fn"], None, None),
    "METHOD_DECLARATION_ATTRIBUTES": (P["fn"], None, None),
    "STATIC_METHOD_ATTRIBUTES": (P["fn"], None, I),
    "CONSTRUCTOR_CALL_ATTRIBUTES": (P["type"], None, I),
    "CONSTRUCTOR_DECLARATION_ATTRIBUTES": (P["fn"], None, None),
    "CLASS_NAME_ATTRIBUTES": (P["type"], None, I),
    "INTERFACE_NAME_ATTRIBUTES": (P["type"], None, I),
    "ENUM_NAME_ATTRIBUTES": (P["enum"], None, None),
    "TYPE_PARAMETER_NAME_ATTRIBUTES": (P["type"], None, I),
    "ABSTRACT_CLASS_NAME_ATTRIBUTES": (P["type"], None, I),
    "PARAMETER_ATTRIBUTES": (P["param"], None, I),
    "LOCAL_VARIABLE_ATTRIBUTES": (P["var"], None, None),
    "IMPLICIT_ANONYMOUS_CLASS_PARAMETER_ATTRIBUTES": (P["param"], None, I),
    # Kotlin — VS Code Kotlin grammar has no dedicated rules, so generic
    # textmate: annotations = storage.type.annotation -> orange #FFA647,
    # this/super = variable.language -> #FF619E, properties #00CFFF.
    "KOTLIN_KEYWORD": (P["kw"], None, None), "KOTLIN_BUILTIN_ANNOTATION": (P["kw"], None, None),
    "KOTLIN_SOFT_KEYWORD": (P["kw"], None, None), "KOTLIN_MODIFIER": (P["kw"], None, None),
    "KOTLIN_ANNOTATION": (P["storage"], None, None),
    "KOTLIN_ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES": (P["param"], None, I),
    "KOTLIN_STRING": (P["str"], None, None), "KOTLIN_NUMBER": (P["num"], None, None),
    "KOTLIN_STRING_ESCAPE": (P["esc"], None, None),
    "KOTLIN_INVALID_STRING_ESCAPE": (P["err"], None, None),
    "KOTLIN_STRING_TEMPLATE_ENTRY": (P["orange"], None, None),  # punctuation.definition.template-expression
    "KOTLIN_CLOSURE_DEFAULT_PARAMETER": (P["param"], None, I),  # `it`
    "KOTLIN_LABEL": (P["kw"], None, None),
    "KOTLIN_CLASS": (P["type"], None, I), "KOTLIN_ABSTRACT_CLASS": (P["type"], None, I),
    "KOTLIN_TRAIT": (P["type"], None, I), "KOTLIN_OBJECT": (P["type"], None, I),
    "KOTLIN_ENUM": (P["enum"], None, None), "KOTLIN_ENUM_ENTRY": (P["enum"], None, None),
    "KOTLIN_TYPE_ALIAS": (P["type"], None, I), "KOTLIN_TYPE_PARAMETER": (P["type"], None, I),
    "KOTLIN_DATA_CLASS": (P["type"], None, I), "KOTLIN_DATA_OBJECT": (P["type"], None, I),
    "KOTLIN_FUNCTION_DECLARATION": (P["fn"], None, None),
    "KOTLIN_FUNCTION_CALL": (P["fn"], None, None),
    "KOTLIN_PACKAGE_FUNCTION_CALL": (P["fn"], None, None),
    "KOTLIN_EXTENSION_FUNCTION_CALL": (P["fn"], None, I),
    "KOTLIN_CONSTRUCTOR": (P["type"], None, I),
    "KOTLIN_DYNAMIC_FUNCTION_CALL": (P["fn"], None, I),
    "KOTLIN_SUSPEND_FUNCTION_CALL": (P["fn"], None, I),
    "KOTLIN_VARIABLE_AS_FUNCTION_CALL": (P["fn"], None, None),
    "KOTLIN_VARIABLE_AS_FUNCTION_LIKE_CALL": (P["fn"], None, None),
    "KOTLIN_PARAMETER": (P["param"], None, I),
    "KOTLIN_NAMED_ARGUMENT": (P["param"], None, I),
    "KOTLIN_LOCAL_VARIABLE": (P["var"], None, None),
    "KOTLIN_MUTABLE_VARIABLE": (P["var"], None, None),  # no underline, like VS Code
    "KOTLIN_INSTANCE_PROPERTY": (P["prop"], None, None),
    "KOTLIN_INSTANCE_PROPERTY_CUSTOM_PROPERTY_DECLARATION": (P["prop"], None, None),
    "KOTLIN_PACKAGE_PROPERTY": (P["const"], None, None),
    "KOTLIN_PACKAGE_PROPERTY_CUSTOM_PROPERTY_DECLARATION": (P["const"], None, None),
    "KOTLIN_EXTENSION_PROPERTY": (P["prop"], None, I),
    "KOTLIN_SYNTHETIC_EXTENSION_PROPERTY": (P["prop"], None, I),
    "KOTLIN_BACKING_FIELD_VARIABLE": (P["prop"], None, I),  # `field`
    "KOTLIN_WRAPPED_INTO_REF": (P["var"], None, None),
    "KOTLIN_SMART_CAST_VALUE": (P["var"], "#12302C", None),
    "KOTLIN_SMART_CAST_RECEIVER": (P["var"], "#12302C", None),
    "KOTLIN_SMART_CONSTANT": (P["num"], "#12302C", None),
    "KOTLIN_DSL_ANNOTATION1": (P["fn"], None, None), "KOTLIN_DSL_ANNOTATION2": (P["purple"], None, None),
    "KOTLIN_DSL_ANNOTATION3": (P["orange"], None, None), "KOTLIN_DSL_ANNOTATION4": (P["kw"], None, None),
    # Dart / Flutter — VS Code rules: storage.modifier/primitive.dart pink,
    # storage.type.annotation.dart cyan #00CFFF, variable.language.dart pink.
    "DART_KEYWORD": (P["kw"], None, None), "DART_BUILTIN": (P["kw"], None, None),
    "DART_ANNOTATION": (P["dart_anno"], None, None),
    "DART_STRING": (P["str"], None, None), "DART_NUMBER": (P["num"], None, None),
    "DART_VALID_STRING_ESCAPE": (P["esc"], None, None),
    "DART_INVALID_STRING_ESCAPE": (P["err"], None, None),
    "DART_SYMBOL_LITERAL": (P["str"], None, None),
    "DART_LINE_COMMENT": (P["comment"], None, I), "DART_BLOCK_COMMENT": (P["comment"], None, I),
    "DART_DOC_COMMENT": (P["comment"], None, N),  # comment.block.documentation: normal
    "DART_CLASS": (P["type"], None, I), "DART_EXTENSION": (P["type"], None, I),
    "DART_MIXIN": (P["type"], None, I), "DART_TYPE_ALIAS": (P["type"], None, I),
    "DART_TYPE_PARAMETER": (P["type"], None, I),
    "DART_TYPE_NAME_DYNAMIC": (P["kw"], None, None),  # dynamic is a keyword-ish primitive (pink)
    "DART_ENUM": (P["enum"], None, None), "DART_ENUM_CONSTANT": (P["enum"], None, None),
    "DART_CONSTRUCTOR": (P["type"], None, I),
    "DART_FUNCTION_TYPE_ALIAS": (P["type"], None, I),
    "DART_IMPORT_PREFIX": (P["var"], None, None), "DART_LIBRARY_NAME": (P["var"], None, None),
    "DART_LABEL": (P["kw"], None, None),
    "DART_INSTANCE_MEMBER_FUNCTION": (P["fn"], None, None),
    "DART_INSTANCE_MEMBER_FUNCTION_DECLARATION": (P["fn"], None, None),
    "DART_STATIC_MEMBER_FUNCTION": (P["fn"], None, None),
    "DART_STATIC_MEMBER_FUNCTION_DECLARATION": (P["fn"], None, None),
    "DART_TOP_LEVEL_FUNCTION_DECLARATION": (P["fn"], None, None),
    "DART_TOP_LEVEL_FUNCTION_REFERENCE": (P["fn"], None, None),
    "DART_LOCAL_FUNCTION_DECLARATION": (P["fn"], None, None),
    "DART_LOCAL_FUNCTION_REFERENCE": (P["fn"], None, None),
    "DART_INSTANCE_MEMBER_FUNCTION_REFERENCE": (P["fn"], None, None),
    "DART_STATIC_MEMBER_FUNCTION_REFERENCE": (P["fn"], None, None),
    "DART_INSTANCE_FIELD_DECLARATION": (P["prop"], None, None),
    "DART_INSTANCE_FIELD_REFERENCE": (P["prop"], None, None),
    "DART_INSTANCE_GETTER_DECLARATION": (P["prop"], None, None),
    "DART_INSTANCE_GETTER_REFERENCE": (P["prop"], None, None),
    "DART_INSTANCE_SETTER_DECLARATION": (P["prop"], None, None),
    "DART_INSTANCE_SETTER_REFERENCE": (P["prop"], None, None),
    "DART_STATIC_FIELD_DECLARATION": (P["const"], None, None),
    "DART_STATIC_GETTER_DECLARATION": (P["const"], None, None),
    "DART_STATIC_GETTER_REFERENCE": (P["const"], None, None),
    "DART_STATIC_SETTER_DECLARATION": (P["const"], None, None),
    "DART_STATIC_SETTER_REFERENCE": (P["const"], None, None),
    "DART_TOP_LEVEL_VARIABLE_DECLARATION": (P["const"], None, None),
    "DART_TOP_LEVEL_GETTER_DECLARATION": (P["const"], None, None),
    "DART_TOP_LEVEL_GETTER_REFERENCE": (P["const"], None, None),
    "DART_TOP_LEVEL_SETTER_DECLARATION": (P["const"], None, None),
    "DART_TOP_LEVEL_SETTER_REFERENCE": (P["const"], None, None),
    "DART_LOCAL_VARIABLE": (P["var"], None, None),
    "DART_LOCAL_VARIABLE_DECLARATION": (P["var"], None, None),
    "DART_PARAMETER_DECLARATION": (P["param"], None, I),
    "DART_PARAMETER_REFERENCE": (P["param"], None, I),
    "DART_NAMED_PARAMETER": (P["param"], None, I),
    "DART_DYNAMIC_LOCAL_VARIABLE_DECLARATION": (P["var"], None, None),
    "DART_DYNAMIC_LOCAL_VARIABLE_REFERENCE": (P["var"], None, None),
    "DART_DYNAMIC_PARAMETER_DECLARATION": (P["param"], None, I),
    "DART_DYNAMIC_PARAMETER_REFERENCE": (P["param"], None, I),
    "DART_OPERATION_SIGN": (P["op"], None, None),
    # XML / Android layouts & manifest
    "XML_TAG": (P["var"], None, None), "XML_TAG_NAME": (P["tag"], None, None),
    "XML_CUSTOM_TAG_NAME": (P["tag"], None, I), "XML_NS_PREFIX": (P["purple"], None, None),
    "XML_ATTRIBUTE_NAME": (P["attr"], None, None), "XML_ATTRIBUTE_VALUE": (P["str"], None, None),
    "XML_ENTITY_REFERENCE": (P["const"], None, None), "XML_PROLOGUE": (P["gray"], None, None),
    "XML_TAG_DATA": (P["var"], None, None),
    "HTML_TAG_NAME": (P["tag"], None, None), "HTML_ATTRIBUTE_NAME": (P["attr"], None, None),
    "HTML_ATTRIBUTE_VALUE": (P["str"], None, None),
    # Groovy / Gradle
    "Groovy method declaration": (P["fn"], None, None),
    "Groovy var": (P["var"], None, None), "Groovy parameter": (P["param"], None, I),
    "Instance property reference ID": (P["prop"], None, None),
    "Static property reference ID": (P["const"], None, None),
    "Method call": (P["fn"], None, None), "Static method access": (P["fn"], None, I),
    "Annotation": (P["storage"], None, None), "List/map to object conversion": (P["type"], None, I),
    "Groovy constructor call": (P["type"], None, I),
    "Unresolved reference access": (P["var"], None, None),
    "GROOVY_KEYWORD": (P["kw"], None, None),
    # JSON / YAML / properties / TOML (libs.versions.toml)
    "JSON_PROPERTY_KEY": (P["prop"], None, None), "JSON_STRING": (P["str"], None, None),
    "JSON_NUMBER": (P["num"], None, None), "JSON_KEYWORD": (P["num"], None, None),
    "YAML_SCALAR_KEY": (P["orange"], None, None), "YAML_SCALAR_VALUE": (P["str"], None, None),
    "PROPERTIES.KEY": (P["prop"], None, None), "PROPERTIES.VALUE": (P["str"], None, None),
    "org.toml.KEY": (P["prop"], None, None), "org.toml.STRING": (P["str"], None, None),
    # Console / terminal ANSI (VS Code terminal.ansi*)
    "CONSOLE_NORMAL_OUTPUT": ("#E6E6E6", None, None), "CONSOLE_ERROR_OUTPUT": ("#FF2D8D", None, None),
    "CONSOLE_SYSTEM_OUTPUT": ("#757575", None, None), "CONSOLE_USER_INPUT": ("#19F9D8", None, I),
    "CONSOLE_BLACK_OUTPUT": ("#24242E", None, None), "CONSOLE_RED_OUTPUT": ("#FF2D8D", None, None),
    "CONSOLE_GREEN_OUTPUT": ("#19F9D8", None, None), "CONSOLE_YELLOW_OUTPUT": ("#FFB86C", None, None),
    "CONSOLE_BLUE_OUTPUT": ("#45A9F9", None, None), "CONSOLE_MAGENTA_OUTPUT": ("#FF75B5", None, None),
    "CONSOLE_CYAN_OUTPUT": ("#B084EB", None, None), "CONSOLE_GRAY_OUTPUT": ("#CDCDCD", None, None),
    "CONSOLE_DARKGRAY_OUTPUT": ("#757575", None, None),
    "LOG_ERROR_OUTPUT": ("#FF3B5C", None, None), "LOG_WARNING_OUTPUT": ("#FFD24A", None, None),
    "LOG_INFO_OUTPUT": ("#19F9D8", None, None), "LOG_DEBUG_OUTPUT": ("#4FB6FF", None, None),
    "LOG_VERBOSE_OUTPUT": ("#898DA5", None, None),
    # Android Studio Logcat (classic + new Logcat level keys)
    "LOGCAT_VERBOSE_OUTPUT": ("#898DA5", None, None), "LOGCAT_DEBUG_OUTPUT": ("#4FB6FF", None, None),
    "LOGCAT_INFO_OUTPUT": ("#19F9D8", None, None), "LOGCAT_WARNING_OUTPUT": ("#FFD24A", None, None),
    "LOGCAT_ERROR_OUTPUT": ("#FF3B5C", None, None), "LOGCAT_ASSERT_OUTPUT": ("#FF4F9D", None, B),
    "LOGCAT_LEVEL_VERBOSE_KEY": ("#0B0B0E", "#898DA5", None), "LOGCAT_LEVEL_DEBUG_KEY": ("#0B0B0E", "#4FB6FF", None),
    "LOGCAT_LEVEL_INFO_KEY": ("#0B0B0E", "#19F9D8", None), "LOGCAT_LEVEL_WARNING_KEY": ("#0B0B0E", "#FFD24A", None),
    "LOGCAT_LEVEL_ERROR_KEY": ("#0B0B0E", "#FF3B5C", None), "LOGCAT_LEVEL_ASSERT_KEY": ("#0B0B0E", "#FF4F9D", None),
    "LOGCAT_MESSAGE_VERBOSE_KEY": ("#898DA5", None, None), "LOGCAT_MESSAGE_DEBUG_KEY": ("#4FB6FF", None, None),
    "LOGCAT_MESSAGE_INFO_KEY": ("#19F9D8", None, None), "LOGCAT_MESSAGE_WARNING_KEY": ("#FFD24A", None, None),
    "LOGCAT_MESSAGE_ERROR_KEY": ("#FF3B5C", None, None), "LOGCAT_MESSAGE_ASSERT_KEY": ("#FF4F9D", None, None),
    # Search / matches / errors (blended VS Code alpha colors onto #0B0B0E)
    "TEXT_SEARCH_RESULT_ATTRIBUTES": (None, "#5F3A26", None),
    "SEARCH_RESULT_ATTRIBUTES": (None, "#5F3A26", None),
    "IDENTIFIER_UNDER_CARET_ATTRIBUTES": (None, "#0A3240", None),
    "WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES": (None, "#3A1A30", None),
    "MATCHED_BRACE_ATTRIBUTES": (None, "#30224A", B),
    "UNMATCHED_BRACE_ATTRIBUTES": (P["err"], None, B),
    "HYPERLINK_ATTRIBUTES": (P["deco"], None, None),
    "TODO_DEFAULT_ATTRIBUTES": (P["warn"], None, B | I),
    "DEPRECATED_ATTRIBUTES": (None, None, None),
    "NOT_USED_ELEMENT_ATTRIBUTES": (P["gray"], None, None),
    "WRONG_REFERENCES_ATTRIBUTES": (P["err"], None, None),
}

# Effect (waved underline) error/warning attrs: key -> effect color
EFFECTS = {"ERRORS_ATTRIBUTES": P["err"], "WARNING_ATTRIBUTES": P["warn"],
           "WEAK_WARNING_ATTRIBUTES": "#898DA5", "INFO_ATTRIBUTES": P["fn"],
           "DEPRECATED_ATTRIBUTES": "#FF2D8D", "MARKED_FOR_REMOVAL_ATTRIBUTES": "#FF2D8D"}

# <colors> section: diff, VCS gutter, file status
COLORS = {
    "ADDED_LINES_COLOR": "#19F9D8", "MODIFIED_LINES_COLOR": "#FFCC95",
    "DELETED_LINES_COLOR": "#FF4B82", "WHITESPACES_MODIFIED_LINES_COLOR": "#FFCC95",
    "IGNORED_ADDED_LINES_BORDER_COLOR": "#19F9D8", "IGNORED_MODIFIED_LINES_BORDER_COLOR": "#FFCC95",
    "IGNORED_DELETED_LINES_BORDER_COLOR": "#FF4B82",
    "FILESTATUS_ADDED": "#19F9D8", "FILESTATUS_MODIFIED": "#FFCC95",
    "FILESTATUS_DELETED": "#FF4B82", "FILESTATUS_UNKNOWN": "#FF7CCB",
    "FILESTATUS_IDEA_FILESTATUS_IGNORED": "#969696", "FILESTATUS_MERGED": "#9C5CF2",
    "FILESTATUS_NOT_CHANGED_IMMEDIATE": "#4FB6FF", "FILESTATUS_NOT_CHANGED_RECURSIVE": "#4FB6FF",
    "ANNOTATIONS_COLOR": "#898DA5", "VCS_ANNOTATIONS_COLOR_1": "#1A1F24",
    "ERROR_STRIPE_COLOR": "#FF3B5C",
}
# Diff backgrounds: VS Code #87994A26 / #FF4B8226 blended on #0B0B0E
DIFF = {"DIFF_INSERTED": ("#1D2116", "#87994A"), "DIFF_DELETED": ("#2E1219", "#FF4B82"),
        "DIFF_MODIFIED": ("#14232E", "#45A9F9"), "DIFF_CONFLICT": ("#2E2414", "#FFB86C")}


def _hex(c):
    return c.lstrip("#").upper()


def extra_colors_xml():
    return [f'    <option name="{k}" value="{_hex(v)}"/>' for k, v in COLORS.items()]


def extra_attrs_xml(existing):
    out = []
    def emit(k, opts):
        inner = "\n".join(f'        <option name="{n}" value="{v}"/>' for n, v in opts)
        out.append(f'    <option name="{k}">\n      <value>\n{inner}\n      </value>\n    </option>')
    for k, (fg, bg, ft) in COMMON.items():
        if k in existing or k in EFFECTS:
            continue
        opts = []
        if fg: opts.append(("FOREGROUND", _hex(fg)))
        if bg: opts.append(("BACKGROUND", _hex(bg)))
        if ft is not None: opts.append(("FONT_TYPE", str(ft)))
        emit(k, opts)
    for k, c in EFFECTS.items():
        opts = [("EFFECT_COLOR", _hex(c)), ("ERROR_STRIPE_COLOR", _hex(c)),
                ("EFFECT_TYPE", "3" if k in ("DEPRECATED_ATTRIBUTES", "MARKED_FOR_REMOVAL_ATTRIBUTES") else "2")]
        emit(k, opts)
    for k, (bg, stripe) in DIFF.items():
        emit(k, [("BACKGROUND", _hex(bg)), ("ERROR_STRIPE_COLOR", _hex(stripe))])
    return out


# ---------------------------------------------------------------------------
# 1.2.1: key names verified against the installed Android Studio 2026.2 jars
# (Dart-510.0.0.jar DartSyntaxHighlighterColors, kotlin-plugin-shared.jar
# KotlinHighlightingColors, android.jar colorSchemes/LogcatColorSchemeDarcula.xml).
# Drop invented keys, add the real ones.
FAKE_KEYS = {
    "KOTLIN_SOFT_KEYWORD", "KOTLIN_MODIFIER", "KOTLIN_STRING_TEMPLATE_ENTRY",
    "KOTLIN_VARIABLE_AS_FUNCTION_CALL", "KOTLIN_VARIABLE_AS_FUNCTION_LIKE_CALL",
    "KOTLIN_DSL_ANNOTATION1", "KOTLIN_DSL_ANNOTATION2", "KOTLIN_DSL_ANNOTATION3", "KOTLIN_DSL_ANNOTATION4",
    "DART_BUILTIN", "DART_LOCAL_VARIABLE", "DART_NAMED_PARAMETER",
    "DART_INSTANCE_MEMBER_FUNCTION", "DART_INSTANCE_MEMBER_FUNCTION_DECLARATION",
    "DART_INSTANCE_MEMBER_FUNCTION_REFERENCE", "DART_STATIC_MEMBER_FUNCTION",
    "DART_STATIC_MEMBER_FUNCTION_DECLARATION", "DART_STATIC_MEMBER_FUNCTION_REFERENCE",
    "DART_OPERATION_SIGN_X",
} | {f"LOGCAT_{l}_OUTPUT" for l in ("VERBOSE", "DEBUG", "INFO", "WARNING", "ERROR", "ASSERT")} \
  | {f"LOGCAT_{k}_{l}_KEY" for k in ("LEVEL", "MESSAGE") for l in ("VERBOSE", "DEBUG", "INFO", "WARNING", "ERROR", "ASSERT")}


def apply_real_keys(common, P, italic=2, named_label=None, logcat=None, bg="#0B0B0E"):
    """named_label: colour for DART_PARAMETER_REFERENCE (the Dart analysis
    server tags named-argument labels `foo:` as PARAMETER_REFERENCE)."""
    I = italic
    for k in FAKE_KEYS:
        common.pop(k, None)
    fn, prop, var, typ, op = P["fn"], P["prop"], P["var"], P["type"], P["op"]
    common.update({
        # Dart methods / tear-offs (real names)
        "DART_INSTANCE_METHOD_DECLARATION": (fn, None, None),
        "DART_INSTANCE_METHOD_REFERENCE": (fn, None, None),
        "DART_INSTANCE_METHOD_TEAR_OFF": (fn, None, None),
        "DART_STATIC_METHOD_DECLARATION": (fn, None, None),
        "DART_STATIC_METHOD_REFERENCE": (fn, None, None),
        "DART_STATIC_METHOD_TEAR_OFF": (fn, None, None),
        "DART_TOP_LEVEL_FUNCTION_TEAR_OFF": (fn, None, None),
        "DART_LOCAL_FUNCTION_TEAR_OFF": (fn, None, None),
        "DART_CONSTRUCTOR_TEAR_OFF": (typ, None, I),
        "DART_EXTENSION_TYPE": (typ, None, I),
        # static / top-level getters & setters are semantic "property" in VS Code
        "DART_STATIC_FIELD_DECLARATION": (prop, None, None),
        "DART_STATIC_GETTER_DECLARATION": (prop, None, None),
        "DART_STATIC_GETTER_REFERENCE": (prop, None, None),   # WidgetsBinding.instance
        "DART_STATIC_SETTER_DECLARATION": (prop, None, None),
        "DART_STATIC_SETTER_REFERENCE": (prop, None, None),
        "DART_TOP_LEVEL_GETTER_DECLARATION": (prop, None, None),
        "DART_TOP_LEVEL_GETTER_REFERENCE": (prop, None, None),
        "DART_TOP_LEVEL_SETTER_DECLARATION": (prop, None, None),
        "DART_TOP_LEVEL_SETTER_REFERENCE": (prop, None, None),
        "DART_TOP_LEVEL_VARIABLE_DECLARATION": (var, None, None),
        "DART_LOCAL_VARIABLE_DECLARATION": (var, None, None),
        "DART_LOCAL_VARIABLE_REFERENCE": (var, None, None),
        "DART_UNRESOLVED_INSTANCE_MEMBER_REFERENCE": (var, None, None),
        "DART_IDENTIFIER": (var, None, None),
        "DART_PARAMETER_DECLARATION": (P["param"], None, I),
        "DART_PARAMETER_REFERENCE": (named_label or P["param"], None, I),
        "DART_FAT_ARROW": (op, None, None), "DART_OPERATION_SIGN": (op, None, None),
        "DART_COLON": (var, None, None), "DART_COMMA": (var, None, None), "DART_DOT": (var, None, None),
        "DART_SEMICOLON": (var, None, None), "DART_BRACES": (var, None, None),
        "DART_BRACKETS": (var, None, None), "DART_PARENTH": (var, None, None),
        # Kotlin real keys not covered before
        "KOTLIN_KEYWORD_VAL": (P["kw"], None, None), "KOTLIN_KEYWORD_VAR": (P["kw"], None, None),
        "KOTLIN_VARIABLE_AS_FUNCTION": (fn, None, None),
        "KOTLIN_VARIABLE_AS_FUNCTION_LIKE": (fn, None, None),
        "KOTLIN_DYNAMIC_PROPERTY_CALL": (prop, None, I),
        "KOTLIN_ANDROID_EXTENSIONS_PROPERTY_CALL": (prop, None, None),
        "KOTLIN_CONTEXT_ARGUMENT": (P["param"], None, I),
        "KOTLIN_LINE_COMMENT": (P["comment"], None, I), "KOTLIN_BLOCK_COMMENT": (P["comment"], None, I),
        "KOTLIN_DOC_COMMENT": (P["comment"], None, None),
        "KOTLIN_OPERATION_SIGN": (op, None, None), "KOTLIN_SAFE_ACCESS": (op, None, None),
        "KOTLIN_EXCLEXCL": (op, None, None), "KOTLIN_QUEST": (op, None, None),
        "KOTLIN_ARROW": (op, None, None), "KOTLIN_DOUBLE_COLON": (op, None, None),
        "KOTLIN_AMPERSAND": (op, None, None),
        "KOTLIN_FUNCTION_LITERAL_BRACES_AND_ARROW": (P["kw"], None, None),
        "KOTLIN_COLON": (var, None, None), "KOTLIN_COMMA": (var, None, None), "KOTLIN_DOT": (var, None, None),
        "KOTLIN_SEMICOLON": (var, None, None), "KOTLIN_BRACES": (var, None, None),
        "KOTLIN_BRACKETS": (var, None, None), "KOTLIN_PARENTHESIS": (var, None, None),
        # Logcat filter bar
        "LOGCAT_FILTER_KEY": (P["kw"], None, None), "LOGCAT_FILTER_KVALUE": (P["str"], None, None),
        "LOGCAT_FILTER_STRING_KVALUE": (P["str"], None, None),
        "LOGCAT_FILTER_REGEX_KVALUE": (P["regexp"], None, None),
    })
    for lvl, c in (logcat or {}).items():
        common[f"LOGCAT_V2_LEVEL_{lvl}"] = (bg, c, 1 if lvl == "ASSERT" else None)
        common[f"LOGCAT_V2_MESSAGE_{lvl}"] = (c, None, 1 if lvl == "ASSERT" else None)
    for k in [k for k, (f, b, t) in common.items() if t is not None and not I]:
        f, b, t = common[k]; common[k] = (f, b, t & ~2)


VIVID_LOGCAT = dict(VERBOSE="#898DA5", DEBUG="#4FB6FF", INFO="#19F9D8",
                    WARNING="#FFD24A", ERROR="#FF3B5C", ASSERT="#FF4F9D")
if P.get("_name") != "modern":
    apply_real_keys(COMMON, P, logcat=VIVID_LOGCAT)
