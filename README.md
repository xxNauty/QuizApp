# QuizApp

It is a simple Python-based quiz game with TUI(Terminal User Interface). Supports quizzes with one of three correct answer

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
Inside it, you can define the name of the quiz, how many questions should be drawn for every quiz and how many correct answers are required to pass it. \
Now you can also use script located inside the `scripts\quiz_template_generator.py` file which can do it for you. Just answer its questions and the templates for new quiz will be generated. \
You can run it with:
```bash
python scripts/quiz_template_generator.py
```
You will be asked four questions, you need to write:
1. The name of quiz
2. In which format you want to store your questions (for now only CSV and JSON are supported)
3. How many questions should single quiz contain
4. How many answers must be correct to pass

Last two information will be stored inside the `config.yaml` file inside the quiz directory

Sample config file:
```yaml
quiz_name: name_of_the_quiz
number_of_questions: 20
minimum_to_pass: 18
```