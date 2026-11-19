#!/usr/bin/env python3
"""Convert VSCode themes to IntelliJ IDEA theme format."""

import argparse
import json
import re
import importlib
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
VSCODE_DIR = ROOT_DIR / "vscode" / "glass-dracula" / "themes"
OUTPUT_DIR = (
    ROOT_DIR
    / "idea"
    / "glass-dracula-idea"
    / "src"
    / "main"
    / "resources"
    / "themes"
)

THEMES = [
    {
        "key": "dracula-glass",
        "vscode_file": "dracula-glass-color-theme.json",
        "name": "Glass Dracula",
        "id": "GlassDracula",
        "dark": True,
    },
    {
        "key": "dracula-glass-hsv",
        "vscode_file": "dracula-glass-hsv-color-theme.json",
        "name": "Glass Dracula HSV",
        "id": "GlassDraculaHSV",
        "dark": True,
    },
    {
        "key": "dracula-glass-vivid",
        "vscode_file": "dracula-glass-vivid-color-theme.json",
        "name": "Glass Dracula Vivid",
        "id": "GlassDraculaVivid",
        "dark": True,
    },
    {
        "key": "dracula-dark-vivid-black",
        "vscode_file": "dracula-dark-vivid-black-color-theme.json",
        "name": "Dracula Dark Vivid Black",
        "id": "DraculaDarkVividBlack",
        "dark": True,
        "preserve_source_contrast": True,
    },
    {
        "key": "dracula-light-vivid-white",
        "vscode_file": "dracula-light-vivid-white-color-theme.json",
        "name": "Dracula Light Vivid White",
        "id": "DraculaLightVividWhite",
        "dark": False,
    },
    {
        "key": "panda-vivid-black",
        "vscode_dir": ROOT_DIR / "vscode" / "panda-vivid-black" / "themes",
        "vscode_file": "panda-vivid-black-color-theme.json",
        "output_dir": ROOT_DIR / "idea" / "panda-vivid-black" / "src" / "main" / "resources" / "themes",
        "name": "Panda Vivid Black",
        "id": "PandaVividBlack",
        "dark": True,
        "preserve_source_contrast": True,
        "editor_font": "Operator Mono",
        "islands": True,
        "extras": "panda_jetbrains_extras",
    },
    {
        "key": "panda-modern-dark",
        "vscode_dir": ROOT_DIR / "vscode" / "panda-vivid-black" / "themes",
        "vscode_file": "panda-modern-dark-color-theme.json",
        "output_dir": ROOT_DIR / "idea" / "panda-vivid-black" / "src" / "main" / "resources" / "themes",
        "name": "Panda Modern Dark",
        "id": "PandaModernDark",
        "dark": True,
        "preserve_source_contrast": True,
        "editor_font": "Operator Mono",
        "islands": True,
        "extras": "panda_modern_dark_extras",
    },

    {
        "key": "panda-modern-cyan",
        "vscode_dir": ROOT_DIR / "vscode" / "panda-vivid-black" / "themes",
        "vscode_file": "panda-modern-cyan-color-theme.json",
        "output_dir": ROOT_DIR / "idea" / "panda-vivid-black" / "src" / "main" / "resources" / "themes",
        "name": "Panda Modern Cyan",
        "id": "PandaModernCyan",
        "dark": True,
        "preserve_source_contrast": True,
        "editor_font": "Operator Mono",
        "islands": True,
        "extras": "panda_modern_cyan_extras",
    },
    {
        "key": "panda-flutter-dark",
        "vscode_dir": ROOT_DIR / "vscode" / "panda-vivid-black" / "themes",
        "vscode_file": "panda-flutter-dark-color-theme.json",
        "output_dir": ROOT_DIR / "idea" / "panda-vivid-black" / "src" / "main" / "resources" / "themes",
        "name": "Panda Flutter Dark",
        "id": "PandaFlutterDark",
        "dark": True,
        "preserve_source_contrast": True,
        "editor_font": "Operator Mono",
        "islands": True,
        "extras": "panda_flutter_dark_extras",
    },
]

