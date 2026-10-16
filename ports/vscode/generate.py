#!/usr/bin/env python3
"""Generate the Cremisi VS Code themes from palette.yaml.

    python3 ports/vscode/generate.py

Writes themes/cremisi-obsidian-color-theme.json and themes/cremisi-ivory-color-theme.json.
Token colours come from the same rules as the Sublime Text port; the workbench is built
from the materials and the stone and blood scales.
"""
import json
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
PALETTE = yaml.safe_load((HERE.parent.parent / "palette.yaml").read_text())

STYLES = {"italic": "italic", "bold": "bold", "bold italic": "bold italic", "underline": "underline"}
JS_LANGS = ("javascript", "javascriptreact", "typescript", "typescriptreact")

# Sublime selectors that VS Code's grammars give a different reach. meta.function-call
# spans the arguments too in VS Code (C, Python), so only the generic call name stays.
SCOPE_SWAP = {"meta.function-call": "meta.function-call.generic"}

# Scopes that VS Code's own grammars name differently from Sublime Text's.
# They come after the palette rules, so they win ties. Checked with vscode-textmate
# against the grammars that ship with VS Code.
JS_TS = ("js", "jsx", "ts", "tsx")
VSCODE_RULES = [
    ("Declaration keywords (VS Code)", ", ".join(
        ["storage.type.struct", "storage.type.enum", "storage.type.union", "storage.type.interface",
         "storage.type.type", "storage.type.namespace", "storage.type.rust"]
        + [f"storage.type.{x}" for x in JS_TS]), "blood", "italic"),
    ("Preprocessor (VS Code)", "keyword.control.directive, meta.preprocessor punctuation.definition.directive", "wine", "italic"),
    ("Macros (VS Code)", "entity.name.function.preprocessor, entity.name.function.macro", "wine", None),
    ("JSON keys (VS Code)", "support.type.property-name.json", "lapis", None),
    ("Object literal keys (VS Code)", "meta.object-literal.key", "lapis", None),
    ("JSON colons (VS Code)", "punctuation.separator.dictionary.key-value", "wine", None),
    ("YAML colons (VS Code)", "punctuation.separator.map", "wine", None),
    ("YAML directives (VS Code)", "meta.directives.yaml punctuation.definition.directive", "wine", None),
    ("YAML anchors and aliases (VS Code)", "keyword.control.flow.anchor.yaml, keyword.control.flow.alias.yaml, variable.other.anchor.yaml", "amethyst", None),
    ("Decorators (VS Code)", "entity.name.function.decorator, punctuation.definition.decorator, meta.function.decorator support.type, meta.attribute.rust", "sealwax", None),
    ("Format placeholders (VS Code)", "constant.character.format.placeholder, storage.type.format", "sealwax", None),
    ("Regex internals (VS Code)", "string.regexp constant.other, string.regexp constant.character, string.regexp keyword.control, string.regexp keyword.operator, string.regexp keyword.other, string.regexp support.other", "sealwax", None),
    ("Number prefixes and suffixes (VS Code)", "constant.numeric storage.type.number, keyword.other.unit", "amber", None),
    ("Python self parameter (VS Code)", "variable.parameter.function.language.special.self", "amethyst", "italic"),
    ("Properties (VS Code)", "meta.attribute.python, variable.object.property, variable.other.constant.property", "verdigris", None),
    # Every JS/TS `const` binding is variable.other.constant: keep it plain ink, as Sublime does.
    ("JS/TS const bindings (VS Code)", ", ".join(f"variable.other.constant.{x}" for x in JS_TS), "ink", None),
    ("Markdown inline code (VS Code)", "markup.inline.raw", "malachite", None),
    ("Markdown link text (VS Code)", "string.other.link", "lapis", None),
    ("Markdown list marks (VS Code)", "punctuation.definition.list.begin.markdown", "blood", None),
    ("Round braces (VS Code)", "meta.brace, storage.modifier.array.bracket", "iron", None),
]


def alpha(hex_colour, a):
    return f"{hex_colour}{round(a * 255):02x}"


