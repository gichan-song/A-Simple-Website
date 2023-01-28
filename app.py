from flask import Flask, render_template, jsonify, request
app = Flask(__name__)


from pymongo import MongoClient
client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.gichan

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')


@app.route('/memo', methods=['GET'])
def listening():
    memos = list(db.memos.find({}, {'_id': False}))
    return jsonify({'msg':memos})

@app.route('/modify', methods=['POST'])
def modify():
    num_receive = request.form['num_give']
    title_receive = request.form['title_give']
    text_receive = request.form['text_give']
    db.memos.update_one({'num':num_receive},{'$set':{'title':title_receive}})
    db.memos.update_one({'num': num_receive}, {'$set':{'text': text_receive}})
    return jsonify({'msg':"수정 완료!"})

@app.route('/delete', methods=['POST'])
def delete():
    num_receive = request.form['num_give']
    db.memos.delete_one({'num': num_receive})
    return jsonify({'msg':"삭제 완료!"})

@app.route('/save', methods=['POST'])
def saving():
    # num_receive = request.form['num_give']
    title_receive = request.form['title_give']
    text_receive = request.form['text_give']
    num = str(db.memos.estimated_document_count())

    doc={"num":num,
        'title':title_receive,
         'text':text_receive
         }
    db.memos.insert_one(doc)


    return jsonify({'msg':"저장 완료!"})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)