from flask import Flask, request
from flask_cors import CORS
import QuestionAnswerEngineTask
import json
app = Flask(__name__,
           static_url_path='',
           static_folder='static')
CORS(app)
test = QuestionAnswerEngineTask.Engine()
@app.route('/')
def root():
   return app.send_static_file('index.html')

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
  res = test.returnresult(text, question, 3)
  return json.dumps(res)

# app.run(host='0.0.0.0')
app.run()