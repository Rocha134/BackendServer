#Omar Jímenez
#Alejandro Ubeto
#Francisco Rocha
import flask
from flask_cors import CORS
from flask.json import jsonify
import uuid
from traffic import Street, Car, Nodo
import json, logging, os, atexit

games = {}

app = flask.Flask(__name__, static_url_path='') 

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

CORS(app)

@app.route("/", methods=["GET"])
def sayhello():
    return jsonify("hello")

@app.route("/games", methods=["POST"])
def create():
    global games
    id = str(uuid.uuid4())
    games[id] = Street()

    response = jsonify(id)
    response.status_code = 201
    response.headers['Location'] = f"/games/{id}"
    response.headers['Access-Control-Expose-Headers'] = '*'
    response.autocorrect_location_header = False
    return response

@app.route("/games/<id>", methods=["GET"])
def queryState(id):
    global model
    model = games[id]
    model.step()
    result = [] #Array of arrays with dictionaries with agent info
    cars = [] #Array of car info
    nodes = [] #Array of nodes info
    model_array = []
    g = dict()
    g["run"] = model.running
    model_array.append(g)
    for agent in model.schedule.agents:
        g = dict() #Dictionary with agent info
        g["id"] = agent.unique_id
        g["x"] = agent.pos[0]
        g["y"] = agent.pos[1]
        
        if type(agent) == Car:    #Add to car array
            g["x_next"] = agent.destino.pos[0]
            g["y_next"] = agent.destino.pos[1]
            cars.append(g)
        elif type(agent) == Nodo: #Add to node array
            nodes.append(g)
            
    result.append(cars)
    result.append(nodes)
    result.append(model_array)
    return jsonify(result)

app.run(host='0.0.0.0', port=port, debug=True)
