#!/usr/bin/env python3
"""Generate the Cremisi Zed themes from palette.yaml.

    python3 ports/zed/generate.py

Writes themes/cremisi.json: one theme family holding Cremisi Obsidian and Cremisi Ivory.
Syntax follows the roles of the palette rules, translated into the capture names of Zed's
Tree-sitter queries; the interface is built from the materials and the stone and blood scales.
"""
import json
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
PALETTE = yaml.safe_load((HERE.parent.parent / "palette.yaml").read_text(encoding="utf-8"))
VARIANTS = ("obsidian", "ivory")

# Zed capture name -> (material, style). A capture falls back to its longest defined prefix
# (keyword.control.return -> keyword.control -> keyword), so only the roles that differ from
# their parent are listed. Checked against the queries that ship with Zed 1.26.
# Semantic tokens look their styles up by exact name: function.macro, keyword.modifier,
# string.regexp and type.enum.member are here for them.
SYNTAX = [
    # Comments and documentation
    ("comment", "incense", "italic"),
    ("comment.doc", "incense", "italic"),
    ("comment.documentation", "incense", "italic"),
    ("string.doc", "incense", "italic"),  # Python docstrings, as in the VS Code port
    # Keywords: declarations italic, control flow bold
    ("keyword", "blood", "italic"),
    ("keyword.modifier", "blood", "italic"),
    ("keyword.control", "blood", "bold"),
    ("keyword.conditional", "blood", "bold"),
    ("keyword.repeat", "blood", "bold"),
    ("keyword.return", "blood", "bold"),
    ("keyword.exception", "blood", "bold"),
    ("keyword.coroutine", "blood", "bold"),
    ("keyword.import", "wine", "italic"),
    ("keyword.export", "wine", "italic"),
    ("keyword.preproc", "wine", "italic"),
    ("keyword.directive", "wine", "italic"),
    ("preproc", "wine", "italic"),
    ("keyword.operator", "wine", None),
    ("operator", "wine", None),
    # Functions
    ("function", "lapis", "italic"),
    ("function.builtin", "amethyst", "italic"),
    ("function.decorator", "sealwax", None),
    ("function.special", "wine", None),  # Rust and C macros
    ("function.macro", "wine", None),
    ("function.kwargs", "petal", "italic"),  # Python keyword arguments
    ("constructor", "blood", "italic"),  # the `constructor` of a JS class
    # Variables and members
    ("variable", "ink", None),
    ("variable.parameter", "petal", "italic"),
    ("variable.special", "amethyst", "italic"),  # self, this, super, $@
    ("variable.builtin", "amethyst", "italic"),
    ("property", "verdigris", None),
    ("property.json_key", "lapis", None),
    ("attribute", "tallow", "italic"),
    ("attribute.builtin", "sealwax", None),  # @classmethod, @staticmethod, @property
    ("attribute.special", "amethyst", "italic"),  # __name__, __dict__
    # Types
    ("type", "tallow", "italic"),
    ("type.class.builtin", "blood", "italic"),  # Python exceptions
    ("type.unit", "amber", None),  # CSS units
    ("type.enum.member", "amber", None),
    ("variant", "amber", None),
    ("namespace", "tallow", "italic"),
    ("module", "tallow", "italic"),
    ("concept", "tallow", "italic"),
    ("lifetime", "tallow", "italic"),
    ("tag.component", "tallow", "italic"),  # JSX components
    ("selector", "tallow", "italic"),  # CSS classes, ids, pseudo-classes
    # Literals
    ("string", "malachite", None),
    ("character", "malachite", None),
    ("string.escape", "sealwax", None),
    ("string.special", "sealwax", None),  # format specifiers, entities, CSS colours
    ("string.special.url", "lapis", None),
    ("string.regex", "sealwax", None),
    ("string.regexp", "sealwax", None),
    ("operator.regex", "sealwax", None),
    ("keyword.operator.regex", "sealwax", None),
    ("label.regex", "sealwax", None),
    ("number.quantifier", "sealwax", None),
    ("number", "amber", None),
    ("constant", "amber", None),
    ("constant.builtin", "blood", "bold italic"),  # null, None, nil
    ("boolean", "blood", "bold italic"),
    ("label", "sealwax", None),
    # Code inside strings: f-strings, template literals, $(...)
    ("embedded", "ink", None),
    # Punctuation
    ("punctuation", "iron", None),
    ("punctuation.special", "sealwax", None),  # ${ }, f-string braces, #[ ], @
    ("punctuation.list_marker", "blood", None),
    # Markup
    ("tag", "blood", None),
    ("tag.attribute", "tallow", "italic"),
    ("tag.delimiter", "iron", None),
    ("title", "blood", "bold"),
    ("markup.heading", "blood", "bold"),
    ("emphasis", "petal", "italic"),
    ("emphasis.strong", "tallow", "bold"),
    ("markup.italic", "petal", "italic"),
    ("markup.strong", "tallow", "bold"),
    ("text.literal", "malachite", None),
    ("markup.raw", "malachite", None),
    ("markup.quote", "incense", "italic"),
    ("markup.list", "blood", None),
    ("strikethrough", "incense", None),
    ("markup.strikethrough", "incense", None),
    ("link_text", "lapis", None),
    ("link_uri", "lapis", None),
    ("markup.link", "lapis", None),
    # Diff
    ("diff.plus", "malachite", None),
    ("diff.minus", "blood", None),
    ("diff.delta", "amber", None),
]

