# Cremisi for VS Code

Both variants as a VS Code extension: **Cremisi Obsidian** (dark) and **Cremisi Ivory** (light).
Works in VS Code, VSCodium and other editors built on it.

## Install

From a packaged extension:

```sh
npx @vscode/vsce package          # in this folder: builds cremisi-theme-0.1.0.vsix
code --install-extension cremisi-theme-0.1.0.vsix
```

Or link the folder into your extensions directory and reload the window
(`~/.vscode/extensions`, or `~/.vscode-oss/extensions` for VSCodium):

```sh
ln -s "$PWD" ~/.vscode/extensions/vari-sh.cremisi-theme-0.1.0
```

Then run **Preferences: Color Theme** and pick *Cremisi Obsidian* or *Cremisi Ivory*.
To follow the system appearance:

```json
"window.autoDetectColorScheme": true,
"workbench.preferredDarkColorTheme": "Cremisi Obsidian",
"workbench.preferredLightColorTheme": "Cremisi Ivory"
```

## How it is built

`generate.py` writes both themes from [`palette.yaml`](../../palette.yaml):

```sh
python3 ports/vscode/generate.py
```

- **Syntax** uses the same TextMate rules as the Sublime Text port, plus a few scopes that VS Code's grammars
  name differently (JSON keys and colons, Python decorators, format placeholders). Semantic highlighting is on,
  with `self`, builtins, decorators and parameters mapped to their materials, and `const` in JavaScript and
  TypeScript kept as plain ink rather than constant amber.
- **The workbench** is built from the stone and blood scales: stone for grounds, borders and text,
  blood for the accent, badges and alerts, as in the `scale_ui` recipe.
- **The terminal** maps the ANSI colours to the materials.
