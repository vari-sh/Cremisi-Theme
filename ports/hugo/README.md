# Cremisi for Hugo

`cremisi-syntax.css` styles Hugo's Chroma highlighting in both variants, switched by an attribute on the page.

## Install

1. Enable Chroma classes in `hugo.toml`:
   ```toml
   [markup.highlight]
     noClasses = false
   ```
2. Include `cremisi-syntax.css` in your theme.
3. Set `data-theme="obsidian"` or `data-theme="ivory"` on the `<html>` element.

## Notes

Chroma is coarser than a TextMate grammar, so a few roles of the editor theme cannot be reproduced:
control flow is not told apart from other keywords, and member access (`obj.field`) stays a plain name.
YAML and JSON keys, YAML anchors and plain YAML scalars are restored per language through `data-lang`.
