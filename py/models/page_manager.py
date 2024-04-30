from cryptography.fernet import Fernet

class PageManager:
    def __init__(self, db_connection, encryption_key):
        self.db_connection = db_connection
        self.fernet = Fernet(encryption_key)
        
    # set_page
    
    # clear_page
    
    # get_page_state_by_number
    
    # search_page_state
    
    # plus_page_state
    
    # random_password_settings
    
    # create_random_password
    
    # about_page_state
    
    