# VSCode token scope → IntelliJ attribute names
SCOPE_TO_ATTR = {
    "comment":                      ["DEFAULT_COMMENT", "DEFAULT_LINE_COMMENT", "DEFAULT_BLOCK_COMMENT"],
    "comment.block.documentation":  ["DEFAULT_DOC_COMMENT"],
    "punctuation.definition.comment": ["DEFAULT_DOC_COMMENT"],
    "keyword":                      ["DEFAULT_KEYWORD"],
    "keyword.control":              ["DEFAULT_KEYWORD"],
    "keyword.operator.new":         ["DEFAULT_KEYWORD"],
    "keyword.other.special-method": ["DEFAULT_KEYWORD"],
    "keyword.control.at-rule":      ["DEFAULT_KEYWORD"],
    "keyword.other.important":      ["DEFAULT_KEYWORD"],
    "storage":                      ["DEFAULT_KEYWORD"],
    "storage.type":                 ["DEFAULT_KEYWORD"],
    "storage.modifier":             ["DEFAULT_KEYWORD"],
    "keyword.operator":             ["DEFAULT_OPERATION_SIGN"],
    "keyword.operator.logical":     ["DEFAULT_OPERATION_SIGN"],
    "keyword.operator.comparison":  ["DEFAULT_OPERATION_SIGN"],
    "keyword.operator.misc":        ["DEFAULT_OPERATION_SIGN"],
    "keyword.operator.sigil":       ["DEFAULT_OPERATION_SIGN"],
    "punctuation.definition.template-expression": ["DEFAULT_OPERATION_SIGN"],
    "entity.other.attribute-name":  ["DEFAULT_ATTRIBUTE"],
    "entity.name.function":         ["DEFAULT_FUNCTION_DECLARATION"],
    "support.function":             ["DEFAULT_FUNCTION_CALL", "DEFAULT_STATIC_METHOD"],
    "entity.name.type.class":       ["DEFAULT_CLASS_NAME"],
    "entity.name.type":             ["DEFAULT_CLASS_NAME", "DEFAULT_INTERFACE_NAME"],
    "support.type":                 ["DEFAULT_CLASS_NAME"],
    "entity.name.type.interface":   ["DEFAULT_INTERFACE_NAME"],
    "entity.other.inherited-class": ["DEFAULT_CLASS_NAME"],
    "constant":                     ["DEFAULT_CONSTANT"],
    "entity.name.type.enum":        ["DEFAULT_CLASS_NAME"],
    "constant.numeric":             ["DEFAULT_NUMBER"],
    "constant.language.boolean":    ["DEFAULT_KEYWORD"],
    "constant.other.symbol":        ["DEFAULT_PREDEFINED_SYMBOL"],
    "string":                       ["DEFAULT_STRING"],
    "constant.character.escape":    ["DEFAULT_VALID_STRING_ESCAPE"],
    "string.regexp":                ["DEFAULT_REGEXP"],
    "string.other":                 ["DEFAULT_STRING"],
    "variable":                     ["DEFAULT_LOCAL_VARIABLE", "DEFAULT_GLOBAL_VARIABLE"],
    "variable.other.member":        ["DEFAULT_INSTANCE_FIELD"],
    "variable.other.property":      ["DEFAULT_INSTANCE_FIELD"],
    "variable.other.constant":      ["DEFAULT_CONSTANT"],
    "variable.other.object":        ["DEFAULT_LOCAL_VARIABLE"],
    "variable.parameter":           ["DEFAULT_PARAMETER"],
    "variable.language":            ["DEFAULT_KEYWORD"],
    "variable.language.this":       ["DEFAULT_KEYWORD"],
    "variable.interpolation":       ["DEFAULT_TEMPLATE_LANGUAGE_COLOR"],
    "entity.name.tag":              ["DEFAULT_TAG"],
    "entity.name.tag.yaml":         ["DEFAULT_TAG"],
    "entity.name.tag.html":         ["DEFAULT_TAG"],
    "entity.name.tag.js":           ["DEFAULT_TAG"],
    "entity.name.tag.css":          ["DEFAULT_TAG"],
    "support.class":                ["DEFAULT_CLASS_NAME"],
    "support.type.object.module.js": ["DEFAULT_CLASS_NAME"],
    "support.type.property-name.css": ["DEFAULT_INSTANCE_FIELD"],
    "meta.decorator variable":      ["DEFAULT_ANNOTATION_NAME"],
    "entity.name.label":            ["DEFAULT_LABEL"],
    "punctuation":                  ["DEFAULT_DOT", "DEFAULT_SEMICOLON"],
    "punctuation.bracket":          ["DEFAULT_BRACES", "DEFAULT_BRACKETS", "DEFAULT_PARENTHS"],
    "punctuation.separator":        ["DEFAULT_COMMA"],
    "punctuation.definition.tag":   ["DEFAULT_TAG"],
    "punctuation.definition.string": ["DEFAULT_STRING"],
    "meta.preprocessor":            ["DEFAULT_METADATA"],
    "markup.italic":                ["DEFAULT_MARKUP_ITALIC"],
    "markup.bold":                  ["DEFAULT_MARKUP_BOLD"],
    "entity.name.section":          ["DEFAULT_MARKUP_HEADING"],
    "entity.name.section.markdown": ["DEFAULT_MARKUP_HEADING"],
    "markup.raw":                   ["DEFAULT_MARKUP_CODE"],
    "markup.inline.raw":            ["DEFAULT_MARKUP_CODE_SPAN"],
    "fenced_code.block.language":   ["DEFAULT_MARKUP_CODE_SPAN"],
    "markup.underline.link":        ["DEFAULT_MARKUP_LINK"],
    "string.other.link":            ["DEFAULT_MARKUP_LINK"],
    "string.other.link.title":      ["DEFAULT_MARKUP_LINK"],
    "meta.link.inline.markdown":    ["DEFAULT_MARKUP_LINK"],
    "entity.name.function.expression": ["DEFAULT_FUNCTION_DECLARATION"],
}

# Canonical scopes that should drive each IntelliJ attribute.
# VSCode applies later rules over earlier ones, but IDEA attributes are coarser
# (one attribute covers a whole category). Resolution strategy:
#   - a rule matching the attribute's primary scope wins (last primary wins)
#   - any other mapped scope only fills the attribute if still unset
PRIMARY_SCOPES = {
    "DEFAULT_KEYWORD": [
        "keyword", "storage", "storage.type", "storage.modifier",
    ],
    "DEFAULT_CLASS_NAME": [
        "entity.name.type.class", "entity.name.type", "support.type",
        "support.class",
    ],
    "DEFAULT_INTERFACE_NAME": ["entity.name.type.interface"],
    "DEFAULT_CONSTANT": ["constant", "variable.other.constant"],
    "DEFAULT_NUMBER": ["constant.numeric"],
    "DEFAULT_STRING": ["string"],
    "DEFAULT_PARAMETER": ["variable.parameter"],
    "DEFAULT_INSTANCE_FIELD": ["variable.other.member", "variable.other.property"],
    "DEFAULT_LOCAL_VARIABLE": ["variable"],
    "DEFAULT_GLOBAL_VARIABLE": ["variable"],
    "DEFAULT_FUNCTION_DECLARATION": ["entity.name.function"],
    "DEFAULT_FUNCTION_CALL": ["support.function"],
    "DEFAULT_OPERATION_SIGN": ["keyword.operator"],
    "DEFAULT_TAG": [
        "entity.name.tag.html", "entity.name.tag.js", "entity.name.tag.css",
        "entity.name.tag.xml", "entity.name.tag.pug", "entity.name.tag.jade",
        "entity.name.tag.yaml", "entity.name.tag",
    ],
    "DEFAULT_ATTRIBUTE": ["entity.other.attribute-name"],
    "DEFAULT_VALID_STRING_ESCAPE": ["constant.character.escape"],
    "DEFAULT_REGEXP": ["string.regexp"],
    "DEFAULT_COMMENT": ["comment"],
    "DEFAULT_LINE_COMMENT": ["comment"],
    "DEFAULT_BLOCK_COMMENT": ["comment"],
    "DEFAULT_DOC_COMMENT": ["comment.block.documentation"],
}


