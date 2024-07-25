print('0')
if __name__ == '__main__':
    print('1')
    import sys

    print('2')
    if getattr(sys, 'frozen', False):
        app_dir = f'{sys._MEIPASS}/Network Folders'
    
    else:
        from pathlib import Path
        app_dir = Path(__file__).resolve().parent

    print('3')
    from app.app import Application
    print('4')
    app = Application(app_dir)
    print('5')
    app.acquire_lock()

    print('6')    
    update = app.try_to_update()
        
    if update is False:
        print('7')
        app.start()
            
    app.release_lock()
        
    sys.exit(0)