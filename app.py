#example of building a REST API to create small to do list
from flask import Flask, jsonify, abort

app = Flask(__name__)
app.secret_key = "jchukwuezi"

#implementing entry point of this web service

#creating a list of tasks to be passed
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },

    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Find a good tutorial on the web',
        'done': False
    }
]

#entry point url, naming convention: application name/api/version/resource
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks(): #jsonify returns a response with JSON representation of an argument
    return jsonify({'tasks': tasks})

#second GET METHOD
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    #list comprehension -> expression condition of a loop
    task =  [task for task in tasks if task['id'] == task_id]
    if len(task) == 0: #if no tasks are found httpexception will be raised
        abort(404) 
    return jsonify({'tasks': task[0]})




if __name__ == "__main__":
    app.run(debug=True)
