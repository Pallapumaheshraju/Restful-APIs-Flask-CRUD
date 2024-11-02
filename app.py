from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory data store for demonstration (you can replace it with a database)
users = [
    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
    {'id': 2, 'name': 'Jane Doe', 'email': 'jane@example.com'}
]

# Retrieve all users (GET)
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})

# Retrieve a single user by id (GET)
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        abort(404)  # Not Found
    return jsonify(user)

# Create a new user (POST)
@app.route('/api/users', methods=['POST'])
def create_user():
    if not request.json or 'name' not in request.json or 'email' not in request.json:
        abort(400)  # Bad Request
        return "User Fields Empty"
    new_user = {
        'id': users[-1]['id'] + 1 if users else 1,
        'name': request.json['name'],
        'email': request.json['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201  # Created

# Update an existing user (PUT)
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        abort(404)  # Not Found
    if not request.json:
        abort(400)  # Bad Request

    user['name'] = request.json.get('name', user['name'])
    user['email'] = request.json.get('email', user['email'])
    return jsonify(user)

# Delete a user (DELETE)
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        abort(404)  # Not Found
    users = [user for user in users if user['id'] != user_id]
    return jsonify({'result': True})

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

# Error handler for 400 Bad Request
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

if __name__ == "__main__":
    print("Starting Flask server... Application is running.")
    app.run()