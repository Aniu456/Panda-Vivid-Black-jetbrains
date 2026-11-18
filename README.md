# Panda Vivid Black, Panda Modern Dark & Panda Modern Cyan for JetBrains (v1.3.1)

JetBrains / Android Studio port of the Panda Vivid Black VS Code themes. Includes:

- **Panda Vivid Black** (+ Islands variant)
- **Panda Modern Dark** (+ Islands variant)
- **Panda Modern Cyan** (+ Islands variant): cyan types (`#00C9B0`), blue named arguments and member method calls (`#79B8FF`), purple fields / property access and function declarations (`#B084FF`)

Tuned separately for Kotlin (Compose annotations, extension functions, smart casts, string templates) and Dart/Flutter (named parameters, static getters), plus Android XML, Gradle Kotlin DSL, Logcat, diff and VCS colors.

## Install (Android Studio / IntelliJ)

1. Download `panda-vivid-black-1.3.1.zip` from Releases.
2. Settings → Plugins → ⚙ → **Install Plugin from Disk…**, pick the zip, restart.
3. Settings → Appearance → Theme: choose Panda Vivid Black, Panda Modern Dark, or Panda Modern Cyan.

## Build

```bash
./gradlew buildPlugin   # output: build/distributions/
```

## tools/

`convert.py`, `panda_*_extras.py` and `test_*.py` are copies of the generator/alignment scripts. They expect the original `theme_extension` layout (`theme_extension/idea/<script>` with sibling `vscode/` and `idea/panda-vivid-black/`), so run them from there, not from `tools/`. Note: re-running `convert.py` overwrites hand-tuned colors in the scheme XMLs.
