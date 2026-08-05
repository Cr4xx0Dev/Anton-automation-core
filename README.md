# Anton App Automation Suite

An automated Playwright engine for educational DOM interaction, state tracking, and answer parsing.

> **Disclaimer:** This repository is intended strictly for educational purposes and browser automation research.
> **AI:** The Readme.md is ai generated!

---

## Architecture Overview

- **State Generator:** Dynamic state key hashing using standard header elements (`h1`/`h2`) and contextual DOM sub-trees.
- **Parser Engine:** Context-aware regex extraction targeting active input containers and text elements.
- **Execution Engine:** Playwright Chromium integration with simulated input handling.

---

## Target DOM Structure

The engine parses context and input states by targeting dynamic cursor elements with the following markup:

```html
<div class="cursor" style="display: inline-block; width: 0px; visibility: visible;">
  <div class="cursor-inner" style="display: inline-block; width: 2px; background-color: rgb(97, 97, 97); pointer-events: none; visibility: hidden;">
    &nbsp;
  </div>
</div>
```

---

## Setup & Deployment

<details>
<summary><b>Developer Setup & Execution Guide (Click to expand)</b></summary>

### Prerequisites
- Python 3.10+
- Chromium browser binaries

### Shell Environment Setup
Clone the repository, create a virtual environment, and install the engine package in editable mode:

```fish
git clone [https://github.com/Cr4xx0Dev/Anton-automation-core.git](https://github.com/Cr4xx0Dev/Anton-automation-core.git)
cd Anton-automation-core/
python3 -m venv .venv
source .venv/bin/activate.fish
pip install -e .
playwright install chromium
```

### Execution Flags
Control runtime behavior via system environment variables (`ANTON_MODE` defaults to `learn`):

```fish
# Parse and record state answers (Learn Mode)
ANTON_MODE=learn anton-bot

# Replay recorded state answers (Solve Mode)
ANTON_MODE=solve anton-bot
```

</details>

---

## License

Distributed under the [MIT License](LICENSE).
