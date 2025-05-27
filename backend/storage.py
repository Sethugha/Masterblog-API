import json
import os

"""
Retrieve the absolute path of the storage file. The relative path fails sometimes
for still unknown reasons, thus the usage of the absolute path.
"""
STORAGE_PATH = f"""{os.path.abspath(os.path.join(os.path.dirname(__file__), 'data.json'))}"""


def save_json(posts):
    """
    Saves the complete in-memory storage
    into the storage file determined by STORAGE_PATH.
    :parameter posts: Storage variable (in-memory storage)
    :return: No return
    """
    with open(STORAGE_PATH, 'w') as file:
        json.dump(posts, file, indent=4)


def load_json():
    """
    Loads storage file contents into memory
    as list of dictionaries.
    return: List of dict
    """
    with open(STORAGE_PATH, 'r') as file:
        posts = json.load(file)
    return posts


def get_highest_id():
    """ loads all posts to find the highest id. Returns the highest id as int. """
    ids = []
    posts = load_json()
    for post in posts:
        ids.append(post['id'])
    return int(max(ids))


def delete_post(id):
    """
    Deletes post with given id.
    :parameter id: Id of the post to be deleted
    :returns: Message containing post id if successful
              None if the deletion failed. No causal investigation yet.
    """
    posts = load_json()
    for post in posts:
        if post['id'] == id:
            posts.remove(post)
            save_json(posts)
            return f"Successfully deleted {post}"
    return None


def add_post(post):
    """
    Adds a new post to the storage:
    -The complete storage is loaded into a list of dicts,
    -the highest id is determined and increased by 1
     creating the id of the new post
    -the new post´s id is filled in and the new dict
     is appended to the dictionaries´ list.
    :param post: dictionary with the new post´s data exclusive the id which is empty
    No return
    """
    posts = load_json()
    new_id = get_highest_id() + 1
    post['id'] = new_id
    posts.append(post)
    save_json(posts)


def find_post_by_id(id):
    """
    Retrieves a single post by id
    iterating through the complete data.
    parameter id: ID of the post sought-after.
    returns: The post as dict if found,
             'None' if not
    """
    posts = load_json()
    for post in posts:
        if post['id'] == id:
            return post
    return None


def update_post(updated_post, changes):
    """
    Updates a single post with predefined changes
    the post is determined in the backend, sent complete 'as is'
    to this function together with the planned changes
    (The body of the originating request).
    parameter updated_post: The post which will be updated, original version
    parameter changes: dictionary with the elements to change: post title and/or content
    returns: If successful, message containing the post,
             'None' if unsuccessful.
    """
    posts = load_json()
    for post in posts:
        if post['id'] == updated_post['id']:
            post.update(changes)
            save_json(posts)
            return f"Successfully changed post: {post}"
    return None


def main():
    """Only used for simple tests"""
    pass

if __name__ == '__main__':
    main()
