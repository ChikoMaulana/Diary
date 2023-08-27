from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient

from datetime import datetime

client = MongoClient('mongodb+srv://chikodatabase:chiko123@chikodata.og7ni.mongodb.net')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get("title_give")
    content_receive = request.form.get("content_give")

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-T%H-%M-%S')
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)

    pp = request.files['profile_give']
    pp_extension = pp.filename.split('.')[-1]
    pp_filename = f'static/profile/pp-{mytime}.{pp_extension}'
    pp.save(pp_filename)

    doc = {
        'pp': pp_filename,
        'file': filename,
        'title':title_receive,
        'content':content_receive
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)