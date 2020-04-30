import json
import QuestionAnswerEngineTask

question_list_file_path = "test-cases/question_list.json"

with open(question_list_file_path, 'r') as file:
    data = file.read()

question_list = json.loads(data)

for q in question_list:
    print("************************************************************")
    print("Testing ", q['name'])

    text_file_path = "test-cases/" + q['file']
    with open(text_file_path, 'r', encoding="utf8") as file:
        text_data = file.read()

    res = QuestionAnswerEngineTask.returnresult(text_data,  q['question'])
    print(q['question'])
    print(res)
    print()