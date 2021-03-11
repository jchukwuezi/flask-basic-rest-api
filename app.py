#example of building a REST API to create small to do list
from flask import Flask, jsonify

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





if __name__ == "__main__":
    app.run(debug=True)