FONT = {
    None: {},
    "italic": {"font_style": "italic"},
    "bold": {"font_weight": 700},
    "bold italic": {"font_style": "italic", "font_weight": 700},
}


def alpha(hex_colour, a):
    return f"{hex_colour}{round(a * 255):02x}"


def palette(variant):
    p = {m["key"]: m[variant] for m in PALETTE["materials"]}
    p.update({u["key"]: u[variant] for u in PALETTE["ui_vars"]})
    for scale in PALETTE["scales"]:
        for step in scale["steps"]:
            p[f'{scale["key"]}-{step["n"]}'] = step["hex"]
    return p


def syntax(c):
    return {key: {"color": c[fg], **FONT[style]} for key, fg, style in SYNTAX}


def terminal(c, dim, dark):
    # Dim colours are the same materials read from the other variant: darker on Obsidian,
    # paler on Ivory, the hue unchanged.
    hues = {"red": "blood", "green": "malachite", "yellow": "amber", "blue": "lapis",
            "magenta": "amethyst", "cyan": "verdigris"}
    t = {
        "terminal.background": c["ground"],
        "terminal.ansi.background": c["ground"],
        "terminal.foreground": c["ink"],
        "terminal.bright_foreground": c["stone-50"] if dark else c["stone-950"],
        "terminal.dim_foreground": c["stone-400"] if dark else c["stone-600"],
    }
    for name, material in hues.items():
        t[f"terminal.ansi.{name}"] = c[material]
        t[f"terminal.ansi.bright_{name}"] = c[material]
        t[f"terminal.ansi.dim_{name}"] = dim[material]
    t["terminal.ansi.bright_yellow"] = c["tallow"]
    t["terminal.ansi.bright_magenta"] = c["petal"]
    if dark:
        t.update({
            "terminal.ansi.black": c["stone-800"],
            "terminal.ansi.bright_black": c["stone-500"],  # stone-600 is 2.97:1, under 3:1
            "terminal.ansi.dim_black": c["stone-800"],
            "terminal.ansi.white": c["stone-200"],
            "terminal.ansi.bright_white": c["stone-50"],
            "terminal.ansi.dim_white": c["stone-400"],
            "terminal.ansi.bright_red": c["blood-400"],
        })
    else:
        t.update({
            "terminal.ansi.black": c["ink"],
            "terminal.ansi.bright_black": c["stone-500"],
            "terminal.ansi.dim_black": c["stone-600"],
            "terminal.ansi.white": c["stone-300"],
            "terminal.ansi.bright_white": c["stone-200"],
            "terminal.ansi.dim_white": c["stone-200"],
            "terminal.ansi.bright_red": c["blood-700"],
        })
    return t


