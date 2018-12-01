import json

from flask import Flask, request
from pymongo import MongoClient

client = MongoClient()
db = client.bot

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello world!'


@app.route('/tasks', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        # file = request.files['file']
        # # if user does not select file, browser also
        # # submit an empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        #
        # with open('data.json', encoding='utf-8') as f:
        #     data = json.load(f)
        #     db.tasks.remove({})
        #     db.tasks.insert(data)
        data = json.load(request.data)
        db.tasks.remove({})
        db.tasks.insert(data)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
