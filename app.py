#example of building a REST API to create small to do list
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.secret_key = "jchukwuezi"
auth = HTTPBasicAuth()

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

""" 
29/03/2021: Commenting this out because the HTTP GET METHOD has been updated. Requires login details.

#entry point url, naming convention: application name/api/version/resource
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks(): #jsonify returns a response with JSON representation of an argument
    #return jsonify({'tasks': tasks})
    #before returning list of tasks, it will be passed through make_public_task method [16/03/2021]
    return jsonify({'tasks': [make_public_task(task) for task in tasks]}) #list comprehension
"""

#second GET METHOD
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    #list comprehension -> expression condition of a loop
    task =  [task for task in tasks if task['id'] == task_id]
    if len(task) == 0: #if no tasks are found httpexception will be raised
        abort(404) 
    return jsonify({'tasks': task[0]})

#function to handle errors raised
@app.errorhandler(404)
def not_found(error):
    #changing the default html response to json (more api friendly)
    return make_response(jsonify({'error': 'Not found'}),404)

#POST METHOD
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(404)
    task = {
        'id': tasks[-1]['id'] + 1, #ensuring id stays unique
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201 #response code for success + resource created

#DELETE METHOD
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task =  [task for task in tasks if task['id'] == task_id]
    if len(task) == 0: #if no tasks are found httpexception will be raised
        abort(404) 
    tasks.remove(task[0])    
    return jsonify({'done': True}), 202

#PUT METHOD - To Update Tasks
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_tasks(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json: #checking if request is json
        abort(404)

    #setting the fields equal to the updated fields
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])

    return jsonify({'task': task[0]}), 201 #response code for success + resource created
    
#improving design by making task public
#list of tasks will be returned to the client + URI will be created using the URI from the get_task method 
#the id will be replaced with the URI for the new_task dict
def make_public_task(task):
    new_task = {} 
    for field in task: #looping through task dict
        if field == 'id': #it's getting the id from task and pass it in while generating the the URI for client
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True) 
        else:
            new_task[field] = task[field] #if it's not an id then the fields in the new_task dict will be set to the fields in the task dict
    return new_task

@auth.get_password
def get_password(username): #this function obtains a password for a given user
    if username == 'joshua':
        return 'python'
    return None

@auth.error_handler #function will be used when unauthorized error code needs to be sent back to the client
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

#updating HTTP GET METHOD to require a specific user before giving password so that tasks can be retrieved
@app.route('/todo/api/v1.0/tasks')
@auth.login_required
def get_tasks():
    return jsonify({'tasks': tasks})
    








if __name__ == "__main__":
    app.run(debug=True)