def brightness(hex_color: str) -> float:
    """Perceived brightness 0-255."""
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16) + int(h[2:4], 16) + int(h[4:6], 16)) / 3


def ensure_contrast(color: str, against: str, min_delta: float = 55) -> str:
    """Ensure abs(brightness(color) - brightness(against)) >= min_delta.
    Adjusts in whichever direction color already differs from against.
    For dark themes (color brighter): lightens color.
    For light themes (color darker): darkens color.
    """
    if not color or not color.startswith("#"):
        return color
    h = color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    delta = brightness(color) - brightness(against)
    if delta >= 0 and delta < min_delta:
        # color is brighter than against but not enough → lighten more
        boost = int(min_delta - delta)
        r, g, b = min(255, r + boost), min(255, g + boost), min(255, b + boost)
    elif delta < 0 and abs(delta) < min_delta:
        # color is darker than against but not enough → darken more
        darken = int(min_delta - abs(delta))
        r, g, b = max(0, r - darken), max(0, g - darken), max(0, b - darken)
    else:
        return color
    return f"#{r:02x}{g:02x}{b:02x}"


def strip_alpha(color: str) -> str:
    """Strip alpha channel from #RRGGBBAA → #RRGGBB."""
    if not color or not color.startswith("#"):
        return color
    h = color[1:]
    if len(h) == 8:
        return "#" + h[:6]
    elif len(h) == 6:
        return "#" + h
    elif len(h) == 3:
        return "#" + h[0] * 2 + h[1] * 2 + h[2] * 2
    return color


def alpha_blend(fg_color: str, bg_color: str) -> str:
    """Alpha-blend fg_color onto bg_color (#RRGGBBAA or #RRGGBB).
    Returns a solid #RRGGBB that looks correct on that background.
    """
    if not fg_color or not fg_color.startswith("#"):
        return fg_color
    h = fg_color.lstrip("#")
    if len(h) == 8:
        r_f, g_f, b_f = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        a = int(h[6:8], 16) / 255.0
        bg = bg_color.lstrip("#")
        r_b, g_b, b_b = int(bg[0:2], 16), int(bg[2:4], 16), int(bg[4:6], 16)
        r = int(r_b * (1 - a) + r_f * a)
        g = int(g_b * (1 - a) + g_f * a)
        b = int(b_b * (1 - a) + b_f * a)
        return f"#{r:02x}{g:02x}{b:02x}"
    return strip_alpha(fg_color)


def to_xml_hex(color: str) -> str:
    """Convert #RRGGBB to rrggbb for IntelliJ XML scheme."""
    c = strip_alpha(color)
    if c and c.startswith("#"):
        return c[1:].lower()
    return (c or "").lower()


def font_type(style: str) -> int | None:
    """Convert VSCode fontStyle to IntelliJ FONT_TYPE (0=regular,1=bold,2=italic,3=bold+italic)."""
    if not style:
        return None
    bold = "bold" in style
    italic = "italic" in style
    if bold and italic:
        return 3
    if bold:
        return 1
    if italic:
        return 2
    return None


