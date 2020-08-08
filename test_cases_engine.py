import json
import QuestionAnswerEngineTask

question_list_file_path = "test-cases/question_list.json"

with open(question_list_file_path, 'r', encoding="utf8") as file:
    data = file.read()

question_list = json.loads(data)

correctAnswer = 0

for q in question_list:
    print("************************************************************")
    print("Testing ", q['name'])

    text_file_path = 'test-cases/' + q['file']
    with open(text_file_path, 'r', encoding="utf8") as file:
        text_data = file.read()

    scores, res = QuestionAnswerEngineTask.returnresult(text_data, q['question'], 3)
    print(q['question'])

    provided_answer = QuestionAnswerEngineTask.remove_abbrev(q['Answer'].lower())

    for answer in res:
        correct = False
        if answer.lower() in provided_answer or provided_answer in answer.lower():
            correctAnswer += 1
            correct = True
            print('correct answer')
            break
    if correct == False and provided_answer in scores:
        print('incorrect:', scores[provided_answer])
    print('correct answer: ', provided_answer)
    print(res)
    print()

print('accuracy: ', correctAnswer / len(question_list), ' correct answer: ', correctAnswer)