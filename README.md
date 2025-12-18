# QuizApp

It is a simple Python-based quiz game with TUI(Terminal User Interface). Supports quizzes with one of three answer correct.

## Requirements
- Python 3.8+
- Everything included in `requirements.txt`

## Quick Start
1. Clone the repository:
```bash
git clone https://github.com/xxNauty/QuizApp.git
cd QuizApp
```
2. Run the app: (replace {name_of_quiz} with actual name of quiz)
```bash
python main.py {name_of_quiz}
```

## Create own quiz database
App for now accepts questions in `CSV` and `JSON` formats.
1. Sample of the `CSV` file
```csv
id,question,answer_a,answer_b,answer_c,correct,source
1,"Content of the question","answer A","answer B","answer C","correct answer (A/B/C)","Optional field, where you can put additional information that can prove the correct answer"
```
2. Sample of the `JSON` file
```json
[
  {
    "id":1,
    "question":"Content of the question",
    "answer_a":"answer A",
    "answer_b":"answer B",
    "answer_c":"answer C",
    "correct":"correct answer (A/B/C)",
    "source":"Optional field, where you can put additional information that can prove the correct answer"}
]
```

If you want to create new quiz, you can use script located inside the `scripts\quiz_template_generator.py` 
file which can do it for you. Just answer its questions and the templates for new quiz will be generated.

You can run it with:
```bash
python -m scripts.quiz_template_generator
```
You will be asked four questions, you need to write:
1. The name of quiz
2. In which format you want to store your questions (for now only CSV and JSON are supported)
3. How many questions should single quiz contain
4. How many answers must be correct to pass

All the configuration of the quiz will be stored inside the `config.yaml` file.

Sample config file:
```yaml
quiz_name: name_of_the_quiz
number_of_questions: 20
minimum_to_pass: 18
integrity_verified: false
```

Now you can fill the database file with questions. But it's not the end of work. When the file is ready, 
you have to run script located inside the `scripts\data_integrity_checker.py` to check if everything is ok with your database.
If there are any errors inside, it will tell you where the problems are. If everything is correct, it will mark this database
as checked, and it will make it available for use (If you try to use unverified database it will tell you that you cannot).

You can run this script with: (replace {name_of_quiz} with actual name of quiz you want to check)
```bash
python -m scripts.data_integrity_checker {name_of_quiz}
```