def build_ui_colors(
    colors: dict, dark: bool, preserve_source_contrast: bool = False
) -> dict:
    """Map VSCode colors dict to IntelliJ .theme.json ui section."""
    base_bg = strip_alpha(
        colors.get("editor.background") or ("#080909" if dark else "#fbfbfd")
    )

    def g(key):
        v = colors.get(key)
        return alpha_blend(v, base_bg) if v else None

    def ga(key, bg_fallback=base_bg):
        """Get color and alpha-blend it with bg_fallback."""
        v = colors.get(key)
        return alpha_blend(v, bg_fallback) if v else None

    bg          = g("editor.background")     or ("#080909" if dark else "#fbfbfd")
    fg          = g("editor.foreground")     or ("#abb2bf" if dark else "#1f1f1f")
    # Use alpha_blend for overlays so #RRGGBBAA → correct blended solid color
    sel_bg_raw  = ga("editor.selectionBackground", bg) or ga("selection.background", bg) or ("#2c313a" if dark else "#d0d8e8")
    sidebar_bg  = g("sideBar.background")    or bg
    status_bg   = g("statusBar.background")  or bg
    status_fg   = g("statusBar.foreground")  or fg
    title_bg    = g("titleBar.activeBackground") or bg
    tab_act     = g("tab.activeBackground")  or bg
    tab_inact   = g("tab.inactiveBackground") or sidebar_bg
    title_inact = g("titleBar.inactiveBackground") or title_bg
    border      = g("sideBar.border") or g("tab.border") or ("#212121" if dark else "#d0d0d0")
    input_bg    = ga("input.background", bg) or ("#2c313a" if dark else "#fbfbfd")
    list_hover  = ga("list.hoverBackground", bg) or input_bg
    list_act_raw = ga("list.activeSelectionBackground", bg) or input_bg
    list_act_fg = g("list.activeSelectionForeground") or fg
    line_num    = g("editorLineNumber.foreground") or ("#495162" if dark else "#9e9e9e")
    focus       = g("focusBorder") or g("tab.activeBorderTop") or ("#f5478c" if dark else "#644AC9")
    scroll_thumb = g("scrollbarSlider.background") or line_num
    scroll_hover = g("scrollbarSlider.hoverBackground") or fg

    # ── CONTRAST FIX ─────────────────────────────────────────────────────────
    # VSCode overlays these as semi-transparent; IntelliJ uses solid colors,
    # so we must guarantee minimum brightness delta from the background.
    # ensure_contrast() handles both dark (lighten) and light (darken) themes.
    MIN_SEL   = 45   # selection must stand out clearly (45 = visible but not too dark)
    MIN_HOVER = 28   # hover is subtler
    if preserve_source_contrast:
        sel_bg = sel_bg_raw
        list_act = list_act_raw
    else:
        sel_bg     = ensure_contrast(sel_bg_raw,   bg, MIN_SEL)
        list_act   = ensure_contrast(list_act_raw, bg, MIN_SEL)
        list_hover = ensure_contrast(list_hover,   bg, MIN_HOVER)
        if dark:
            input_bg = ensure_contrast(input_bg, bg, MIN_HOVER)
    # ─────────────────────────────────────────────────────────────────────────

    # ── Light theme: use IDEA accent blue for all active selections ───────────
    # For light themes the VSCode selectionBackground alpha-blends to gray.
    # Override with IDEA's New UI accent blue so Tree/List rows look like
    # the IDE default (blue row, white text) instead of dull gray.
    if not dark:
        list_act    = "#3574F0"
        list_act_fg = "#FFFFFF"
    # ─────────────────────────────────────────────────────────────────────────

    # ── TOOL WINDOW BUTTON active state → keep IDEA's default blue ────────────
    twb_active_bg = list_act if preserve_source_contrast else ("#2D6295" if dark else "#3574F0")
    twb_active_fg = "#ffffff"
    # ─────────────────────────────────────────────────────────────────────────

    # ── Default button foreground (light theme only) ───────────────────────
    # focus color (purple ~#644AC9) is dark → text must be near-white.
    # For dark themes, fg is already light so no change needed.
    btn_default_fg = fg if dark else "#FBFBFB"
    # Default/primary button: darkened accent (same hue, ~60% brightness) so the
    # bright teal/purple accent doesn't glare.
    h = focus.lstrip("#")
    default_btn_bg = (
        "#{:02x}{:02x}{:02x}".format(
            int(int(h[0:2], 16) * 0.6),
            int(int(h[2:4], 16) * 0.6),
            int(int(h[4:6], 16) * 0.6),
        )
        if len(h) >= 6
        else focus
    )
    # ─────────────────────────────────────────────────────────────────────────

    return {
        "*.background":                    bg,
        "*.foreground":                    fg,
        "*.selectionBackground":           sel_bg,
        "*.selectionForeground":           list_act_fg,
        "*.borderColor":                   border,
        "*.separatorColor":                border,
        "*.disabledBackground":            bg,
        "*.disabledForeground":            line_num,
        "*.inactiveForeground":            line_num,
        "*.focusedBorderColor":            focus,

        "ActionButton.hoverBackground":    list_hover,
        "ActionButton.pressedBackground":  list_act,

        "Button.background":               input_bg,
        "Button.foreground":               fg,
        "Button.startBackground":          input_bg,
        "Button.endBackground":            input_bg,
        # Turn off Darcula's button drop-shadow and use a darkened accent for the
        # default (primary) button — the bright accent + shadow looks too flashy.
        "Button.paintShadow":              False,
        "Button.default.background":       default_btn_bg,
        "Button.default.foreground":       btn_default_fg,
        "Button.default.startBackground":  default_btn_bg,
        "Button.default.endBackground":    default_btn_bg,
        "Button.default.focusedBorderColor": focus,

        "CheckBox.background":             bg,
        "CheckBox.foreground":             fg,

        "CompletionPopup.background":      input_bg,
        "CompletionPopup.selectionBackground": list_act,
        "CompletionPopup.selectionForeground": list_act_fg,

        "ComboBox.background":             input_bg,
        "ComboBox.foreground":             fg,
        "ComboBox.selectionBackground":    list_act,
        "ComboBox.selectionForeground":    list_act_fg,

        # ── EditorPane: font preview, quick-doc, settings panels ─────────────
        # These do NOT inherit from *.background — must be set explicitly.
        "EditorPane.background":           bg,
        "EditorPane.foreground":           fg,
        "EditorPane.selectionBackground":  sel_bg,
        "EditorPane.selectionForeground":  list_act_fg,
        "EditorPane.caretForeground":      fg,
        "EditorPane.inactiveForeground":   line_num,

        # TextPane (same family, used in quick-doc / help dialogs)
        "TextPane.background":             bg,
        "TextPane.foreground":             fg,
        "TextPane.selectionBackground":    sel_bg,
        "TextPane.selectionForeground":    list_act_fg,

        "EditorTabs.background":           sidebar_bg,
        "EditorTabs.underlinedTabBackground": tab_act,
        "EditorTabs.inactiveBackground":   tab_inact,
        "EditorTabs.inactiveForeground":   line_num,
        "EditorTabs.borderColor":          border,
        "EditorTabs.underlineColor":       focus,
        "EditorTabs.selectedBackground":   tab_act,

        "Link.activeForeground":           focus,
        "Link.foreground":                 focus,
        "Link.hoverForeground":            focus,
        "Link.visitedForeground":          focus,

        "List.background":                 bg,
        "List.foreground":                 fg,
        "List.selectionBackground":        list_act,
        "List.selectionForeground":        list_act_fg,
        "List.selectionInactiveBackground": list_hover,
        "List.selectionInactiveForeground": fg,
        "List.hoverBackground":            list_hover,

        "Menu.background":                 bg,
        "Menu.foreground":                 fg,
        "Menu.selectionBackground":        list_act,
        "Menu.selectionForeground":        list_act_fg,
        "Menu.separatorColor":             border,

        "MenuBar.background":              title_bg,
        "MenuBar.foreground":              fg,
        "MenuBar.borderColor":             border,
        # MainMenu is the real menu-bar key in Darcula (#3C3F41 default)
        "MainMenu.background":             title_bg,
        "MainMenu.foreground":             fg,

        "Notification.background":         input_bg,
        "Notification.foreground":         fg,

        "Panel.background":                bg,
        "Panel.foreground":                fg,

        # Popup header matches popup body (was bg=pure black before)
        "Popup.background":                input_bg,
        "Popup.foreground":                fg,
        "Popup.borderColor":               border,
        "Popup.headerBackground":          input_bg,
        "Popup.separatorForeground":       line_num,

        "ProgressBar.background":          border,
        "ProgressBar.foreground":          focus,
        "ProgressBar.progressColor":       focus,

        "ScrollBar.background":            bg,
        "ScrollBar.thumbColor":            scroll_thumb,
        "ScrollBar.thumbBorderColor":      scroll_thumb,
        "ScrollBar.hoverThumbColor":       scroll_hover,
        "ScrollBar.Mac.thumbColor":        scroll_thumb,
        "ScrollBar.Mac.hoverThumbColor":   scroll_hover,

        "SearchEverywhere.background":     bg,
        "SearchEverywhere.foreground":     fg,
        "SearchEverywhere.Tab.selectedBackground": list_act,
        "SearchEverywhere.Tab.selectedForeground": list_act_fg,

        "SidePanel.background":            sidebar_bg,

        "StatusBar.background":            status_bg,
        "StatusBar.foreground":            status_fg,
        "StatusBar.borderColor":           border,
        "StatusBar.hoverBackground":       list_hover,

        "TabbedPane.background":           bg,
        "TabbedPane.foreground":           fg,
        "TabbedPane.selectedBackground":   list_act,
        "TabbedPane.hoverBackground":      list_hover,
        "TabbedPane.underlineColor":       focus,

        "Table.background":                bg,
        "Table.foreground":                fg,
        "Table.gridColor":                 border,
        "Table.selectionBackground":       list_act,
        "Table.selectionForeground":       list_act_fg,
        "Table.selectionInactiveBackground": list_act,
        "Table.stripeColor":               sidebar_bg,

        "TextArea.background":             bg,
        "TextArea.foreground":             fg,
        "TextArea.selectionBackground":    sel_bg,
        "TextArea.selectionForeground":    list_act_fg,

        "TextField.background":            input_bg,
        "TextField.foreground":            fg,
        "TextField.selectionBackground":   sel_bg,
        "TextField.borderColor":           border,

        "TitleBar.background":             title_bg,
        "TitleBar.foreground":             fg,
        "TitleBar.inactiveBackground":     title_inact,
        "TitleBar.inactiveForeground":     line_num,
        "TitlePane.background":            title_bg,
        "TitlePane.foreground":            fg,

        "ToolWindow.background":           sidebar_bg,
        "ToolWindow.foreground":           fg,
        # Header keys must use Darcula's nested form (ToolWindow.Header.background)
        # — the camelCase variants are not recognized and fall back to #3C3F41.
        "ToolWindow.Header.background":          sidebar_bg,
        "ToolWindow.Header.inactiveBackground":  sidebar_bg,
        "ToolWindow.Header.foreground":          fg,
        "ToolWindow.Header.inactiveForeground":  line_num,
        "ToolWindow.Header.borderColor":         border,
        "ToolWindow.HeaderTab.selectedBackground": list_act,
        "ToolWindow.HeaderTab.selectedForeground": list_act_fg,

        "Tree.background":                 sidebar_bg,
        "Tree.foreground":                 fg,
        "Tree.selectionBackground":        list_act,
        "Tree.selectionForeground":        list_act_fg,
        "Tree.selectionInactiveBackground": list_hover,
        "Tree.selectionInactiveForeground": fg,
        "Tree.hoverBackground":            list_hover,
        # New UI (2023.1+) uses TreeView/ProjectView keys — without these the
        # sidebar tree falls back to Darcula's default (#46484A).
        "TreeView.background":             sidebar_bg,
        "TreeView.foreground":             fg,
        "TreeView.selectionBackground":    list_act,
        "TreeView.selectionForeground":    list_act_fg,
        "TreeView.selectionInactiveBackground": list_hover,
        "TreeView.selectionInactiveForeground": fg,
        "TreeView.hoverBackground":        list_hover,
        "ProjectView.background":          sidebar_bg,
        "ProjectView.foreground":          fg,
        "ProjectView.selectionBackground": list_act,
        "ProjectView.selectionForeground": list_act_fg,

        # ── ToolWindowButton: keep IDEA default blue for active sidebar icons ─
        "ToolWindowButton.selectedBackground": twb_active_bg,
        "ToolWindowButton.selectedForeground": twb_active_fg,
        "ToolWindowButton.selectedIconColor":  twb_active_fg,  # New UI icon tint
        "ToolWindowButton.hoverBackground":    list_hover,

        "WelcomeScreen.background":        bg,
        "WelcomeScreen.foreground":        fg,
        "WelcomeScreen.captionBackground": sidebar_bg,
        "WelcomeScreen.captionForeground": fg,
        "WelcomeScreen.headerBackground":  sidebar_bg,
        "WelcomeScreen.headerForeground":  fg,
    }


