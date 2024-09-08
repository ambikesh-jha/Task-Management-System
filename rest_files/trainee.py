from flask import Flask, request, jsonify
from pymongo import MongoClient
 
app = Flask(__name__)
 
class Trainee:
    def __init__(self, username, trainee_name, task):
        self.username = username
        self.trainee_name = trainee_name
        self.task = task
 
client = MongoClient("mongodb://localhost:27017/flaskDB")
db = client['task_manager']
collection = db['tasks']
 
# Sample trainees{ data from trainer}
trainee_list = [
    Trainee('user1', 'trainer 1', 'Complete project'),
    Trainee('user1', 'trainer 2', 'Complet etask'),
    Trainee('user2', 'trainer 2', 'Prepare presentation')
]
 
# Insert the trainees' tasks into MongoDB (if not already present)
for trainee in trainee_list:
    if not collection.find_one({"username": trainee.username, "task": trainee.task}):
        collection.insert_one({
            "username": trainee.username,
            "assigned_by": trainee.trainee_name,
            "task": trainee.task,
            "task_status": "to do"
        })
 
@app.route('/tasks')
def get_tasks():
    tasks = list(collection.find({}, {"_id": 0}))
    return jsonify(tasks)
 
 
 
# fetch single user task
@app.route('/user_tasks', methods=['POST'])
def get_user_tasks_by_json():
    data = request.json
    if not data or not data.get('username'):
        return jsonify({"error": "Username is required"}), 400
   
    username = data['username']
    user_tasks = list(collection.find({"username": username}, {"_id": 0}))
   
    if not user_tasks:
        return jsonify({"message": "No tasks found for the specified user"}), 404
   
    return jsonify(user_tasks), 200
 
 
# update status of task
@app.route('/update_task_status', methods=['POST'])
def update_task_status():
    data = request.json
    query = {
        "username": data['username'],
        "assigned_by": data['assigned_by'],
        "task": data['task']
    }
    new_status = {"$set": {"task_status": data['task_status']}}
    collection.update_one(query, new_status)
    return jsonify({"message": "Task status updated "}), 200
 
 
# Clear entire 'tasks' collection
@app.route('/clear_db', methods=['POST'])
def clear_db():
    collection.drop()  
    return jsonify({"message": "Database cleared"}), 200
 
if __name__ == '__main__':
    app.run(debug=True)