from app.app import Application


def generate_session_name(length=10):
    """Generates the session name for the application.
    
    This name contains letters, numbers and symbols.

    Args:
        length (int, optional): The length of the session name. Defaults to 10.

    Returns:
        str: The session name.
    """
    
    from random import choice
    from string import ascii_letters, digits, punctuation
    
    
    chars = ascii_letters + digits + punctuation
    return ''.join(choice(chars) for _ in range(length))

if __name__ == '__main__':
    app = Application()
    app.acquire_lock()
    
    session_name = generate_session_name(5)
    app.start(session_name)
    
    app.release_lock()
    exit(0)