def palette(variant):
    p = {m["key"]: m[variant] for m in PALETTE["materials"]}
    p.update({u["key"]: u[variant] for u in PALETTE["ui_vars"]})
    for scale in PALETTE["scales"]:
        for step in scale["steps"]:
            p[f'{scale["key"]}-{step["n"]}'] = step["hex"]
    return p


def token_colors(c):
    out = []
    levels = {int(r["scope"][-1]): r for r in PALETTE["rules"] if r["scope"].startswith("markup.heading.")}
    for rule in PALETTE["rules"]:
        if rule.get("bg"):
            # Token colours cannot set a background: mark invalid code as blood and underlined
            # (crimson alone is 3.16:1 on Obsidian).
            settings = {"foreground": c["blood"], "fontStyle": "underline"}
        else:
            # An unset fontStyle inherits from a wider rule (keyword.operator would turn italic
            # under keyword): every rule states its own, roman when none is given.
            settings = {"foreground": c[rule["fg"]], "fontStyle": STYLES.get(rule.get("style"), "")}
        out.append({
            "name": rule["name"],
            "scope": [SCOPE_SWAP.get(x.strip(), x.strip()) for x in rule["scope"].split(",")],
            "settings": settings,
        })
    for name, scope, fg, style in VSCODE_RULES:
        settings = {"foreground": c[fg], "fontStyle": style or ""}
        out.append({"name": name, "scope": [x.strip() for x in scope.split(",")], "settings": settings})
    for n, rule in sorted(levels.items()):
        out.append({
            "name": f"Markdown h{n} (VS Code)",
            "scope": [f"heading.{n}.markdown entity.name.section"],
            "settings": {"foreground": c[rule["fg"]], "fontStyle": STYLES.get(rule.get("style"), "")},
        })
    return out


def semantic_token_colors(c):
    def role(fg, style=""):
        return {"foreground": c[fg], "fontStyle": style}
    s = {
        "function": role("lapis", "italic"),
        "method": role("lapis", "italic"),
        "parameter": role("petal", "italic"),
        "property": role("verdigris"),
        "variable": role("ink"),
        "variable.readonly": role("amber"),
        "enumMember": role("amber"),
        "decorator": role("sealwax"),
        "macro": role("wine"),
        "selfKeyword": role("amethyst", "italic"),
        "selfParameter": role("amethyst", "italic"),
        "*.defaultLibrary": role("amethyst", "italic"),
        "variable.typeHint:python": role("tallow", "italic"),
    }
    # Types keep tallow, builtin ones too: support.type is tallow in the token rules.
    for kind in ("type", "class", "interface", "struct", "namespace", "enum", "typeParameter"):
        s[kind] = role("tallow", "italic")
        s[f"{kind}.defaultLibrary"] = role("tallow", "italic")
    # `const` is readonly in JS and TS: amber would paint every binding, so they stay ink.
    for lang in JS_LANGS:
        s[f"variable.readonly:{lang}"] = role("ink")
        s[f"property.readonly:{lang}"] = role("verdigris")
    return s


