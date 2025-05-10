from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import storage

app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address)
CORS(app)  # This will enable CORS for all routes


@app.route('/api/posts', methods=['GET'])
@limiter.limit("10/minute") #Limit to 10 requests per minute
def get_posts():
    posts = storage.load_json("data.json")
    title = request.args.get('title')
    content = request.args.get('content')
    if title:
        collection = [post for post in posts if title in post.get('title')]
        return jsonify(collection)
    if content:
        collection = [post for post in posts if content in post.get('content')]
        return jsonify(collection)

    sort = request.args.get('sort')
    direction = request.args.get('direction')
    if sort and direction:
        if direction == 'desc':
            sorted_posts = sorted(posts, key=lambda item: item[sort], reverse=True)
        else:
            sorted_posts = sorted(posts, key=lambda item: item[sort])

    else:
        sorted_posts = posts
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    if page and limit:
        start_index = (page - 1) * limit
        end_index = start_index + limit
        paginated_posts = sorted_posts[start_index:end_index]
        return jsonify(paginated_posts)
    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'GET':
        # Handle the GET request
        posts = storage.load_json("data.json")
        return jsonify(posts)

    elif request.method == 'POST':
        # Handle the POST request
        new_post = request.get_json()
        if not validate_post_data(new_post):
            return jsonify({"error": "Invalid post data"}), 400
        storage.add_post(new_post)
        return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['PUT'])
def handle_post(id):
    # Find the post with the given ID
    post = storage.find_post_by_id(id)

    # If the post wasn't found, return a 404 error
    if post is None:
        return '', 404

    # Update the post with the new data
    new_data = request.get_json()
    updated_post = storage.update_post(post, new_data)
    # Return the updated post
    return jsonify(updated_post)


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    # Find the post with the given ID
    post = storage.find_post_by_id(id)

    # If the post wasn't found, return a 404 error
    if post is None:
        return '', 404

    # Remove the book from the list
    deleted_post = storage.delete_post(id)

    # Return the deleted post
    return jsonify(deleted_post)


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Post Not Found or Wrong Url"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Request is in bad shape. Missing some field data?"}), 400


def validate_post_data(data):
    if "title" not in data or "content" not in data:
        return False
    return True


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
