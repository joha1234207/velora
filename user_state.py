# User state management - using simple dictionaries instead of FSM

# Dictionary to store what each user is currently doing
# Keys: user_id
# Values: state name (string)
user_states = {}

# Dictionary to store temporary data for users
# Keys: user_id
# Values: dictionary with temporary data
user_data = {}


def set_state(user_id, state):
    """
    Set the current state of a user
    
    Args:
        user_id: Telegram user ID
        state: State name (string)
    """
    user_states[user_id] = state


def get_state(user_id):
    """
    Get the current state of a user
    
    Args:
        user_id: Telegram user ID
    
    Returns:
        State name or None if not set
    """
    return user_states.get(user_id)


def delete_state(user_id):
    """
    Delete the state of a user
    
    Args:
        user_id: Telegram user ID
    """
    if user_id in user_states:
        del user_states[user_id]


def set_data(user_id, key, value):
    """
    Store temporary data for a user
    
    Args:
        user_id: Telegram user ID
        key: Data key
        value: Data value
    """
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id][key] = value


def get_data(user_id, key):
    """
    Retrieve temporary data for a user
    
    Args:
        user_id: Telegram user ID
        key: Data key
    
    Returns:
        Data value or None if not found
    """
    if user_id not in user_data:
        return None
    return user_data[user_id].get(key)


def clear_data(user_id):
    """
    Clear all temporary data for a user
    
    Args:
        user_id: Telegram user ID
    """
    if user_id in user_data:
        del user_data[user_id]


def clear_all(user_id):
    """
    Clear everything for a user (state + data)
    
    Args:
        user_id: Telegram user ID
    """
    delete_state(user_id)
    clear_data(user_id)


# State constants
class States:
    """Constants for user states"""
    IDLE = "idle"
    REGISTERING = "registering"
    ENTERING_NICKNAME = "entering_nickname"
    ADDING_POST = "adding_post"
    VIEWING_POSTS = "viewing_posts"
    VIEWING_ADMIN_PANEL = "viewing_admin_panel"
    BROADCASTING = "broadcasting"
    CONFIRMING_ACTION = "confirming_action"
