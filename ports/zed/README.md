# Cremisi for Zed

Both variants in one theme family for [Zed](https://zed.dev): **Cremisi Obsidian** (dark) and **Cremisi Ivory** (light),
editor and interface together.

## Install

As a dev extension: open the extensions page (`ctrl-shift-x`), click *Install Dev Extension* and pick this folder,
`ports/zed`, the one that holds `extension.toml`.

Or as a local theme: copy `themes/cremisi.json` into `~/.config/zed/themes` (macOS and Linux) or
`%APPDATA%\Zed\themes` (Windows). Zed reads it the next time it starts.

## Use

Open the theme selector (`ctrl-k ctrl-t`, or **theme selector: toggle** from the command palette)
and pick *Cremisi Obsidian* or *Cremisi Ivory*. To follow the system appearance, set both in your settings:

```json
"theme": {
  "mode": "system",
  "light": "Cremisi Ivory",
  "dark": "Cremisi Obsidian"
}
```

## Roles

- **Syntax** speaks the roles of the palette rules, translated into the capture names of Zed's Tree-sitter queries.
  The theme also styles the names that semantic tokens look up, for `"semantic_tokens": "combined"`.
- **The interface** is built from the stone and blood scales: the editor lies on the ground, panels, tabs,
  title and status bars on the sunken stone. Crimson is the only accent: cursor, selection, focus, the selected entry.
- **Your cursor** is crimson; collaborators take lapis, malachite, amber, amethyst, verdigris, sealing wax and petal.
- **The terminal** takes its sixteen colours from the materials; the dim ones are the same materials read from the
  other variant, darker on Obsidian and paler on Ivory.

Every code token clears 4.5:1 against its own background; only comments, the smoke of incense, may fall below.

## What Zed cannot tell apart

Zed's queries name some roles more broadly than Sublime Text and VS Code do, so a few tokens take a neighbour's colour:

- **Python** captures every keyword alike: `if`, `return` and `import` are blood italic, like `def`.
  **Rust** does the same for `use` and `mod`, which stay blood rather than wine.
- **Null** shares its capture with CSS keyword values (`flex`, `none`) and C++ all-caps names, and booleans and
  null are blood in JSON and YAML too, where the other ports make them amber.
- **YAML keys** are properties, in verdigris; anchors and tags are types, in tallow.
- **Attributes** are one capture in HTML and in Rust or C: `#[derive]` is tallow, like `class=`, not sealing wax.
- **Special punctuation** is sealing wax: the braces of interpolations, and in TypeScript the `:`, `|` and `?` of types.
- **Markdown headings** have one level: all are blood.

## Built, not drawn

The theme is generated from the same `palette.yaml` as the other ports and the page:

```sh
python3 ports/zed/generate.py      # from the root of vari-sh/Cremisi-Theme
```

`generate.py` maps each Zed capture to a material; a capture without its own entry falls back to its longest
defined prefix, so `keyword.control.return` reads `keyword.control`. Checked against the queries that ship with Zed 1.26.
