# QuizApp

A simple Python-based quiz application. This repository contains the code for creating and running quizzes 
from the command line. It is intended to be lightweight and easy to extend.

## Features
- Questions with one of three correct answers
- Easy to add new questions or question files
- Minimal dependencies (almost pure Python)

## Requirements
- Python 3.8+
- Everything included in `requirements.txt`

## Quick Start
1. Clone the repository:
```bash
    git clone https://github.com/xxNauty/QuizApp.git
    cd QuizApp
```

2. Run the app:
```bash
    python main.py
```

## Custom quiz database
App for now accepts questions in `CSV` and `JSON` formats.
1. Sample of the `CSV` file
```csv
NUMER_PYTANIA,PYTANIE,ODP_A,ODP_B,ODP_C,POPRAWNA,ZRODLO
1,"Content of the question","answer A","answer B","answer C","correct answer (A/B/C)","Optional field, where you can put additional information that can prove the correct answer"
```
2. Sample of the `JSON` file
```json
[
  {"NUMER_PYTANIA":1,"PYTANIE":"Content of the question","ODP_A":"answer A","ODP_B":"answer B","ODP_C":"answer C","POPRAWNA":"correct answer (A/B/C)","ZRODLO":"Optional field, where you can put additional information that can prove the correct answer"}
]
```
For every new quiz database you should create new directory inside the `data` directory. For database create the `data.csv` or `data.json` file and for the configuration create the `config.yaml` file.
Inside it, you can define how many questions should be drawn for every quiz and how many correct answers are required to pass it.

Sample of the `config.yaml` file:
```yaml
number_of_questions: 20
minimum_to_pass: 18
```