def build_color_scheme_xml(
    name: str,
    dark: bool,
    colors: dict,
    token_colors: list,
    editor_font: str | None = None,
    extras=None,
) -> str:
    """Generate IntelliJ color scheme XML from VSCode theme data."""
    def g(key):
        v = colors.get(key)
        return strip_alpha(v) if v else None

    bg       = g("editor.background")     or ("#080909" if dark else "#fbfbfd")
    fg       = g("editor.foreground")     or ("#abb2bf" if dark else "#1f1f1f")
    # Alpha-blend selection onto editor background (e.g. #67769640 → deep blue-gray)
    # then ensure_contrast so it's actually visible on solid background.
    # Use a low min_delta (20) so selection stays subtle — syntax colors remain visible.
    sel_raw  = alpha_blend(colors.get("editor.selectionBackground", ""), bg) or ("#2c313a" if dark else "#d0d8e8")
    sel_bg   = ensure_contrast(sel_raw, bg, 20)
    line_num = g("editorLineNumber.foreground") or ("#495162" if dark else "#9e9e9e")
    cursor   = g("editorCursor.foreground") or fg
    caret_row = alpha_blend(colors.get("editor.lineHighlightBackground", ""), bg) or bg
    whitespace = g("editorWhitespace.foreground") or line_num
    indent_guide = alpha_blend(colors.get("editorIndentGuide.background1", ""), bg) or ("#212121" if dark else "#d0d0d0")
    active_indent_guide = alpha_blend(colors.get("editorIndentGuide.activeBackground1", ""), bg) or line_num
    margin = alpha_blend(colors.get("widget.border", ""), bg) or ("#444444" if dark else "#aaaaaa")
    parent   = "Darcula" if dark else "Default"

    # Build attribute map: attr_name → (fg, bg, font_type_int, priority)
    # Priorities come from PRIMARY_SCOPES ordering; lower = more canonical.
    # Equal priority: later rule wins (mirrors VSCode rule stacking).
    attrs: dict[str, tuple] = {}
    for tc in token_colors:
        scope_val = tc.get("scope", "")
        settings  = tc.get("settings", {})
        tc_fg  = strip_alpha(settings.get("foreground", "")) or None
        tc_bg  = strip_alpha(settings.get("background", "")) or None
        ft     = font_type(settings.get("fontStyle", ""))

        scopes = scope_val if isinstance(scope_val, list) else [scope_val]
        for scope in scopes:
            for sub in scope.split(","):
                sub = sub.strip()
                for attr in SCOPE_TO_ATTR.get(sub, []):
                    primaries = PRIMARY_SCOPES.get(attr)
                    if primaries and sub in primaries:
                        prio = primaries.index(sub)
                        if attr not in attrs or prio <= attrs[attr][3]:
                            attrs[attr] = (tc_fg, tc_bg, ft, prio)
                    elif attr not in attrs:
                        attrs[attr] = (tc_fg, tc_bg, ft, float("inf"))

    for k in getattr(extras, "FORCE", {}):
        attrs.pop(k, None)

    def attr_xml(attr_name: str, tc_fg=None, tc_bg=None, ft=None) -> str:
        opts = []
        if tc_fg:
            opts.append(f'        <option name="FOREGROUND" value="{to_xml_hex(tc_fg)}"/>')
        if tc_bg:
            opts.append(f'        <option name="BACKGROUND" value="{to_xml_hex(tc_bg)}"/>')
        if ft is not None:
            opts.append(f'        <option name="FONT_TYPE" value="{ft}"/>')
        if not opts:
            return f'    <option name="{attr_name}"/>'
        inner = "\n".join(opts)
        return (
            f'    <option name="{attr_name}">\n'
            f'      <value>\n'
            f'{inner}\n'
            f'      </value>\n'
            f'    </option>'
        )

    lines = [
        f'<scheme name="{name}" version="142" parent_scheme="{parent}">',
        '  <metaInfo>',
        '    <property name="created">2025-01-01</property>',
        '    <property name="ide">Idea</property>',
        f'    <property name="originalScheme">{name}</property>',
        '  </metaInfo>',
        '  <colors>',
        f'    <option name="CARET_ROW_COLOR" value="{to_xml_hex(caret_row)}"/>',
        f'    <option name="CARET_COLOR" value="{to_xml_hex(cursor)}"/>',
        f'    <option name="SELECTION_BACKGROUND" value="{to_xml_hex(sel_bg)}"/>',
        '    <option name="SELECTION_FOREGROUND"/>',
        f'    <option name="LINE_NUMBERS_COLOR" value="{to_xml_hex(line_num)}"/>',
        f'    <option name="WHITESPACES" value="{to_xml_hex(whitespace)}"/>',
        f'    <option name="INDENT_GUIDE" value="{to_xml_hex(indent_guide)}"/>',
        f'    <option name="SELECTED_INDENT_GUIDE" value="{to_xml_hex(active_indent_guide)}"/>',
        f'    <option name="RIGHT_MARGIN_COLOR" value="{to_xml_hex(margin)}"/>',
        f'    <option name="TEARLINE_COLOR" value="{to_xml_hex(margin)}"/>',
        # Terminal background: the real key is CONSOLE_BACKGROUND_KEY (not
        # CONSOLE_BACKGROUND, which is ignored in New UI / GoLand 2026.x).
        f'    <option name="CONSOLE_BACKGROUND_KEY" value="{to_xml_hex(g("terminal.background") or bg)}"/>',
        f'    <option name="CONSOLE_FOREGROUND" value="{to_xml_hex(g("terminal.foreground") or fg)}"/>',
        # Code-completion popup background (LOOKUP_COLOR) — match terminal bg.
        f'    <option name="LOOKUP_COLOR" value="{to_xml_hex(g("terminal.background") or bg)}"/>',
        *(extras.extra_colors_xml() if extras else []),
        '  </colors>',
        '  <attributes>',
        attr_xml("TEXT", tc_fg=fg, tc_bg=bg),
        attr_xml("DEFAULT_BACKGROUND", tc_bg=bg),
    ]

    if editor_font:
        lines.insert(
            lines.index('  <attributes>'),
            '  <fonts>\n'
            f'    <font name="{editor_font}" size="12" lineSpacing="1.0"/>\n'
            '  </fonts>',
        )

    for attr_name, (tc_fg, tc_bg, ft, _prio) in sorted(attrs.items()):
        lines.append(attr_xml(attr_name, tc_fg, tc_bg, ft))
        # Go/Python/etc. token keys (GO_EXPORTED_FUNCTION, …) fall back to the
        # unprefixed key (FUNCTION_DECLARATION, GLOBAL_VARIABLE, …) which has its
        # own default color (#AFC07E, #B6A985). Emit the unprefixed twin so those
        # tokens also pick up the theme color.
        if attr_name.startswith("DEFAULT_"):
            twin = attr_name[len("DEFAULT_"):]
            if twin not in attrs and twin not in getattr(extras, "FORCE", {}):
                lines.append(attr_xml(twin, tc_fg, tc_bg, ft))

    # Base identifiers (Go package names etc.) — default to the editor foreground.
    for base in ("IDENTIFIER", "CLASS_REFERENCE", "INSTANCE_METHOD", "STATIC_FIELD"):
        if base not in attrs and ("DEFAULT_" + base) not in attrs and base not in getattr(extras, "FORCE", {}):
            lines.append(attr_xml(base, tc_fg=fg, tc_bg=None, ft=None))

    if extras:
        emitted = set(re.findall(r'^    <option name="([^"]+)"', "\n".join(lines), re.M))
        lines += extras.extra_attrs_xml(emitted)

    lines += [
        '  </attributes>',
        '</scheme>',
    ]

    return "\n".join(lines)


