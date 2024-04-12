import os, portalocker

from .window_factory import WindowFactory


class Application():
    def __init__(self):
        self._lockfile = '../temp/app.lock'
        
        self.win_factory = WindowFactory()
        
    def acquire_lock(self):
        lockfile_dir = os.path.dirname(self._lockfile)
        os.makedirs(lockfile_dir, exist_ok=True)
        
        self.fd = open(self._lockfile, 'w')
        try:
            portalocker.lock(self.fd, portalocker.LOCK_EX | portalocker.LOCK_NB)
            
        except portalocker.LockException:
            main_window = self.win_factory.create_main()
            
            from dialog import Dialog
            Dialog().show_error('Программа уже запущена!', main_window)
            
            main_window.destroy()
            exit(0)
            
    def release_lock(self):
        portalocker.unlock(self.fd)
        self.fd.close()
        os.unlink(self._lockfile)
        
    def start(self, session_name='00000'):
        from time import time
        start_time = time()
        
        from performers.logs_performer import LogsPerformer
        logs_perf = LogsPerformer()
        logs_perf.log(logs_perf.INFO, logs_perf.APP_LAUNCH_MESS_ID, (session_name,))

        self.win_factory.logs_perf = logs_perf
                
        loading_window = self.win_factory.create_and_preapare_loader()
        main_window = self.win_factory.create_main()
        
        from performers.data_performer import DataPerformer
        data_perf = DataPerformer(main_window, logs_perf)
        data_perf.load_service_data()
        
        from validator import Validator
        raw_app_data = data_perf.load_application_data_locally()
        valid_app_data = Validator(logs_perf).validate_app_data(raw_app_data, main_window)
        
        from threading import Thread
        Thread(
            target=data_perf.update_application_file,
            name='Appearance data updating thread',
        ).start()
        
        if data_perf.service_data[data_perf.creds_import_mode_key] == 'True':
            data_perf.save_credentials(
                valid_app_data['credentials']['username'],
                valid_app_data['credentials']['password'],
            )
            
        self.win_factory.prepare_main(main_window, valid_app_data, data_perf)
        
        logs_perf.log(logs_perf.INFO, logs_perf.DESTROY_LOADER_MESS_ID)
        
        loading_window.destroy()
        
        logs_perf.log(logs_perf.INFO, logs_perf.DESTROY_LOADER_SUCC_MESS_ID)
        
        from decimal import Decimal, ROUND_DOWN
        time_delta = float(Decimal(str(time() - start_time)).quantize(Decimal('0.000'), rounding=ROUND_DOWN))
        
        logs_perf.log(logs_perf.INFO, logs_perf.TIME_LAUNCH_MESS_ID, (time_delta,))
        
        optimal_time = 8
        if time_delta >= optimal_time:
            logs_perf.log(logs_perf.INFO, logs_perf.WARN_TIME_LAUNCH_MESS_ID, (optimal_time,))
        
        main_window.mainloop()