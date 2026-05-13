import requests
import random

from config import SUPABASE_URL, SUPABASE_API_KEY

# =========================
# Headers
# =========================

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# =========================
# Helper request
# =========================

def supabase_request(method, table, params=None, data=None):

    url = f"{SUPABASE_URL}/rest/v1/{table}"

    response = requests.request(
        method=method,
        url=url,
        headers=HEADERS,
        params=params,
        json=data
    )

    return response


# =========================
# Add post
# =========================

def add_post(user_id, content):

    response = supabase_request(
        "POST",
        "posts",
        params={
            "select": "*"
        },
        data={
            "user_id": user_id,
            "content": content
        }
    )

    if not response:
        return None

    print(response.status_code)
    print(response.text)

    try:

        data = response.json()

        if data:
            return data[0]["post_id"]

    except Exception as e:

        print("JSON ERROR:", e)
        print("Response:", response.text)

    return None

# =========================
# Get post by id
# =========================

def get_post_by_id(post_id):

    response = supabase_request(
        "GET",
        "posts",
        params={
            "post_id": f"eq.{post_id}",
            "select": "post_id,user_id,content,created_at,is_reported,users(nickname)"
        }
    )

    data = response.json()

    if data:

        post = data[0]

        return {
            "post_id": post["post_id"],
            "user_id": post["user_id"],
            "content": post["content"],
            "nickname": post["users"]["nickname"],
            "created_at": post["created_at"],
            "is_reported": post["is_reported"]
        }

    return None


# =========================
# Random post
# =========================

def get_random_post(exclude_user_id=None):

    params = {
        "is_reported": "eq.false",
        "select": "post_id,user_id,content,created_at,users(nickname)"
    }

    if exclude_user_id:
        params["user_id"] = f"neq.{exclude_user_id}"

    response = supabase_request(
        "GET",
        "posts",
        params=params
    )

    data = response.json()

    if not data:
        return None

    post = random.choice(data)

    return {
        "post_id": post["post_id"],
        "user_id": post["user_id"],
        "content": post["content"],
        "nickname": post["users"]["nickname"],
        "created_at": post["created_at"]
    }


# =========================
# User posts
# =========================

def get_user_posts(user_id):

    response = supabase_request(
        "GET",
        "posts",
        params={
            "user_id": f"eq.{user_id}",
            "is_reported": "eq.false",
            "order": "created_at.desc",
            "select": "post_id,user_id,content,created_at"
        }
    )

    return response.json()


# =========================
# Delete post
# =========================

def delete_post(post_id):

    try:

        # Delete reactions first
        reactions_response = supabase_request(
            "DELETE",
            "reactions",
            params={
                "post_id": f"eq.{post_id}"
            }
        )

        print("REACTIONS DELETE:", reactions_response.status_code)

        # Delete post
        response = supabase_request(
            "DELETE",
            "posts",
            params={
                "post_id": f"eq.{post_id}"
            }
        )

        print("POST DELETE:", response.status_code)
        print(response.text)

        return response.status_code in [200, 204]

    except Exception as e:

        print("DELETE ERROR:", e)
        return False

# =========================
# Report post
# =========================

def report_post(post_id):

    response = supabase_request(
        "PATCH",
        "posts",
        params={
            "post_id": f"eq.{post_id}"
        },
        data={
            "is_reported": True
        }
    )

    return response.status_code in [200, 204]


# =========================
# Reported posts
# =========================

def get_reported_posts():

    response = supabase_request(
        "GET",
        "posts",
        params={
            "is_reported": "eq.true",
            "order": "created_at.desc",
            "select": "post_id,user_id,content,created_at,users(nickname)"
        }
    )

    data = response.json()

    posts = []

    for post in data:

        posts.append({
            "post_id": post["post_id"],
            "user_id": post["user_id"],
            "content": post["content"],
            "nickname": post["users"]["nickname"],
            "created_at": post["created_at"]
        })

    return posts


# =========================
# Toggle reaction
# =========================

def toggle_reaction(user_id, post_id, reaction_type):

    response = supabase_request(
        "GET",
        "reactions",
        params={
            "user_id": f"eq.{user_id}",
            "post_id": f"eq.{post_id}",
            "select": "reaction_id,reaction_type"
        }
    )

    data = response.json()

    if data:

        existing = data[0]

        # Same reaction
        if existing["reaction_type"] == reaction_type:

            supabase_request(
                "DELETE",
                "reactions",
                params={
                    "reaction_id": f"eq.{existing['reaction_id']}"
                }
            )

            return "removed"

        # Change reaction
        else:

            supabase_request(
                "PATCH",
                "reactions",
                params={
                    "reaction_id": f"eq.{existing['reaction_id']}"
                },
                data={
                    "reaction_type": reaction_type
                }
            )

            return "changed"

    else:

        supabase_request(
            "POST",
            "reactions",
            data={
                "user_id": user_id,
                "post_id": post_id,
                "reaction_type": reaction_type
            }
        )

        return "added"


# =========================
# Get reactions
# =========================

def get_post_reactions(post_id):

    response = supabase_request(
        "GET",
        "reactions",
        params={
            "post_id": f"eq.{post_id}",
            "select": "reaction_type"
        }
    )

    data = response.json()

    likes = 0
    dislikes = 0

    for reaction in data:

        if reaction["reaction_type"] == "like":
            likes += 1

        elif reaction["reaction_type"] == "dislike":
            dislikes += 1

    return {
        "likes": likes,
        "dislikes": dislikes
    }


# =========================
# User reaction
# =========================

def get_user_reaction(user_id, post_id):

    response = supabase_request(
        "GET",
        "reactions",
        params={
            "user_id": f"eq.{user_id}",
            "post_id": f"eq.{post_id}",
            "select": "reaction_type"
        }
    )

    data = response.json()

    if data:
        return data[0]["reaction_type"]

    return None


# =========================
# Format post
# =========================

def format_post_text(post_data, show_nickname=True):

    text = f"<b>{post_data['content']}</b>\n\n"

    if show_nickname:
        text += f"👤 <i>@{post_data['nickname']}</i>"

    return text