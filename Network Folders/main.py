if __name__ == '__main__':
    from app.app import Application
    app = Application()
    app.acquire_lock()
    
    update = app.try_to_update()
    
    if update is False:
        app.start()
        
    app.release_lock()
    
    from sys import exit
    exit(0)