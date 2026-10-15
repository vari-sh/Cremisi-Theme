# Cremisi for fish

Syntax-highlighting themes for the [fish shell](https://fishshell.com) (fish 4.1 or later).

## Install

1. Copy both files into `~/.config/fish/themes/`.
2. Run `fish_config theme choose cremisi-obsidian` (or `cremisi-ivory`).

Each theme carries a `[light]` (Ivory) and a `[dark]` (Obsidian) section, so fish follows the terminal background;
the two files differ only in the variant used when the background cannot be detected.
Add `--color-theme=dark` or `--color-theme=light` to force one.

## Roles

Commands are lapis, keywords blood, parameters petal, options tallow, strings malachite, escapes sealing wax,
operators and redirections wine, comments incense. An unknown command is crimson and underlined, so it never
reads as a keyword.