def style(c, dim, dark):
    if dark:
        ground, deep, raised, border, field = c["stone-900"], c["stone-950"], c["stone-800"], c["stone-800"], c["stone-700"]
        text, muted, placeholder, faint = c["stone-100"], c["stone-400"], c["stone-500"], c["stone-600"]
        link, error_bg, error_border = c["blood-400"], c["blood-950"], c["blood-800"]
    else:
        ground, deep, raised, border, field = c["stone-50"], c["stone-100"], c["stone-200"], c["stone-200"], c["stone-300"]
        text, muted, placeholder, faint = c["stone-900"], c["stone-600"], c["stone-600"], c["stone-400"]
        link, error_bg, error_border = c["blood-700"], c["blood-50"], c["blood-200"]

    # Crimson is the only accent: cursor, selection, focus, the selected entry.
    accent = c["crimson"]
    selection = alpha(accent, 0.24)
    transparent = "#00000000"

    s = {
        "background.appearance": "opaque",
        "accents": [c[m] for m in ("blood", "amber", "lapis", "malachite", "amethyst", "verdigris", "petal")],

        # surfaces: the editor is the ground, the chrome around it the sunken stone
        "background": deep,
        "surface.background": deep,
        "elevated_surface.background": deep,
        "panel.background": deep,
        "panel.overlay_background": deep,
        "panel.overlay_hover": raised,
        "panel.focused_border": transparent,
        "panel.indent_guide": alpha(c["ink"], 0.10),
        "panel.indent_guide_active": alpha(c["ink"], 0.20),
        "panel.indent_guide_hover": alpha(c["ink"], 0.28),
        "pane.focused_border": transparent,
        "pane_group.border": border,
        "title_bar.background": deep,
        "title_bar.inactive_background": deep,
        "status_bar.background": deep,
        "toolbar.background": ground,
        "tab_bar.background": deep,
        "tab.inactive_background": deep,
        "tab.active_background": ground,

        # borders
        "border": field,
        "border.variant": border,
        "border.focused": alpha(accent, 0.7),
        "border.selected": accent,
        "border.transparent": transparent,
        "border.disabled": border,

        # elements
        "element.background": deep,
        "element.hover": raised,
        "element.active": field,
        "element.selected": selection,
        "element.selection_background": selection,
        "element.disabled": deep,
        "ghost_element.background": transparent,
        "ghost_element.hover": alpha(c["ink"], 0.06),
        "ghost_element.active": alpha(c["ink"], 0.10),
        "ghost_element.selected": selection,
        "ghost_element.disabled": transparent,
        "drop_target.background": alpha(accent, 0.12),
        "drop_target.border": accent,

        # text and icons
        "text": text,
        "text.muted": muted,
        "text.placeholder": placeholder,
        "text.disabled": faint,
        "text.accent": c["blood"],
        "icon": text,
        "icon.muted": muted,
        "icon.disabled": faint,
        "icon.placeholder": muted,
        "icon.accent": c["blood"],
        "link_text.hover": link,

        # scrollbars and minimap
        "scrollbar.thumb.background": alpha(c["ink"], 0.12),
        "scrollbar.thumb.hover_background": alpha(c["ink"], 0.20),
        "scrollbar.thumb.active_background": alpha(c["ink"], 0.28),
        "scrollbar.thumb.border": transparent,
        "scrollbar.track.background": transparent,
        "scrollbar.track.border": transparent,
        "minimap.thumb.background": alpha(c["ink"], 0.08),
        "minimap.thumb.hover_background": alpha(c["ink"], 0.12),
        "minimap.thumb.active_background": alpha(c["ink"], 0.16),
        "minimap.thumb.border": transparent,

        # editor
        "editor.foreground": c["ink"],
        "editor.background": ground,
        "editor.gutter.background": ground,
        "editor.subheader.background": deep,
        "editor.active_line.background": alpha(c["ink"], 0.05),
        "editor.highlighted_line.background": alpha(c["ink"], 0.08),
        "editor.debugger_active_line.background": alpha(c["amber"], 0.15),
        "editor.line_number": c["gutter_fg"],
        "editor.active_line_number": c["blood"],
        "editor.hover_line_number": muted,
        "editor.invisible": alpha(c["ink"], 0.12),
        "editor.wrap_guide": alpha(c["ink"], 0.08),
        "editor.active_wrap_guide": alpha(c["ink"], 0.16),
        "editor.indent_guide": alpha(c["ink"], 0.06),
        "editor.indent_guide_active": alpha(c["ink"], 0.16),
        "editor.document_highlight.read_background": alpha(c["ink"], 0.08),
        "editor.document_highlight.write_background": alpha(c["ink"], 0.12),
        "editor.document_highlight.bracket_background": alpha(c["blood"], 0.15),
        "editor.code_lens.foreground": muted,
        "search.match_background": alpha(c["amber"], 0.2),
        "search.active_match_background": alpha(c["amber"], 0.45),

        # version control: diff hunks are derived by Zed from added and deleted
        "version_control.added": c["malachite"],
        "version_control.deleted": c["blood"],
        "version_control.modified": c["amber"],
        "version_control.renamed": c["verdigris"],
        "version_control.conflict": c["sealwax"],
        "version_control.ignored": faint,
        "version_control.word_added": alpha(c["malachite"], 0.3),
        "version_control.word_deleted": alpha(c["blood"], 0.3),
        "version_control.conflict_marker.ours": alpha(c["malachite"], 0.15),
        "version_control.conflict_marker.theirs": alpha(c["lapis"], 0.15),
        "debugger.accent": accent,

        # status
        "error": c["blood"],
        "error.background": error_bg,
        "error.border": error_border,
        "warning": c["amber"],
        "warning.background": alpha(c["amber"], 0.12),
        "warning.border": alpha(c["amber"], 0.5),
        "info": c["lapis"],
        "info.background": alpha(c["lapis"], 0.12),
        "info.border": alpha(c["lapis"], 0.5),
        "success": c["malachite"],
        "success.background": alpha(c["malachite"], 0.12),
        "success.border": alpha(c["malachite"], 0.5),
        "hint": muted,  # inlay hints
        "hint.background": alpha(c["ink"], 0.05),
        "hint.border": border,
        "predictive": c["stone-500"],  # edit predictions
        "predictive.background": alpha(c["ink"], 0.05),
        "predictive.border": border,
        "created": c["malachite"],
        "created.background": alpha(c["malachite"], 0.12),
        "created.border": alpha(c["malachite"], 0.5),
        "modified": c["amber"],
        "modified.background": alpha(c["amber"], 0.12),
        "modified.border": alpha(c["amber"], 0.5),
        "deleted": c["blood"],
        "deleted.background": alpha(c["blood"], 0.12),
        "deleted.border": alpha(c["blood"], 0.5),
        "renamed": c["verdigris"],
        "renamed.background": alpha(c["verdigris"], 0.12),
        "renamed.border": alpha(c["verdigris"], 0.5),
        "conflict": c["sealwax"],
        "conflict.background": alpha(c["sealwax"], 0.12),
        "conflict.border": alpha(c["sealwax"], 0.5),
        "hidden": faint,
        "hidden.background": deep,
        "hidden.border": border,
        "ignored": faint,
        "ignored.background": deep,
        "ignored.border": border,
        "unreachable": muted,
        "unreachable.background": deep,
        "unreachable.border": border,

        # vim and helix modes: the mode speaks with a material, on the ground
        "vim.normal.background": c["blood"],
        "vim.insert.background": c["malachite"],
        "vim.replace.background": c["sealwax"],
        "vim.visual.background": c["amethyst"],
        "vim.visual_line.background": c["amethyst"],
        "vim.visual_block.background": c["amethyst"],
        "vim.helix_normal.background": c["blood"],
        "vim.helix_select.background": c["amethyst"],
        "vim.yank.background": alpha(c["amber"], 0.3),
        "vim.helix_jump_label.foreground": c["blood"],
        **{f"vim.{mode}.foreground": ground for mode in
           ("normal", "insert", "replace", "visual", "visual_line", "visual_block", "helix_normal", "helix_select")},

        **terminal(c, dim, dark),

        # Your cursor is crimson; collaborators take the other materials.
        "players": [
            {"cursor": c[m], "background": c[m], "selection": alpha(c[m], 0.24)}
            for m in ("crimson", "lapis", "malachite", "amber", "amethyst", "verdigris", "sealwax", "petal")
        ],
        "syntax": syntax(c),
    }
    return s


def family():
    themes = []
    for variant, label, dark in (("obsidian", "Cremisi Obsidian", True), ("ivory", "Cremisi Ivory", False)):
        other = VARIANTS[1 - VARIANTS.index(variant)]
        themes.append({
            "name": label,
            "appearance": "dark" if dark else "light",
            "style": style(palette(variant), palette(other), dark),
        })
    return {
        "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
        "name": "Cremisi",
        "author": "vari.sh",
        "themes": themes,
    }


def main():
    out = HERE / "themes"
    out.mkdir(exist_ok=True)
    path = out / "cremisi.json"
    path.write_text(json.dumps(family(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(path.relative_to(HERE.parent.parent))


if __name__ == "__main__":
    main()
