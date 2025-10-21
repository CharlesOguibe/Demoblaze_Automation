import random
import string

def generate_random_user():
    """Generate a random username and password."""
    username = "user_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return username, password
