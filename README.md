# Panda Vivid Black, Panda Modern Dark, Panda Modern Cyan & Panda Flutter Dark for JetBrains (v1.4.2)

JetBrains / Android Studio port of the Panda Vivid Black VS Code themes. Includes:

- **Panda Vivid Black** (+ Islands variant)
- **Panda Modern Dark** (+ Islands variant)
- **Panda Modern Cyan** (+ Islands variant): cyan types (`#00C9B0`), blue named arguments and member method calls (`#79B8FF`), purple fields / property access and function declarations (`#B084FF`)
- **Panda Flutter Dark** (+ Islands variant, new in 1.4.0): the official DartPad / Flutter dark syntax colors on the Modern Dark / Cyan near-black `#0C0C0C` UI — green keywords (`#50E191`), orange types (`#FF916E`), cyan identifiers / functions / properties / named arguments (`#00D2FA`), pink strings (`#FA557D`), numbers (`#AFCEA2`, updated in 1.4.1), and gray annotations (`#909090`)

Tuned separately for Kotlin (Compose annotations, extension functions, smart casts, string templates) and Dart/Flutter (named parameters, static getters), plus Android XML, Gradle Kotlin DSL, Logcat, diff and VCS colors.

## Install (Android Studio / IntelliJ)

1. Build or obtain `panda-vivid-black-1.4.2.zip`.
2. Settings → Plugins → ⚙ → **Install Plugin from Disk…**, pick the zip, restart.
3. Settings → Appearance → Theme: choose Panda Vivid Black, Panda Modern Dark, Panda Modern Cyan, or Panda Flutter Dark.

## 1.4.1 update

Panda Flutter Dark numeric literals now use `#AFCEA2`, matching Panda Modern Cyan. This applies to integers, decimals, and hexadecimal literals, including the Islands variant. Annotation colors are unchanged.

## Custom colors

Choose the Panda theme under **Settings → Appearance & Behavior → Appearance**. To adjust numeric colors, duplicate the scheme under **Editor → Color Scheme**, then change **Language Defaults → Number** or the language-specific number attribute. Custom schemes may retain old colors after a plugin update; reselect the bundled Panda Flutter Dark scheme to use its defaults.

## Build

```bash
./gradlew buildPlugin   # output: build/distributions/
```

## tools/

`convert.py`, `panda_*_extras.py` and `test_*.py` are copies of the generator/alignment scripts. They expect the original `theme_extension` layout (`theme_extension/idea/<script>` with sibling `vscode/` and `idea/panda-vivid-black/`), so run them from there, not from `tools/`. Note: re-running `convert.py` overwrites hand-tuned colors in the scheme XMLs.

## Theme palette previews / 四套主题配色预览

Generated from the VS Code theme color definitions. These illustrate token colors; they are not editor screenshots. Language grammars and semantic providers can assign different roles. Font styling is simplified in these previews.

示例覆盖 Dart / Flutter、Kotlin、Go、Rust 和 C++。以下为主题源码生成的配色示意图，不是编辑器实机截图；具体高亮分类由语言扩展决定，预览简化了字体样式。

### Panda Vivid Black

![Panda Vivid Black Dart palette preview](images/panda-vivid-black-preview.png)

<details>
<summary>Kotlin · Go · Rust · C++</summary>

**Kotlin**

![Panda Vivid Black Kotlin palette preview](images/panda-vivid-black-kotlin-preview.png)

**Go**

![Panda Vivid Black Go palette preview](images/panda-vivid-black-go-preview.png)

**Rust**

![Panda Vivid Black Rust palette preview](images/panda-vivid-black-rust-preview.png)

**C++**

![Panda Vivid Black C++ palette preview](images/panda-vivid-black-cpp-preview.png)

</details>

### Panda Modern Dark

![Panda Modern Dark Dart palette preview](images/panda-modern-dark-preview.png)

<details>
<summary>Kotlin · Go · Rust · C++</summary>

**Kotlin**

![Panda Modern Dark Kotlin palette preview](images/panda-modern-dark-kotlin-preview.png)

**Go**

![Panda Modern Dark Go palette preview](images/panda-modern-dark-go-preview.png)

**Rust**

![Panda Modern Dark Rust palette preview](images/panda-modern-dark-rust-preview.png)

**C++**

![Panda Modern Dark C++ palette preview](images/panda-modern-dark-cpp-preview.png)

</details>

### Panda Modern Cyan

![Panda Modern Cyan Dart palette preview](images/panda-modern-cyan-preview.png)

<details>
<summary>Kotlin · Go · Rust · C++</summary>

**Kotlin**

![Panda Modern Cyan Kotlin palette preview](images/panda-modern-cyan-kotlin-preview.png)

**Go**

![Panda Modern Cyan Go palette preview](images/panda-modern-cyan-go-preview.png)

**Rust**

![Panda Modern Cyan Rust palette preview](images/panda-modern-cyan-rust-preview.png)

**C++**

![Panda Modern Cyan C++ palette preview](images/panda-modern-cyan-cpp-preview.png)

</details>

### Panda Flutter Dark

![Panda Flutter Dark Dart palette preview](images/panda-flutter-dark-preview.png)

<details>
<summary>Kotlin · Go · Rust · C++</summary>

**Kotlin**

![Panda Flutter Dark Kotlin palette preview](images/panda-flutter-dark-kotlin-preview.png)

**Go**

![Panda Flutter Dark Go palette preview](images/panda-flutter-dark-go-preview.png)

**Rust**

![Panda Flutter Dark Rust palette preview](images/panda-flutter-dark-rust-preview.png)

**C++**

![Panda Flutter Dark C++ palette preview](images/panda-flutter-dark-cpp-preview.png)

</details>
