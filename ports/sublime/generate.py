#!/usr/bin/env python3
"""Generate the Cremisi Sublime Text colour schemes from palette.yaml.

    python3 ports/sublime/generate.py

Writes "Cremisi Obsidian.sublime-color-scheme" and "Cremisi Ivory.sublime-color-scheme".
The palette rules come first, then the roles that Sublime's own syntaxes name differently.
"""
import json
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
PALETTE = yaml.safe_load((HERE.parent.parent / "palette.yaml").read_text())

# Palette selectors that Sublime's syntaxes give a different reach; None drops one.
# Sublime resolves font_style apart from colour, so a rule without one inherits it from a wider
# rule: exclusions keep italic and bold off operators, markers and regex internals.
# Checked against the syntaxes that ship with Sublime Text build 4200.
SCOPE_SWAP = {
    # meta.function-call spans the arguments too (C, Python): call names are variable.function already.
    "meta.function-call": None,
    # Python docstrings are comment.block.documentation: they read as strings.
    "comment": "comment - comment.block.documentation.python",
    "punctuation.definition.comment": "punctuation.definition.comment - comment.block.documentation.python",
    "keyword": "keyword - keyword.operator - source.regexp - string.regexp",
    "keyword.control": "keyword.control - keyword.control.import-export - source.regexp - string.regexp",
    # A decorator's arguments are plain code, as on the page.
    "meta.annotation": "meta.annotation - meta.function-call.arguments",
    "storage.modifier": " - ".join(
        ["storage.modifier", "storage.modifier.conversion", "storage.modifier.named-args-only",
         "storage.modifier.positional-args-only", "storage.modifier.optional", "source.regexp", "string.regexp"]),
}

# Scopes that Sublime's own syntaxes name differently from the palette rules. They come after
# the palette rules, so they win ties. Python attribute access has no scope of its own:
# self.abbey and abbey are both meta.generic-name, so it stays ink.
NOT_ARGS = " - meta.function-call.arguments - meta.brackets - meta.group"
REGEX_ROLES = ("keyword.control", "keyword.operator", "keyword.other", "constant.other", "constant.character",
               "variable.other", "entity.name", "storage.modifier")
SUBLIME_RULES = [
    ("Decorators and attributes (Sublime)",
     f"variable.annotation, meta.annotation meta.generic-name{NOT_ARGS}, meta.annotation punctuation.accessor{NOT_ARGS}",
     "sealwax", None),
    ("Imports (Sublime)", "keyword.control.import-export, keyword.declaration.import", "wine", "italic"),
    ("Python docstrings (Sublime)", "comment.block.documentation.python", "malachite", None),
    ("Member access (Sublime)", "meta.property.object, meta.path.rust meta.path.rust variable.other.rust", "verdigris", None),
    ("Imported modules (Sublime)", "meta.import-name, meta.statement.import meta.path meta.generic-name", "tallow", "italic"),
    ("Type declarations (Sublime)",
     "entity.name.enum, entity.name.interface, entity.name.trait, entity.name.union, entity.name.impl, entity.name.module",
     "tallow", "italic"),
    ("Type parameters (Sublime)", "variable.parameter.generic, variable.parameter.type", "tallow", "italic"),
    ("Constant declarations (Sublime)", "entity.name.constant", "amber", None),
    ("Macros (Sublime)", "entity.name.constant.preprocessor, entity.name.macro, support.macro", "wine", None),
    ("Constructors (Sublime)", "entity.name.function.constructor.js", "blood", "italic"),
    ("Interpolations and format specs (Sublime)",
     "punctuation.section.interpolation, storage.modifier.conversion, constant.other.format-spec", "sealwax", None),
    ("Parameter and optional markers (Sublime)",
     "storage.modifier.named-args-only, storage.modifier.positional-args-only, storage.modifier.optional", "wine", None),
    ("Regex internals (Sublime)",
     ", ".join(f"{root} {role}" for root in ("source.regexp", "string.regexp") for role in REGEX_ROLES),
     "sealwax", None),
]


def colour(value):
    # Materials are scheme variables; anything else is a literal colour.
    return value if value.startswith("#") else f"var({value})"


def rule(name, scope, fg=None, bg=None, style=None):
    r = {"name": name, "scope": scope}
    if fg:
        r["foreground"] = colour(fg)
    if bg:
        r["background"] = colour(bg)
    if style:
        r["font_style"] = style
    return r


def swap(scope):
    selectors = (SCOPE_SWAP.get(s, s) for s in (x.strip() for x in scope.split(",")))
    return ", ".join(s for s in selectors if s)


def rules():
    out = [rule(r["name"], swap(r["scope"]), r.get("fg"), r.get("bg"), r.get("style")) for r in PALETTE["rules"]]
    out += [rule(name, scope, fg, style=style) for name, scope, fg, style in SUBLIME_RULES]
    return out


def scheme(variant, label):
    variables = {m["key"]: m[variant] for m in PALETTE["materials"]}
    variables.update({u["key"]: u[variant] for u in PALETTE["ui_vars"]})
    return {
        "name": label,
        "author": "vari.sh",
        "variables": variables,
        "globals": dict(PALETTE["globals"]),
        "rules": rules(),
    }


def main():
    for variant, label in (("obsidian", "Cremisi Obsidian"), ("ivory", "Cremisi Ivory")):
        path = HERE / f"{label}.sublime-color-scheme"
        path.write_text(json.dumps(scheme(variant, label), indent=2, ensure_ascii=False) + "\n")
        print(path.relative_to(HERE.parent.parent))


if __name__ == "__main__":
    main()