def build_islands_theme(
    name: str,
    tid: str,
    colors: dict,
    editor_scheme: str,
) -> dict:
    """Build a New UI (Islands) theme JSON for GoLand 2026.x.

    Islands themes use parentTheme='Islands Dark' + a 'colors' variable table,
    and the ui section references those variables. Without this variant the
    Islands-only components (code-completion popup, tool-window panels, etc.)
    fall back to the default Islands palette instead of the theme's colors.
    """
    def c(key, fallback):
        return colors.get(key) or fallback

    def strip(v):
        v = v.lstrip("#")
        return "#" + v[:6] if len(v) >= 6 else "#" + v

    editor_bg   = strip(c("editor.background", "#000000"))
    sidebar_bg  = strip(c("sideBar.background", "#07080a"))
    fg          = strip(c("editor.foreground", "#F5F5FA"))
    accent      = strip(c("focusBorder", "#19F9D8"))           # teal accent
    accent_soft = "#4FE6C8"
    comment     = strip(c("editorHint.foreground", accent))
    sel_bg      = strip(c("editor.selectionBackground", "#141d26"))
    input_bg    = strip(c("input.background", "#17191f"))
    hover_bg    = strip(c("list.hoverBackground", "#10161d"))
    sel_hover   = "#1e2b2a"
    border      = strip(c("sideBar.border", "#FFFFFF1A")) or "#1a1a1a"
    if len(border) == 7 and border[:1] == "#":
        border = "#1a1a1a"

    return {
        "name": f"{name} (Islands)",
        "dark": True,
        "author": "BennyWu",
        "editorScheme": editor_scheme,
        "parentTheme": "Islands Dark",
        "colors": {
            "accentColor": accent,
            "secondaryAccentColor": accent_soft,
            "primaryForeground": fg,
            "primaryBackground": sidebar_bg,
            "secondaryBackground": editor_bg,
            "hoverBackground": hover_bg,
            "selectionBackground": sel_bg,
            "selectionInactiveBackground": sel_hover,
            "borderColor": border,
            "separatorColor": border,
            "editorBackground": editor_bg,
            "transparent": "#00000000",
        },
        "ui": {
            "*": {
                "background": "primaryBackground",
                "selectionForeground": "primaryForeground",
                "selectionInactiveForeground": "primaryForeground",
                "selectionBackground": "selectionBackground",
                "selectionInactiveBackground": "selectionInactiveBackground",
                "inactiveBackground": "primaryBackground",
                "disabledBackground": "primaryBackground",
                "borderColor": "borderColor",
                "separatorColor": "separatorColor",
            },
            "Editor": {"background": "editorBackground"},
            "EditorTabs": {
                "background": "primaryBackground",
                "underlinedTabBackground": "secondaryBackground",
                "underlinedBorderColor": "accentColor",
                "underlineHeight": 2,
            },
            "CompletionPopup": {
                "background": "secondaryBackground",
                "selectionBackground": "selectionBackground",
                "selectionInactiveBackground": "selectionInactiveBackground",
                "matchForeground": "accentColor",
            },
            "List": {
                "background": "secondaryBackground",
                "selectionBackground": "selectionBackground",
                "selectionInactiveBackground": "selectionInactiveBackground",
                "hoverBackground": "selectionInactiveBackground",
                "hoverInactiveBackground": "selectionInactiveBackground",
            },
            "Tree": {
                "background": "primaryBackground",
                "selectionBackground": "selectionBackground",
                "selectionInactiveBackground": "selectionInactiveBackground",
                "hoverBackground": "selectionInactiveBackground",
                "hoverInactiveBackground": "selectionInactiveBackground",
            },
            "ToolWindow": {
                "background": "primaryBackground",
                "Header": {
                    "background": "primaryBackground",
                    "inactiveBackground": "primaryBackground",
                },
                "HeaderTab": {
                    "underlineColor": "accentColor",
                    "underlineHeight": 2,
                    "underlinedTabBackground": "secondaryBackground",
                    "underlinedTabInactiveBackground": "secondaryBackground",
                },
                "Stripe": {"background": "secondaryBackground", "borderColor": "transparent"},
            },
            "SidePanel": {"background": "primaryBackground"},
            "StatusBar": {"background": "secondaryBackground", "borderColor": "transparent"},
            "MainToolbar": {"background": "secondaryBackground", "borderColor": "transparent"},
            "MainWindow": {"background": "secondaryBackground"},
            "MainWindow.Tab": {
                "selectedBackground": "selectionBackground",
                "selectedForeground": "primaryForeground",
                "selectedInactiveBackground": "secondaryBackground",
                "hoverBackground": "hoverBackground",
                "hoverForeground": "primaryForeground",
                "separatorColor": "separatorColor",
            },
            "SearchEverywhere": {
                "background": "secondaryBackground",
                "SearchField": {"background": "secondaryBackground"},
                "Tab": {"selectedBackground": "selectionBackground", "selectedForeground": "primaryForeground"},
            },
            "TextField": {"background": "secondaryBackground"},
            "PasswordField": {"background": "secondaryBackground"},
            "ComboBox": {
                "background": "secondaryBackground",
                "nonEditableBackground": "secondaryBackground",
                "ArrowButton": {"background": "secondaryBackground", "nonEditableBackground": "secondaryBackground"},
            },
            "Button": {
                "foreground": "primaryForeground",
                "startBackground": "#1c2a27",
                "endBackground": "#1c2a27",
                "startBorderColor": "borderColor",
                "endBorderColor": "borderColor",
                "focusedBorderColor": "accentColor",
                "default": {
                    "foreground": "primaryForeground",
                    "startBackground": "#0c7767",
                    "endBackground": "#0c7767",
                    "startBorderColor": "accentColor",
                    "endBorderColor": "accentColor",
                    "focusColor": "accentColor",
                    "focusedBorderColor": "accentColor",
                },
            },
            "ProgressBar": {
                "progressColor": "accentColor",
                "trackColor": "selectionBackground",
                "indeterminateStartColor": "accentColor",
                "indeterminateEndColor": accent_soft,
                "passedColor": "#22E67A",
                "passedEndColor": "#22E67A",
            },
            "Link": {
                "activeForeground": "accentColor",
                "hoverForeground": "accentColor",
                "visitedForeground": "accentColor",
                "pressedForeground": "accentColor",
            },
            "Separator": {"separatorColor": "separatorColor"},
            "ScrollBar": {"Mac": {"hoverThumbColor": "accentColor", "Transparent": {"hoverThumbColor": "accentColor"}}},
            "Island": {"borderColor": "primaryBackground", "arc": "20", "borderWidth": "6"},
        },
    }


