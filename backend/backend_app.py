from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import storage

app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address)
CORS(app)  # This will enable CORS for all routes
SWAGGER_URL = "/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL = "/static/masterblog.json"


@app.route('/api/posts', methods=['GET'])
@limiter.limit("10/minute") #Limit to 10 requests per minute
def get_posts():
    """
    Retrieves all posts from storage (json-file)
    according as parameters are given for sorting and/or pagination
    :parameters sort, direction: Sort the posts according to the direction
    :parameters page, limit: Pagination of the posts with <page> pages having <limit> posts each.
    """
    posts = storage.load_json()

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


@app.route('/api/posts/search', methods=['GET'])
@limiter.limit("10/minute") #Limit to 10 requests per minute
def search_posts():
    """
    Retrieves all posts from storage (json-file)
    under consideration of the search specs listed below.
    The search is case-insensitive and finds fragments.
    The sort and pagination features are also available after search.
    :parameter title: (usage: url/?title=<search term>)
                      retrieve posts having the search term somewhere in the title.
                      Somewhere in... means that word parts are found too!
    :parameter content: Retrieves posts having the search term somewhere in the content.
                        Like the title search the content search finds word parts as well.
    :parameters sort, direction: Sort the found posts according to the direction
    :parameters page, limit: Pagination of the posts with <page> pages having <limit> posts each.
    """
    posts = storage.load_json()
    title = request.args.get('title')
    content = request.args.get('content')
    if title:
        collection = [post for post in posts if title.lower() in post.get('title').lower()]
    if content:
        collection = [post for post in posts if content.lower() in post.get('content').lower()]
    posts = collection
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


@app.route('/api/posts', methods=['POST'])
def create_new_posts():
    """
    Creates a new post from the form fields.
    If the add post button is hit, the data of the form fields are sent via POST
    method to the backend. Detecting this kind of request, the function validates
    the message body for having valid data and sends the new pos to the storage module
    :returns: jsonified post-data and code 201,
              in case of failed validation an error message and code 400 are sent
    """
    if request.method == 'GET':
        # Handle the GET request
        posts = storage.load_json()
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
    """
    Finds the post with the given ID using the storage´s find function.
    uses GET-method to get the id of the post to change,
    uses PUT-Method having the new data in the body to change post.
    :param id: Id of the post to be changed in the url for GET-method
    :returns:jsonified post,
             404 if there is no post with the given id.
    """

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
    """
    Uses GET to retrieve the id of the post which shall be deleted,
    followed by the DELETE-method to delete the post with the given id.
    :param id: id of the post to be deleted
    :returns: jsonified data from the deleted post,
              , Error 404 if there is no post having the given id.
    """
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
    """ Errorhandler for Error 404 (not found) """
    return jsonify({"error": "Post Not Found or Wrong Url"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    """ Errorhandler for Error 405 (Method not allowed) """
    return jsonify({"error": "Method Not Allowed"}), 405


@app.errorhandler(400)
def bad_request(error):
    """ Errorhandler for Error 400 (Bad request) """
    return jsonify({"error": "Request is in bad shape. Missing some field data?"}), 400


def validate_post_data(data):
    """
    Validates the body of a POST request to be sure there is an
    element 'title' and an element 'content'
    The elements´ values are not checked, thus empty posts are still possible.
    parameter data: the POST-request´s body contents
    returns: True if valid,
             False if not.
    """
    if "title" not in data or "content" not in data:
        return False
    return True


if __name__ == '__main__':
    """swagger initialization and start of backend server"""
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Masterblog-API'
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    app.run(host="0.0.0.0", port=5002, debug=True)
