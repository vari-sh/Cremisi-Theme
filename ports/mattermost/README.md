# Cremisi for Mattermost

Two custom themes for [Mattermost](https://mattermost.com), **Cremisi Obsidian** and **Cremisi Ivory**,
each a single line of JSON, the format Mattermost uses to share theme colours.

## Install

1. In Mattermost open *Settings → Display → Theme*, click *Edit* and choose *Custom Theme*.
2. Copy the content of `cremisi-obsidian.json` or `cremisi-ivory.json` (on GitHub: *Copy raw file*)
   and paste it into the text box at the bottom of the panel. Mattermost reads the colours on paste, so paste it
   rather than type it.
3. Click *Save*. Tick *Apply new theme to all my teams* first if you are in more than one team.

## Roles

- **Sidebar.** Sunken stone: the deepest step on Obsidian, `stone-100` on Ivory, with a `stone-200` header.
  The current channel is marked by a crimson border, unread channels are tallow on Obsidian and dark blood on Ivory.
- **Center channel.** The editor's ground and ink. Errors and the new-message line speak with the voice of blood;
  a message that mentions you lies on clotted blood (`blood-950`) on Obsidian, on `blood-50` on Ivory,
  with the mention itself in withered petal.
- **Badges and presence.** Mention badges are blood. Online is malachite, away amber, do not disturb blood.
- **Links and buttons.** Links are lapis, buttons crimson with bone text, the same in both variants.

Every text colour clears 4.5:1 against the ground it sits on.

Mattermost highlights code with one of four fixed themes, so code blocks cannot speak the materials:
Obsidian uses *Monokai*, Ivory *GitHub*. The fonts are Mattermost's own.

## Built, not drawn

Both themes are generated from the same `palette.yaml` as the editor ports and the page:

```sh
python3 ports/mattermost/generate.py      # from the root of vari-sh/Cremisi-Theme
```

Every colour is a material or a step of the stone and blood scales.
`mentionBj` repeats `mentionBg`: it is the old misspelled name of the same key, kept by Mattermost for older themes.
