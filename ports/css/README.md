# Cremisi scales for CSS

`cremisi-scales.css` declares the two tonal scales as custom properties on `:root`:
`--cremisi-stone-50` … `--cremisi-stone-950` and `--cremisi-blood-50` … `--cremisi-blood-950`.

## Usage

Include the file, then map the steps to roles in your own interface, one map per variant:

```css
[data-theme="obsidian"] {
  --ui-ground: var(--cremisi-stone-900);
  --ui-text:   var(--cremisi-stone-100);
  --ui-accent: var(--cremisi-blood-600);
}
[data-theme="ivory"] {
  --ui-ground: var(--cremisi-stone-50);
  --ui-text:   var(--cremisi-stone-900);
  --ui-accent: var(--cremisi-blood-600);
}
```

A complete role-by-role recipe is `scale_ui` in [`palette.yaml`](../../palette.yaml).
The scales are for interfaces; syntax highlighting stays with the materials.
