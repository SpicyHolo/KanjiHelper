# KanjiHelper
KanjiHelper is a simple **TUI** (Text-baseed user interface) app written using [Rich](https://github.com/Textualize/rich) library for python. It helps with _visualising progress in learning Japanese writing system (Kanji)_.  
It has features such as:
- importing the Kanji from **Anki**, a popular flashcard program **(not implemented yet)**
- displaying the gallery of known unique Kanji characters
- comparing it to external lists such as JLPT levels, Japanese School Grades and Jōyō list.

## Getting started
App requires **Python** to run, you can create a virtual environment (if you wish) and install all the dependencies defined in `pyproject.toml` using pip:
```sh
pip install .
```
To run app currently you need to start the main script located in `./src`
```sh
python ./src/main.py
```

## Preview
### Gallery
![app gallery preview](https://github.com/user-attachments/assets/2c2922ee-099a-49b3-896f-5ba33a118ae1)
### External Kanji Lists
![app kanji lists preview](https://github.com/user-attachments/assets/a0bf37a7-72f4-47a8-bd18-2d1d91c5dbbc)

## Controls
Currently navigation is done using arrow keys, and vim navigation keys (hjkl).  
- Use vertical movements (`↑ up` and `↓down` arrow keys, or `k` and `j`) for navigating the main menu,  
- and Horizontal movement (`← left` and `→ right` arrow keys or `h` and `l`) for navigating across pages in gallery or Kanji Lists.
- To quickly change across categories of Kanji Lists use `Tab` or `Shift+Tab`.

## Motivation
- Learning [Rich](https://github.com/Textualize/rich) library.
- Love the TUI apps estetique <3.
- Actually needed the tool.
