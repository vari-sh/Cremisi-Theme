#!/usr/bin/env python3
"""Generate the Cremisi Typora themes from palette.yaml.

    python3 ports/typora/generate.py

Writes cremisi-obsidian.css and cremisi-ivory.css: the --cr-* variables that
cremisi/cremisi-base.css reads. The base stylesheet is drawn by hand and holds no colour of its own.
"""
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
PALETTE = yaml.safe_load((HERE.parent.parent / "palette.yaml").read_text(encoding="utf-8"))

def palette(variant):
    p = {m["key"]: m[variant] for m in PALETTE["materials"]}
    for scale in PALETTE["scales"]:
        for step in scale["steps"]:
            p[f'{scale["key"]}-{step["n"]}'] = step["hex"]
    return p

COLOURS = {v: palette(v) for v in ("obsidian", "ivory")}

def rgba(hex_colour, a):
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    return f"rgba({r}, {g}, {b}, {a:g})".replace(" 0.", " .")

# A reference is a material or a scale step; "obsidian:amber" pins the other variant's value.
# A (reference, alpha) pair becomes an rgba() of that colour.
def resolve(variant, ref):
    if isinstance(ref, tuple):
        return rgba(resolve(variant, ref[0]), ref[1])
    if ":" in ref:
        variant, ref = ref.split(":")
    return COLOURS[variant][ref]

MATERIALS = ("lapis", "tallow", "amber", "sealwax", "malachite", "verdigris", "amethyst", "wine", "petal")

VARIANTS = {
    "obsidian": {
        "title": "Cremisi Obsidian",
        "line": "A gothic, arcane colour scheme. Blood is the protagonist, bone is the text, stone is the ground.",
        "scheme": "dark", "mermaid": "dark", "text": "bone",
        "stone": [("void", "stone-950"), ("crypt", "stone-950"), ("ground", "stone-900"),
                  ("border", "stone-800"), ("border-2", "stone-700"), ("gutter", "stone-700")],
        "ink": [("ink", "ink"), ("ink-dim", "stone-200"), ("side-fg", "ink"), ("iron", "iron"),
                ("incense", "incense")],
        "blood": [("title", "blood-500"), ("link", "blood-400"), ("link-line", ("blood-400", .35))],
        "title-shadow": lambda c: f"0 3px 0 rgba(0, 0, 0, .55), 0 0 36px {rgba(c['blood-500'], .25)}",
        "tallow-line": ("tallow", .35),
        "interface": [("sel", ("crimson", .38)), ("sel-fg", "stone-50"), ("sel-soft", ("crimson", .16)),
                      ("sel-faint", ("crimson", .06)), ("hover", ("ink", .06)), ("zebra", ("ink", .018)),
                      ("mark", ("amber", .26)), ("mark-fg", "ink"), ("glow", ("crimson", .13)),
                      ("glow-strong", ("crimson", .45)), ("scroll", ("ink", .12)), ("scroll-hover", ("ink", .22))],
        "code-shadow": "0 12px 30px -20px rgba(0, 0, 0, .8)",
    },
    "ivory": {
        "title": "Cremisi Ivory",
        "line": "The same stone, read from the opposite end: vellum ground, scriptorium ink, the same crimson.",
        "scheme": "light", "mermaid": "default", "text": "ink",
        "stone": [("void", "stone-900"), ("crypt", "stone-100"), ("ground", "stone-50"),
                  ("border", "stone-200"), ("border-2", "stone-300"), ("gutter", "stone-300")],
        "ink": [("ink", "ink"), ("ink-dim", "stone-700"), ("side-fg", "stone-900"), ("iron", "iron"),
                ("incense", "incense")],
        "blood": [("title", "blood-700"), ("link", "blood-700"), ("link-line", ("blood-700", .3))],
        "title-shadow": None,
        "tallow-line": ("tallow", .4),
        # The highlighter keeps Obsidian's amber: Ivory's own is too dark to read through.
        "interface": [("sel", ("crimson", .24)), ("sel-fg", "ink"), ("sel-soft", ("crimson", .12)),
                      ("sel-faint", ("crimson", .05)), ("hover", ("ink", .06)), ("zebra", ("ink", .025)),
                      ("mark", ("obsidian:amber", .32)), ("mark-fg", "ink"), ("glow", ("crimson", .07)),
                      ("glow-strong", ("crimson", .28)), ("scroll", ("ink", .16)), ("scroll-hover", ("ink", .28))],
        "code-shadow": None,
    },
}

# Shared by both variants: tooltips are dark stone with bone text, buttons crimson with bone text.
COMMON = [("void-fg", "stone-100"), ("on-accent", "stone-50"), ("accent-top", "blood-600"),
          ("accent-bottom", "blood-700"), ("backdrop", ("stone-950", .6))]

def theme(variant):
    v = VARIANTS[variant]
    c = COLOURS[variant]

    def block(label, pairs):
        return [f"  /* {label} */"] + [f"  --cr-{k}: {resolve(variant, ref)};" for k, ref in pairs] + [""]

    lines = [
        "/*",
        f" * {v['title']} — Typora theme",
        f" * {v['line']}",
        " * Based on Cremisi by vari.sh — https://vari-sh.github.io/cremisi/",
        " * Generated from palette.yaml by generate.py: edit the palette, not this file.",
        " */",
        "",
        '@import "cremisi/cremisi-base.css";',
        "",
        ":root {",
        f"  color-scheme: {v['scheme']};",
        f"  --mermaid-theme: {v['mermaid']};",
        "",
    ]
    lines += block("stone", v["stone"])
    lines += block(v["text"], v["ink"])
    lines += [
        "  /* blood */",
        f"  --cr-crimson: {c['crimson']};",
        f"  --cr-crimson-deep: {c['crimson_deep']};",
        f"  --cr-blood: {c['blood']};",
        f"  --cr-title: {resolve(variant, v['blood'][0][1])};",
        f"  --cr-title-shadow: {v['title-shadow'](c) if v['title-shadow'] else 'none'};",
    ]
    lines += [f"  --cr-{k}: {resolve(variant, ref)};" for k, ref in v["blood"][1:]] + [""]
    lines += ["  /* materials */"]
    for m in MATERIALS:
        lines.append(f"  --cr-{m}: {c[m]};")
        if m == "tallow":
            lines.append(f"  --cr-tallow-line: {resolve(variant, v['tallow-line'])};")
    lines += [""]
    lines += block("interface", v["interface"] + COMMON)[:-1]
    lines += [f"  --cr-code-shadow: {v['code-shadow'] or 'none'};", "}", ""]
    return "\n".join(lines)

def main():
    for variant in VARIANTS:
        path = HERE / f"cremisi-{variant}.css"
        path.write_text(theme(variant), encoding="utf-8", newline="\n")
        print(f"wrote {path.relative_to(HERE.parent.parent)}")

if __name__ == "__main__":
    main()
