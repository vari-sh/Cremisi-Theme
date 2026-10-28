# Cremisi for Typora

Two themes for [Typora](https://typora.io), **Cremisi Obsidian** and **Cremisi Ivory**,
sharing one base stylesheet: the variant files only define the `--cr-*` colours.
The fonts (Cinzel, Montserrat, JetBrains Mono) are bundled, so the theme works offline.

## Install

1. In Typora open *Preferences → Appearance → Open Theme Folder*.
2. Copy `cremisi-obsidian.css`, `cremisi-ivory.css` and the whole `cremisi/` folder into it.
3. Restart Typora and pick *Cremisi Obsidian* or *Cremisi Ivory* from the *Themes* menu.

The `cremisi/` folder must sit next to the two variant files: they import `cremisi/cremisi-base.css`,
which loads the fonts from `cremisi/fonts/`.

## Roles

Headings are set in Cinzel and speak with the voice of blood, body text in Montserrat, code in JetBrains Mono.
Code fences follow the sixteen materials of the editor themes: keywords blood, functions lapis, types tallow,
strings malachite, numbers amber, properties verdigris, comments incense.
Mermaid diagrams use Typora's `dark` theme on Obsidian and `default` on Ivory.

## Fonts

Cinzel, Montserrat and JetBrains Mono are licensed under the SIL Open Font License 1.1:
see [`cremisi/fonts/OFL.txt`](cremisi/fonts/OFL.txt).
