import json


def save_json(posts):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(posts, file, ensure_ascii=False, indent=4)


def load_json(filepath):
    with open(filepath, 'r') as file:
        posts = json.load(file)
    return posts


def get_highest_id():
    ids = []
    posts = load_json('data.json')
    for post in posts:
        ids.append(post['id'])
    return int(max(ids))


def delete_post(id):
    posts = load_json('data.json')
    for post in posts:
        if post['id'] == id:
            posts.remove(post)
            save_json(posts)
            return f"Successfully deleted {post}"
    return None


def add_post(post):
    posts = load_json('data.json')
    new_id = get_highest_id() + 1
    post['id'] = new_id
    posts.append(post)
    save_json(posts)


def find_post_by_id(id):
    posts = load_json('data.json')
    for post in posts:
        if post['id'] == id:
            return post
    return None


def update_post(updated_post, changes):
    posts = load_json('data.json')
    for post in posts:
        if post['id'] == updated_post['id']:
            post.update(changes)
            save_json(posts)
            return f"Successfully changed post: {post}"
    return None


def main():
    posts = [
        {"id": 1, "title": "First post", "content": "This is the first post."},
        {"id": 2, "title": "Second post", "content": "This is the second post."},
    ]
    save_json(posts)
    get_highest_id()


if __name__ == '__main__':
    main()
