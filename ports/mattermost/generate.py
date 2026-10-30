#!/usr/bin/env python3
"""Generate the Cremisi Mattermost themes from palette.yaml.

    python3 ports/mattermost/generate.py

Writes cremisi-obsidian.json and cremisi-ivory.json: the one-line JSON that Mattermost's
custom theme box exports and takes back.
"""
import json
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
PALETTE = yaml.safe_load((HERE.parent.parent / "palette.yaml").read_text(encoding="utf-8"))
VARIANTS = ("obsidian", "ivory")

def palette(variant):
    p = {m["key"]: m[variant] for m in PALETTE["materials"]}
    for scale in PALETTE["scales"]:
        for step in scale["steps"]:
            p[f'{scale["key"]}-{step["n"]}'] = step["hex"]
    return p

COLOURS = {v: palette(v) for v in VARIANTS}

# Mattermost key -> (Obsidian, Ivory), each a material or a scale step.
# In the order of Mattermost's custom theme panel; the sidebar is the sunken stone of scale_ui.
ROLES = {
    # Sidebar
    "sidebarBg": ("stone-950", "stone-100"),
    "sidebarText": ("ink", "ink"),
    "sidebarHeaderBg": ("stone-950", "stone-200"),
    "sidebarTeamBarBg": ("stone-950", "stone-200"),
    "sidebarHeaderTextColor": ("ink", "ink"),
    "sidebarUnreadText": ("tallow", "blood-700"),
    "sidebarTextHoverBg": ("stone-800", "stone-200"),
    "sidebarTextActiveBorder": ("crimson", "crimson"),
    "sidebarTextActiveColor": ("ink", "ink"),
    "onlineIndicator": ("malachite", "malachite"),
    "awayIndicator": ("amber", "amber"),
    "dndIndicator": ("blood", "blood"),
    "mentionBg": ("blood", "blood"),
    "mentionColor": ("stone-950", "stone-50"),
    # Center channel
    "centerChannelBg": ("ground", "ground"),
    "centerChannelColor": ("ink", "ink"),
    "newMessageSeparator": ("blood", "blood"),
    "errorTextColor": ("blood", "blood"),
    "mentionHighlightBg": ("blood-950", "blood-50"),
    "mentionHighlightLink": ("petal", "petal"),
    # Links and buttons
    "linkColor": ("lapis", "lapis"),
    "buttonBg": ("crimson", "crimson"),
    "buttonColor": ("stone-50", "stone-50"),
}

# Mattermost highlights code with one of four fixed themes: none of them speaks the materials.
CODE_THEME = {"obsidian": "monokai", "ivory": "github"}

def theme(variant):
    i = VARIANTS.index(variant)
    t = {key: COLOURS[variant][refs[i]] for key, refs in ROLES.items()}
    # mentionBj is the old misspelling of mentionBg: Mattermost reads it only when mentionBg is missing.
    t["mentionBj"] = t["mentionBg"]
    t["codeTheme"] = CODE_THEME[variant]
    return json.dumps(t, sort_keys=True, separators=(",", ":")) + "\n"

def main():
    for variant in VARIANTS:
        path = HERE / f"cremisi-{variant}.json"
        path.write_text(theme(variant), encoding="utf-8", newline="\n")
        print(f"wrote {path.relative_to(HERE.parent.parent)}")

if __name__ == "__main__":
    main()
