from flask import Flask, request, jsonify
import json

app = Flask(__name__)

file_path = '....\\films.json'

# Function to update the JSON file
def update_json_file(data):
   with open(file_path, 'w') as json_file:
       json.dump(data, json_file, indent=2)

# Function to load data from JSON file
def load_data():
   try:
       with open(file_path, 'r') as json_file:
           data = json.load(json_file)
       return data
   except FileNotFoundError:
       return []

# Function to save data to the JSON file
def save_data(data):
   with open(file_path, 'w') as json_file:
       json.dump(data, json_file, indent=2)

films_data = load_data()

# Command GET for all list
@app.route('/films', methods=['GET'])
def get_films():
   return jsonify(films_data)

# Command GET for a film by ID
@app.route('/films/<string:film_id>', methods=['GET'])
def get_film(film_id):
   try:
       film_id = int(film_id)
       film = next((f for f in films_data if f["id"] == film_id), None)
       if film:
           return jsonify(film)
       else:
           return jsonify({"message": "Resource not found"}), 404
   except ValueError:
       return jsonify({"message": "Invalid id, must be number"}), 422

# For command POST
@app.route('/films', methods=['POST'])
def create_film():
   try:
       data = request.json
       new_film = {
           "id": len(films_data) + 1,
           "title": data["title"],
           "director": data["director"],
           "release_date": data["release_date"],
           "genre": data["genre"],
       }
       films_data.append(new_film)
       update_json_file(films_data)
       return jsonify(new_film), 201
   except (KeyError, ValueError):
       return jsonify({"message": "Invalid request data"}), 422

# Command PUT
@app.route('/films/<string:film_id>', methods=['PUT'])
def update_film(film_id):
   try:
       data = request.json
       film_id = int(film_id)
       film = next((f for f in films_data if f["id"] == film_id), None)
       if film:
           film.update(data)
           update_json_file(films_data)
           return jsonify(film)
       else:
           return jsonify({"message": "Resource not found"}), 404
   except (KeyError, ValueError):
       return jsonify({"message": "Invalid id, must be number"}), 422

# Command delete
@app.route('/films/<string:film_id>', methods=['DELETE'])
def delete_film(film_id):
   try:
       film_id = int(film_id)
       global films_data
       films_data = [f for f in films_data if f["id"] != film_id]
       update_json_file(films_data)
       return jsonify({"message": "Resource deleted"}), 200
   except ValueError:
       return jsonify({"message": "Invalid id, must be number"}), 422


if __name__ == '__main__':
   app.run(debug=True)
