import json
import os

STORAGE_PATH = f"""{os.path.abspath(os.path.join(os.path.dirname(__file__), 'data.json'))}"""


def save_json(posts):
    with open(STORAGE_PATH, 'w') as file:
        json.dump(posts, file, indent=4)


def load_json():
    with open(STORAGE_PATH, 'r') as file:
        posts = json.load(file)
    return posts


def get_highest_id():
    ids = []
    posts = load_json()
    for post in posts:
        ids.append(post['id'])
    return int(max(ids))


def delete_post(id):
    posts = load_json()
    for post in posts:
        if post['id'] == id:
            posts.remove(post)
            save_json(posts)
            return f"Successfully deleted {post}"
    return None


def add_post(post):
    posts = load_json()
    new_id = get_highest_id() + 1
    post['id'] = new_id
    posts.append(post)
    save_json(posts)


def find_post_by_id(id):
    posts = load_json()
    for post in posts:
        if post['id'] == id:
            return post
    return None


def update_post(updated_post, changes):
    posts = load_json()
    for post in posts:
        if post['id'] == updated_post['id']:
            post.update(changes)
            save_json(posts)
            return f"Successfully changed post: {post}"
    return None


def main():
    pass

if __name__ == '__main__':
    main()
