from flask import Flask, render_template, jsonify, request, send_file
import json

app = Flask(__name__)

# Load initial data
with open('data.json', 'r') as file:
    data = json.load(file)

# Save data to file
def save_data():
    with open('data.json', 'w') as file:
        json.dump(data, file)

# Get the count of JSON values
def get_data_count():
    return len(data)

# Get all data
@app.route('/', methods=['GET'])
def get_all_data():
    count = get_data_count()
    return render_template('index.html', data=data, count=count)

# Add data
@app.route('/', methods=['POST'])
def add_item():
    req_data = request.json
    index = str(len(data))  # use len(data) as the index
    data[index] = req_data  # add data with the index
    save_data()
    return jsonify(req_data), 201

# Update data
@app.route('/<index>', methods=['PUT'])
def update_item(index):
    if index in data:
        req_data = request.json
        data[index] = req_data
        save_data()
        return jsonify(req_data)
    else:
        return jsonify({"error": "Index not found"}), 404

# Delete data
@app.route('/<index>', methods=['DELETE'])
def delete_item(index):
    if index in data:
        deleted_item = data.pop(index)
        save_data()
        return jsonify(deleted_item)
    else:
        return jsonify({"error": "Index not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
