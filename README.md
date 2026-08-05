# Anton App Automation Suite

An automated Playwright engine for educational DOM interaction, state tracking, and answer parsing.

> **Disclaimer:** This repository is intended strictly for educational purposes and browser automation research.

---

## Architecture Overview

- **State Generator:** Dynamic state key hashing using standard header elements (`h1`/`h2`) and contextual DOM sub-trees.
- **Parser Engine:** Context-aware regex extraction targeting active input containers and text elements.
- **Execution Engine:** Playwright Chromium integration with simulated input handling.

---

## Setup & Deployment

<details>
<summary><b>Developer Setup & Execution Guide (Click to expand)</b></summary>

### Prerequisites
- Python 3.10+
- Chromium browser binaries

### Shell Environment Setup
Create a virtual environment and install the engine package in editable mode:

```fish
python3 -m venv .venv
source .venv/bin/activate.fish
pip install -e .
playwright install chromium