def workbench(c, dark):
    if dark:
        ground, deep, raised, border, field = c["stone-900"], c["stone-950"], c["stone-800"], c["stone-800"], c["stone-700"]
        text, muted, faint = c["stone-100"], c["stone-400"], c["stone-600"]
        link, alert_bg, removed_line, removed_text = c["blood-400"], c["blood-950"], c["blood-950"], c["blood-900"]
    else:
        ground, deep, raised, border, field = c["stone-50"], c["stone-100"], c["stone-100"], c["stone-200"], c["stone-300"]
        text, muted, faint = c["stone-900"], c["stone-600"], c["stone-400"]
        link, alert_bg, removed_line, removed_text = c["blood-700"], c["blood-50"], c["blood-50"], c["blood-100"]

    # crimson is the only accent: focus, badges, cursor, active tab, primary buttons.
    accent, on_accent = c["blood-600"], c["stone-50"]
    selection = alpha(c["crimson"], 0.24)
    hover = alpha(c["ink"], 0.06)

    colors = {
        # base
        "foreground": text,
        "descriptionForeground": muted,
        "disabledForeground": faint,
        "errorForeground": c["blood"],
        "focusBorder": alpha(accent, 0.7),
        "icon.foreground": muted,
        "selection.background": selection,
        "widget.border": border,
        "widget.shadow": alpha("#000000", 0.4 if dark else 0.12),
        "sash.hoverBorder": accent,
        "textLink.foreground": link,
        "textLink.activeForeground": c["blood"],
        "textBlockQuote.background": deep,
        "textBlockQuote.border": accent,
        "textCodeBlock.background": deep,
        "textPreformat.foreground": c["malachite"],
        "textSeparator.foreground": border,

        # editor
        "editor.background": ground,
        "editor.foreground": c["ink"],
        "editorCursor.foreground": accent,
        "editor.lineHighlightBackground": alpha(c["ink"], 0.05),
        "editor.lineHighlightBorder": "#00000000",
        "editor.selectionBackground": selection,
        "editor.inactiveSelectionBackground": alpha(c["crimson"], 0.12),
        "editor.selectionHighlightBackground": alpha(c["crimson"], 0.14),
        "editor.wordHighlightBackground": alpha(c["ink"], 0.08),
        "editor.wordHighlightStrongBackground": alpha(c["ink"], 0.12),
        "editor.findMatchBackground": alpha(c["amber"], 0.45),
        "editor.findMatchBorder": c["amber"],
        "editor.findMatchHighlightBackground": alpha(c["amber"], 0.2),
        "editor.findRangeHighlightBackground": alpha(c["amber"], 0.08),
        "editor.rangeHighlightBackground": alpha(c["ink"], 0.05),
        "editor.hoverHighlightBackground": alpha(c["lapis"], 0.15),
        "editorLink.activeForeground": link,
        "editorLineNumber.foreground": c["gutter_fg"],
        "editorLineNumber.activeForeground": c["blood"],
        "editorWhitespace.foreground": alpha(c["ink"], 0.12),
        "editorIndentGuide.background1": alpha(c["ink"], 0.06),
        "editorIndentGuide.activeBackground1": alpha(c["ink"], 0.16),
        "editorRuler.foreground": alpha(c["ink"], 0.08),
        "editorBracketMatch.background": alpha(c["blood"], 0.15),
        "editorBracketMatch.border": alpha(c["blood"], 0.6),
        "editorBracketHighlight.foreground1": c["blood"],
        "editorBracketHighlight.foreground2": c["amber"],
        "editorBracketHighlight.foreground3": c["lapis"],
        "editorBracketHighlight.foreground4": c["malachite"],
        "editorBracketHighlight.foreground5": c["amethyst"],
        "editorBracketHighlight.foreground6": c["sealwax"],
        "editorBracketHighlight.unexpectedBracket.foreground": c["crimson"],
        "editorCodeLens.foreground": muted,
        "editorInlayHint.foreground": muted,
        "editorInlayHint.background": alpha(c["ink"], 0.05),
        "editorGutter.background": ground,
        "editorGutter.addedBackground": c["malachite"],
        "editorGutter.modifiedBackground": c["amber"],
        "editorGutter.deletedBackground": c["blood"],
        "editorGutter.foldingControlForeground": muted,
        "editorError.foreground": c["blood"],
        "editorWarning.foreground": c["amber"],
        "editorInfo.foreground": c["lapis"],
        "editorHint.foreground": c["verdigris"],
        "editorUnnecessaryCode.opacity": "#00000088",
        "editorOverviewRuler.border": "#00000000",
        "editorOverviewRuler.errorForeground": c["blood"],
        "editorOverviewRuler.warningForeground": c["amber"],
        "editorOverviewRuler.infoForeground": c["lapis"],
        "editorOverviewRuler.findMatchForeground": c["amber"],
        "editorOverviewRuler.selectionHighlightForeground": alpha(c["crimson"], 0.6),
        "editorOverviewRuler.addedForeground": c["malachite"],
        "editorOverviewRuler.modifiedForeground": c["amber"],
        "editorOverviewRuler.deletedForeground": c["blood"],
        "editorWidget.background": deep,
        "editorWidget.foreground": text,
        "editorWidget.border": border,
        "editorSuggestWidget.background": deep,
        "editorSuggestWidget.border": border,
        "editorSuggestWidget.foreground": text,
        "editorSuggestWidget.highlightForeground": c["blood"],
        "editorSuggestWidget.focusHighlightForeground": c["blood"],
        "editorSuggestWidget.selectedBackground": selection,
        "editorHoverWidget.background": deep,
        "editorHoverWidget.border": border,
        "editorGroup.border": border,
        "editorGroup.dropBackground": alpha(c["crimson"], 0.12),
        "editorGroupHeader.tabsBackground": deep,
        "editorGroupHeader.tabsBorder": border,
        "editorGroupHeader.noTabsBackground": ground,
        "editorStickyScroll.background": ground,
        "editorStickyScrollHover.background": raised,
        "minimap.background": ground,
        "minimap.selectionHighlight": alpha(c["crimson"], 0.5),
        "minimap.findMatchHighlight": alpha(c["amber"], 0.6),
        "minimapGutter.addedBackground": c["malachite"],
        "minimapGutter.modifiedBackground": c["amber"],
        "minimapGutter.deletedBackground": c["blood"],
        "minimapSlider.background": alpha(c["ink"], 0.08),
        "minimapSlider.hoverBackground": alpha(c["ink"], 0.12),
        "minimapSlider.activeBackground": alpha(c["ink"], 0.16),

        # diff
        "diffEditor.insertedTextBackground": alpha(c["malachite"], 0.15),
        "diffEditor.insertedLineBackground": alpha(c["malachite"], 0.08),
        # Removed grounds are clotted blood on Obsidian, petal on Ivory; slightly
        # translucent, as VS Code asks, so selections show through.
        "diffEditor.removedTextBackground": alpha(removed_text, 0.85),
        "diffEditor.removedLineBackground": alpha(removed_line, 0.85),
        "diffEditor.border": border,

        # tabs
        "tab.activeBackground": ground,
        "tab.activeForeground": text,
        "tab.activeBorderTop": accent,
        "tab.activeBorder": ground,
        "tab.inactiveBackground": deep,
        "tab.inactiveForeground": muted,
        "tab.hoverBackground": raised,
        "tab.border": border,
        "tab.unfocusedActiveForeground": muted,
        "tab.unfocusedActiveBorderTop": alpha(accent, 0.4),
        "tab.activeModifiedBorder": c["amber"],

        # chrome
        "titleBar.activeBackground": deep,
        "titleBar.activeForeground": text,
        "titleBar.inactiveBackground": deep,
        "titleBar.inactiveForeground": muted,
        "titleBar.border": border,
        "activityBar.background": deep,
        "activityBar.foreground": text,
        "activityBar.inactiveForeground": faint,
        "activityBar.activeBorder": accent,
        "activityBar.border": border,
        "activityBarBadge.background": accent,
        "activityBarBadge.foreground": on_accent,
        "sideBar.background": deep,
        "sideBar.foreground": text,
        "sideBar.border": border,
        "sideBarTitle.foreground": muted,
        "sideBarSectionHeader.background": deep,
        "sideBarSectionHeader.foreground": text,
        "sideBarSectionHeader.border": border,
        "statusBar.background": deep,
        "statusBar.foreground": muted,
        "statusBar.border": border,
        "statusBar.noFolderBackground": deep,
        "statusBar.debuggingBackground": accent,
        "statusBar.debuggingForeground": on_accent,
        "statusBarItem.hoverBackground": hover,
        "statusBarItem.remoteBackground": accent,
        "statusBarItem.remoteForeground": on_accent,
        # The status bar stays sober: crimson only for debugging and remote.
        "statusBarItem.errorBackground": deep,
        "statusBarItem.errorForeground": c["blood"],
        "statusBarItem.warningBackground": deep,
        "statusBarItem.warningForeground": c["amber"],
        "statusBarItem.prominentBackground": raised,
        "statusBarItem.prominentHoverBackground": field,
        "panel.background": ground,
        "panel.border": border,
        "panelTitle.activeForeground": text,
        "panelTitle.inactiveForeground": muted,
        "panelTitle.activeBorder": accent,
        "breadcrumb.foreground": muted,
        "breadcrumb.focusForeground": text,
        "breadcrumb.activeSelectionForeground": c["blood"],
        "breadcrumbPicker.background": deep,
        "commandCenter.background": ground,
        "commandCenter.foreground": muted,
        "commandCenter.border": border,

        # lists and trees
        "list.activeSelectionBackground": selection,
        "list.activeSelectionForeground": text,
        "list.inactiveSelectionBackground": alpha(c["crimson"], 0.12),
        "list.hoverBackground": hover,
        "list.focusOutline": alpha(accent, 0.7),
        "list.highlightForeground": c["blood"],
        "list.focusHighlightForeground": c["blood"],
        "list.errorForeground": c["blood"],
        "list.warningForeground": c["amber"],
        "list.dropBackground": alpha(c["crimson"], 0.12),
        "tree.indentGuidesStroke": alpha(c["ink"], 0.12),

        # inputs and controls
        "input.background": ground,
        "input.foreground": text,
        "input.border": field,
        "input.placeholderForeground": muted,
        "inputOption.activeBorder": accent,
        "inputOption.activeBackground": alpha(c["crimson"], 0.2),
        "inputValidation.errorBackground": alert_bg,
        "inputValidation.errorBorder": c["blood"],
        "inputValidation.warningBackground": deep,
        "inputValidation.warningBorder": c["amber"],
        "inputValidation.infoBackground": deep,
        "inputValidation.infoBorder": c["lapis"],
        "dropdown.background": deep,
        "dropdown.border": field,
        "dropdown.foreground": text,
        "dropdown.listBackground": deep,
        "checkbox.background": ground,
        "checkbox.border": field,
        "checkbox.foreground": text,
        "button.background": accent,
        "button.foreground": on_accent,
        "button.hoverBackground": c["blood-700"],
        "button.secondaryBackground": raised,
        "button.secondaryForeground": text,
        "button.secondaryHoverBackground": field,
        "badge.background": accent,
        "badge.foreground": on_accent,
        "progressBar.background": accent,
        "scrollbar.shadow": alpha("#000000", 0.3 if dark else 0.08),
        "scrollbarSlider.background": alpha(c["ink"], 0.12),
        "scrollbarSlider.hoverBackground": alpha(c["ink"], 0.2),
        "scrollbarSlider.activeBackground": alpha(c["ink"], 0.28),
        "quickInput.background": deep,
        "quickInput.foreground": text,
        "quickInputList.focusBackground": selection,
        "quickInputList.focusForeground": text,
        "pickerGroup.foreground": c["blood"],
        "pickerGroup.border": border,
        "quickInputTitle.background": raised,
        "keybindingLabel.background": raised,
        "keybindingLabel.foreground": text,
        "keybindingLabel.border": field,
        "keybindingLabel.bottomBorder": field,
        "menu.background": deep,
        "menu.foreground": text,
        "menu.border": border,
        "menu.selectionBackground": selection,
        "menu.selectionForeground": text,
        "menu.separatorBackground": border,
        "notifications.background": deep,
        "notifications.foreground": text,
        "notifications.border": border,
        "notificationCenterHeader.background": raised,
        "notificationsErrorIcon.foreground": c["blood"],
        "notificationsWarningIcon.foreground": c["amber"],
        "notificationsInfoIcon.foreground": c["lapis"],
        "notificationLink.foreground": link,
        "peekView.border": accent,
        "peekViewEditor.background": deep,
        "peekViewEditor.matchHighlightBackground": alpha(c["amber"], 0.3),
        "peekViewResult.background": deep,
        "peekViewResult.selectionBackground": selection,
        "peekViewResult.matchHighlightBackground": alpha(c["amber"], 0.3),
        "peekViewTitle.background": raised,
        "peekViewTitleLabel.foreground": text,
        "peekViewTitleDescription.foreground": muted,

        # git and source control
        "gitDecoration.addedResourceForeground": c["malachite"],
        "gitDecoration.modifiedResourceForeground": c["amber"],
        "gitDecoration.deletedResourceForeground": c["blood"],
        "gitDecoration.stageModifiedResourceForeground": c["amber"],
        "gitDecoration.stageDeletedResourceForeground": c["blood"],
        "gitDecoration.renamedResourceForeground": c["verdigris"],
        "gitDecoration.untrackedResourceForeground": c["malachite"],
        "gitDecoration.ignoredResourceForeground": faint,
        "gitDecoration.conflictingResourceForeground": c["sealwax"],
        "gitDecoration.submoduleResourceForeground": c["lapis"],

        # terminal
        "terminal.background": ground,
        "terminal.foreground": c["ink"],
        "terminal.border": border,
        "terminal.selectionBackground": selection,
        "terminalCursor.foreground": accent,
        "terminal.ansiRed": c["blood"],
        "terminal.ansiGreen": c["malachite"],
        "terminal.ansiYellow": c["amber"],
        "terminal.ansiBlue": c["lapis"],
        "terminal.ansiMagenta": c["amethyst"],
        "terminal.ansiCyan": c["verdigris"],
        "terminal.ansiBrightGreen": c["malachite"],
        "terminal.ansiBrightYellow": c["tallow"],
        "terminal.ansiBrightBlue": c["lapis"],
        "terminal.ansiBrightMagenta": c["petal"],
        "terminal.ansiBrightCyan": c["verdigris"],

        # debug and misc
        "debugToolBar.background": deep,
        "editor.stackFrameHighlightBackground": alpha(c["amber"], 0.15),
        "editor.focusedStackFrameHighlightBackground": alpha(c["malachite"], 0.15),
        "debugIcon.breakpointForeground": c["crimson"],
        "settings.headerForeground": text,
        "settings.modifiedItemIndicator": c["amber"],
        "welcomePage.tileBackground": deep,
        "walkThrough.embeddedEditorBackground": deep,
        "charts.red": c["blood"],
        "charts.orange": c["sealwax"],
        "charts.yellow": c["amber"],
        "charts.green": c["malachite"],
        "charts.blue": c["lapis"],
        "charts.purple": c["amethyst"],
        "charts.foreground": text,
        "charts.lines": border,
    }
    if dark:
        colors.update({
            "terminal.ansiBlack": c["stone-800"],
            "terminal.ansiWhite": c["stone-200"],
            "terminal.ansiBrightBlack": c["stone-500"],  # stone-600 is 2.97:1, under 3:1
            "terminal.ansiBrightRed": c["blood-400"],
            "terminal.ansiBrightWhite": c["stone-50"],
        })
    else:
        colors.update({
            "terminal.ansiBlack": c["ink"],
            "terminal.ansiWhite": c["stone-300"],
            "terminal.ansiBrightBlack": c["stone-500"],
            "terminal.ansiBrightRed": c["blood-700"],
            "terminal.ansiBrightWhite": c["stone-200"],
        })
    return colors


def theme(variant, label, dark):
    c = palette(variant)
    return {
        "$schema": "vscode://schemas/color-theme",
        "name": label,
        "type": "dark" if dark else "light",
        "semanticHighlighting": True,
        "colors": workbench(c, dark),
        "semanticTokenColors": semantic_token_colors(c),
        "tokenColors": token_colors(c),
    }


def main():
    out = HERE / "themes"
    out.mkdir(exist_ok=True)
    for variant, label, dark in (("obsidian", "Cremisi Obsidian", True), ("ivory", "Cremisi Ivory", False)):
        path = out / f"cremisi-{variant}-color-theme.json"
        path.write_text(json.dumps(theme(variant, label, dark), indent=2, ensure_ascii=False) + "\n")
        print(path.relative_to(HERE.parent.parent))


if __name__ == "__main__":
    main()
