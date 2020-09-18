import json
import QuestionAnswerEngineTask

question_list_file_path = "test-cases/question_list.json"
test = QuestionAnswerEngineTask.Engine()
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

    scores, res = test.returnresult(text_data, q['question'], 3)
    print(q['question'])

    # provided_answer = test.remove_abbrev(q['Answer'].lower())

    for answer in res:
        correct = False
        if answer.lower() in q['Answer'].lower():
            correctAnswer += 1
            correct = True
            print('correct answer')
            break
    if correct == False and q['Answer'] in scores:
        print('incorrect:', scores[q['Answer']])
    print('correct answer: ',q['Answer'])
    print(res)
    print()

print('accuracy: ', correctAnswer / len(question_list), ' correct answer: ', correctAnswer)