def _load_extras(mod_name):
    if not mod_name:
        return None
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    return importlib.import_module(mod_name)


def convert_theme(theme_info: dict):
    vscode_dir = theme_info.get("vscode_dir", VSCODE_DIR)
    vscode_path = vscode_dir / theme_info["vscode_file"]
    data = json.loads(vscode_path.read_text())
    # Honour VS Code "include" (base theme): base first, theme overrides.
    if data.get("include"):
        base = json.loads((vscode_path.parent / data["include"]).read_text())
        data["colors"] = {**base.get("colors", {}), **data.get("colors", {})}
        data["tokenColors"] = base.get("tokenColors", []) + data.get("tokenColors", [])

    name  = theme_info["name"]
    tid   = theme_info["id"]
    dark  = theme_info["dark"]
    out_dir = theme_info.get("output_dir", OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    colors       = data.get("colors", {})
    token_colors = data.get("tokenColors", [])

    # --- Generate .theme.json ---
    # Optional per-theme UI-only colour overrides (extras.UI_COLOR_OVERRIDES):
    # applied to the .theme.json / Islands UI, never to the editor scheme XML.
    extras_mod = _load_extras(theme_info.get("extras"))
    ui_source = {**colors, **getattr(extras_mod, "UI_COLOR_OVERRIDES", {})}
    ui_colors = build_ui_colors(
        ui_source,
        dark,
        preserve_source_contrast=theme_info.get("preserve_source_contrast", False),
    )
    theme_json = {
        "name": name,
        "dark": dark,
        "author": "BennyWu",
        "parentTheme": theme_info.get("parent_theme", "Darcula" if dark else "IntelliJ Light"),
        "editorScheme": f"/themes/{tid}.xml",
        "ui": ui_colors,
    }
    theme_json_path = out_dir / f"{tid}.theme.json"
    theme_json_path.write_text(
        json.dumps(theme_json, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  [OK] {tid}.theme.json")

    # --- Generate Islands (New UI) variant if requested ---
    if theme_info.get("islands", False):
        islands_theme = build_islands_theme(
            name, tid, ui_source, f"/themes/{tid}.xml"
        )
        islands_path = out_dir / f"{tid}Islands.theme.json"
        islands_path.write_text(
            json.dumps(islands_theme, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"  [OK] {tid}Islands.theme.json")

    # --- Generate .xml color scheme ---
    xml_content = build_color_scheme_xml(
        name, dark, colors, token_colors, theme_info.get("editor_font"),
        extras=extras_mod,
    )
    xml_path = out_dir / f"{tid}.xml"
    xml_path.write_text(xml_content, encoding="utf-8")
    print(f"  [OK] {tid}.xml")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "theme",
        nargs="?",
        choices=[theme["key"] for theme in THEMES],
        help="Generate only one theme; omit to generate every configured theme.",
    )
    args = parser.parse_args()
    selected_themes = (
        [theme for theme in THEMES if theme["key"] == args.theme]
        if args.theme
        else THEMES
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Converting VSCode themes → IntelliJ format...\n")
    done = 0
    out_dirs = set()
    for t in selected_themes:
        print(f"→ {t['name']}")
        if not (t.get("vscode_dir", VSCODE_DIR) / t["vscode_file"]).exists():
            print("  [SKIP] source theme file not found")
            continue
        convert_theme(t)
        out_dirs.add(str(t.get("output_dir", OUTPUT_DIR)))
        done += 1
    print(f"\nDone! Generated {done * 2} files in:")
    for d in sorted(out_dirs):
        print(f"  {d}")


if __name__ == "__main__":
    main()
