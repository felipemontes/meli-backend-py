from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["conversations"]
coll = db.conversations

@app.route('/conversations', methods=['POST'])
def create_conversation():
    userid = request.json['userid']
    messages = request.json['messages']
    if userid and messages:
        id = db.conversations.insert_one({'userid': userid, 'messages': messages})
        response = {
            'id': str(id),
            'userid': userid,
            'messages': messages,
        }
        return response
    else:
        return jsonify({"error": "missing request params"}, 400)
    
@app.route('/conversations/<user_id>', methods=['GET'])
def get_user_last_message(user_id):
    conversation = coll.find_one({'userid': user_id})
    resp = json_util.dumps(conversation)
    test = conversation['messages'][-1]['date']
    return test

if __name__ == "__main__":
    app.run(debug=True)