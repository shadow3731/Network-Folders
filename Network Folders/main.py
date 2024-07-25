if __name__ == '__main__':
    import sys

    if getattr(sys, 'frozen', False):
        app_dir = f'{sys._MEIPASS}\\Network Folders'
        
    else:
        from pathlib import Path
        app_dir = Path(__file__).resolve().parent

    from app.app import Application
    app = Application(app_dir)
    app.acquire_lock()

    update = app.try_to_update()
            
    if update is False:
        app.start()
                
    app.release_lock()
        
    sys.exit(0)