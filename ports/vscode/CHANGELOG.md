# Changelog

## 0.2.1

- Booleans and null speak with the voice of blood: `True`, `False`, `None`, `null`, `undefined` and `NULL`
  are all blood, bold italic. Python's grammar gives `True` and `None` the same scope, so they could not
  differ. JSON and YAML values stay amber.
- Brackets are iron at every depth, as in Sublime Text and on the page: bracket pair colorization no longer
  paints them blood, amber and lapis.
- Python docstrings are documentation, incense like comments, JSDoc and Rust's doc comments.
- Aligned with the Sublime Text port and the page: decorator dots and Rust attributes (`#`, derived traits)
  are sealing wax; member-access dots and C `->` are wine; `export`, `from`, `import type`, `as` and Rust
  `use` read as imports.
- Interpolations are sealing wax: TypeScript `${…}` and Rust format strings such as `{}` and `{left:>4}`.
- Python raw strings keep their plain text in malachite, with only the regex internals in sealing wax and
  character-set brackets in iron.
- Rust modules are tallow, enum members amber, TypeScript built-in properties such as `.length` verdigris;
  Rust floats no longer break at the decimal point.

## 0.2.0

- Syntax checked token by token against the grammars that ship with VS Code: operators, JSON keys and
  YAML anchors no longer inherit italic or bold from wider rules; call arguments, Python attributes,
  TypeScript properties and `const` bindings, C directives, regex internals, Markdown headings, inline
  code and link text now match the Sublime Text port.
- Semantic tokens mapped on every role: functions and methods, parameters, properties, variables and
  readonly ones, types, enum members, decorators, macros, `self` and builtins.
- Workbench: crimson badges and cursor, a sober status bar (crimson only for debugging and remote),
  removed-diff grounds from the blood scale, a terminal bright black that clears 3:1.

## 0.1.1

- Markdown links are lapis without underline: the text between square brackets is no longer underlined.

## 0.1.0

- First release: Cremisi Obsidian and Cremisi Ivory.
