# Cremisi for Sublime Text

Both variants as `.sublime-color-scheme` files: **Obsidian** (dark) and **Ivory** (light).

## Install

From [Package Control](https://packagecontrol.io/packages/Cremisi%20Color%20Scheme): run
**Package Control: Install Package** from the command palette and pick *Cremisi Color Scheme*.

Without Package Control or offline, download the `.sublime-package` from the
[page of the theme](https://vari-sh.github.io/cremisi/#install) and drop it into the `Installed Packages`
folder, next to the one *Preferences → Browse Packages…* opens.

If you copied the `.sublime-color-scheme` files into `Packages/User` before, remove them:
Sublime Text merges schemes that share a name, and the old copies would override the package.

## Use

Run **UI: Select Color Scheme** from the command palette and pick *Cremisi Obsidian* or *Cremisi Ivory*.
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

## Published package

On Package Control the schemes ship as *Cremisi Color Scheme*, from their own repository,
[vari-sh/cremisi-sublime](https://github.com/vari-sh/cremisi-sublime): the two files at its root,
a README and the LICENSE, nothing else. It does not follow this folder by itself, so at every
release of the schemes:

1. Run `generate.py` here and copy both `.sublime-color-scheme` files to the root of `cremisi-sublime`.
2. Commit there and push a new semver tag (`1.0.2`, `1.1.0`, …).
3. Rebuild the offline package for the page, in `vari-sh.github.io`, and point the Sublime card of
   `layouts/cremisi/section.html` at it, removing the old one:

   ```sh
   git -C cremisi-sublime archive --format=zip -o \
     ../vari-sh.github.io/static/cremisi/downloads/cremisi-color-scheme-1.0.2.sublime-package 1.0.2
   ```

Package Control only ships tags: a commit without a new tag reaches no one.
