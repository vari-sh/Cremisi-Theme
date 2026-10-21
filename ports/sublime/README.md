# Cremisi for Sublime Text

Both variants as `.sublime-color-scheme` files: **Obsidian** (dark) and **Ivory** (light).

## Install

1. Copy both files into your `Packages/User` folder (*Preferences → Browse Packages…*).
2. Run **UI: Select Color Scheme** from the command palette and pick *Cremisi Obsidian* or *Cremisi Ivory*.

To follow the system appearance, set both in your preferences:

```json
"color_scheme": "auto",
"light_color_scheme": "Cremisi Ivory.sublime-color-scheme",
"dark_color_scheme": "Cremisi Obsidian.sublime-color-scheme"
```

## Built, not drawn

Both schemes are generated from the same `palette.yaml` as the VS Code port and the page,
so a change of palette reaches every editor at once:

```sh
python3 ports/sublime/generate.py      # from the root of vari-sh/Cremisi-Theme
```

The palette rules come first; `generate.py` then adds the roles that Sublime's own syntaxes
name differently, checked against Sublime Text build 4200. Python attribute access has no scope
of its own in Sublime, so `self.abbey` stays in ink.
