import requests
import re
from config import (
    SUPABASE_URL,
    SUPABASE_API_KEY,
    NICKNAME_MIN_LENGTH,
    NICKNAME_MAX_LENGTH,
    POST_MAX_LENGTH
)

# =========================
# Headers
# =========================

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

# =========================
# Helper function
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
# Validate nickname
# =========================

def validate_nickname(nickname):

    if len(nickname) < NICKNAME_MIN_LENGTH:
        return False

    if len(nickname) > NICKNAME_MAX_LENGTH:
        return False

    if not re.match(r"^[a-zA-Z0-9_]+$", nickname):
        return False

    return True


# =========================
# Check nickname
# =========================

def is_nickname_taken(nickname):

    response = supabase_request(
        "GET",
        "users",
        params={
            "nickname": f"ilike.{nickname}",
            "select": "user_id"
        }
    )

    data = response.json()

    return len(data) > 0


# =========================
# Register user
# =========================

def register_user(user_id, nickname):

    response = supabase_request(
        "POST",
        "users",
        data={
            "user_id": user_id,
            "nickname": nickname
        }
    )

    return response.status_code in [200, 201]


# =========================
# User exists
# =========================

def user_exists(user_id):

    response = supabase_request(
        "GET",
        "users",
        params={
            "user_id": f"eq.{user_id}",
            "select": "user_id"
        }
    )

    data = response.json()

    return len(data) > 0


# =========================
# Get nickname
# =========================

def get_user_nickname(user_id):

    response = supabase_request(
        "GET",
        "users",
        params={
            "user_id": f"eq.{user_id}",
            "select": "nickname"
        }
    )

    data = response.json()

    if data:
        return data[0]["nickname"]

    return None


# =========================
# Validate post length
# =========================

def validate_post_length(content):

    return len(content) > 0 and len(content) <= POST_MAX_LENGTH


# =========================
# Get user id by nickname
# =========================

def get_user_id_by_nickname(nickname):

    response = supabase_request(
        "GET",
        "users",
        params={
            "nickname": f"ilike.{nickname}",
            "select": "user_id"
        }
    )

    data = response.json()

    if data:
        return data[0]["user_id"]

    return None


# =========================
# Total users
# =========================

def get_total_users():

    response = supabase_request(
        "GET",
        "users",
        params={
            "select": "user_id"
        }
    )

    data = response.json()

    return len(data)


# =========================
# Total posts
# =========================

def get_total_posts():

    response = supabase_request(
        "GET",
        "posts",
        params={
            "is_reported": "eq.false",
            "select": "post_id"
        }
    )

    data = response.json()

    return len(data)


# =========================
# Reported posts
# =========================

def get_total_reported_posts():

    response = supabase_request(
        "GET",
        "posts",
        params={
            "is_reported": "eq.true",
            "select": "post_id"
        }
    )

    data = response.json()

    return len(data)


# =========================
# User posts count
# =========================

def get_user_posts_count(user_id):

    response = supabase_request(
        "GET",
        "posts",
        params={
            "user_id": f"eq.{user_id}",
            "is_reported": "eq.false",
            "select": "post_id"
        }
    )

    data = response.json()

    return len(data)


# =========================
# User likes count
# =========================

def get_user_likes_count(user_id):

    # 1. User postlarini olish
    response = supabase_request(
        "GET",
        "posts",
        params={
            "user_id": f"eq.{user_id}",
            "select": "post_id"
        }
    )

    posts = response.json()

    if not posts:
        return 0

    post_ids = [str(post["post_id"]) for post in posts]

    ids = ",".join(post_ids)

    # 2. Like count
    response = supabase_request(
        "GET",
        "reactions",
        params={
            "post_id": f"in.({ids})",
            "reaction_type": "eq.like",
            "select": "reaction_id"
        }
    )

    likes = response.json()

    return len(likes)


# =========================
# Broadcast
# =========================

def broadcast_message(message, user_ids):

    return user_ids