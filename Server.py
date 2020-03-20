from flask import Flask, request
from flask_cors import CORS
import QuestionAnswerEngineTask
import json

app = Flask(__name__)
CORS(app)

@app.route("/result2")
def result():
 res = 4+3
 print('here')
 return json.dumps(res)


@app.route("/result/", methods=["POST"])
def get_result():
  data = request.data
  print(data)
  text = request.args.get('Text')
  question = request.args.get('Question')
  print(text)
  print(question)
  res = QuestionAnswerEngineTask.returnresult(text, question)
  return json.dumps(res)

app.run(host='0.0.0.0')