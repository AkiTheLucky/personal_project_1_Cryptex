# CrypTerm

A terminal-based word puzzle game inspired by daily logic games like Mini Crosswords, Spelling Bee, and classic cryptex locking mechanisms. Built as part of the Boot.dev curriculum to bridge the gap between structured tutorials and standalone software development.

## Project Overview

CrypTerm dynamically generates daily-style word puzzles directly in your terminal.

The game fetches a hidden **theme word** from an API and builds a set of related vertical auxiliary words. Players manipulate individual vertical columns by sliding letters up and down to align the correct letters horizontally along the target indicators, unlocking the cryptex.

### Key Features

* **Dynamic Word Generation:** Leverages the Datamuse API to pull target theme words and curate semantically linked auxiliary words on the fly.
* **Interactive Terminal UI:** Powered by `blessed` for full-screen rendering, keyboard event handling, custom color highlights, and adaptive positioning.
* **Dynamic Content Filtering:** Intelligent fallback loops and quality filters prevent obscure jargon, duplicate stems, and unfair word combinations.
* **Built-in Hint System:** Option to automatically align the active column if stuck.
* **End Game Visuals:** Custom terminal burn animation rendered upon solving the puzzle using `terminaltexteffects`.

## How It Works

1. **Theme Selection:** The application selects a random high-frequency theme word (4 to 7 letters long).
2. **Bucket & Column Matching:** Queries Datamuse endpoints for synonyms, triggers, and related terms. It parses frequency scores to ensure high word quality and places matching letters across columns.
3. **Matrix Assembly:** Converts vertical word lists into a navigable grid matrix.
4. **Gameplay Loop:** Key presses rotate column arrays (`pop` and `append`/`insert`) in real time until the solve row string matches the hidden target word.


## Getting Started

### Prerequisites

* Python 3.8 or higher
* Internet connection (required for initial Datamuse API requests)

### Installation

1. **Clone the repository:**
bash
git clone https://github.com/your-username/crypterm.git
cd crypterm



2. **Create and activate a virtual environment (optional but recommended):**
bash
python -m venv venv
source venv/bin/activate
On Windows use: venv\Scripts\activate

3. **Install dependencies:**
bash
pip install requests blessed terminaltexteffects



### Running the Game

Launch the application using Python:

bash
python app.py


> **Note:** Ensure your terminal window is expanded before running. The application checks system terminal dimensions to verify all UI elements fit cleanly.

## Controls

| Key | Action |
| --- | --- |
| `Left Arrow` / `Right Arrow` | Navigate between columns |
| `Up Arrow` / `Down Arrow` | Rotate letters vertically |
| `E` | Reveal hint for active column |
| `Q` | Quit game |


## Code Architecture

* `get_theme_word()`: Fetches popular target words from the Datamuse API.
* `get_thematic_bucket()`: Gathers related vocabulary using synonym and associative endpoints while filtering out obscure entries.
* `arrange_column_words()`: Maps vertical words to target letter indexes across columns.
* `build_cryptex_matrix()`: Converts column dictionary structures into a 2D matrix array.
* `draw_cryptex_board()`: Renders borders, side panels, instructions, and color-coded character selections.
* `generate_playable_board()`: Handles retry logic if initial API payloads do not yield viable matrices.


## Future Roadmap

1. Implement offline word list fallbacks for play without network connectivity.
2. Build a web version using Flask or JavaScript for broader browser access.
3. Sell to LinkedIn or NYT and become millionaire