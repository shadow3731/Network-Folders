import random, string

from app.app import Application

def _generate_session_name(length: int=10) -> str:
    """Generates the session name for the application.
    
    This name contains letters, numbers and symbols.

    Args:
        length (int, optional): The length of the session name. Defaults to 10.

    Returns:
        str: The session name.
    """
    
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

if __name__ == '__main__':
    Application(_generate_session_name(5)).start()