def authenticate(username, password):
    """
    Check if the provided username and password match the stored credentials.
    """
    stored_username = 'brainwave'
    stored_password = '2005'
    return username == stored_username and password == stored_password
