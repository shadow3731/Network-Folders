if __name__ == '__main__':
    from app.app import Application
    app = Application()
    app.acquire_lock()
    
    data_perf = app.update_or_get_data_performer()
    
    if data_perf:
        app.start()
        
    app.release_lock()
    
    from sys import exit
    exit(0)
    
    
# внедрить автообновление программы