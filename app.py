from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Load initial data
try:
    with open('data.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = {}

# Save data to file
def save_data():
    with open('data.json', 'w') as file:
        json.dump(data, file)

# Get all data
@app.route('/', methods=['GET'])
def get_all_data():
    count = len(data)
    return render_template('index.html', data=data, count=count)

# Get data at specific index
@app.route('/<index>', methods=['GET'])
def get_item(index):
    try:
        item = data.get(index)
        if item:
            return jsonify(item), 200
        else:
            return jsonify({"error": "No data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Add data
@app.route('/', methods=['POST'])
def add_item():
    try:
        req_data = request.json
        index = str(len(data))
        data[index] = req_data
        save_data()
        return jsonify(req_data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Update data
@app.route('/<index>', methods=['PUT'])
def update_item(index):
    try:
        if index in data:
            req_data = request.json
            data[index] = req_data
            save_data()
            return jsonify(req_data), 200
        else:
            return jsonify({"error": "Index not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete data
@app.route('/<index>', methods=['DELETE'])
def delete_item(index):
    try:
        if index in data:
            deleted_item = data.pop(index)
            save_data()
            return jsonify(deleted_item), 200
        else:
            return jsonify({"error": "Index not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=False, host='0.0.0.0')
