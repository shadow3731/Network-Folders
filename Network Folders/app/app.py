import os, portalocker
from sys import exit

from app.window.window_factory import WindowFactory
from app.performer.logs_performer import LogsPerformer
from app.performer.data_performer import DataPerformer


class Application():
    def __init__(self):
        self._lockfile = '../temp/app.lock'
        
        self.logs_perf = LogsPerformer()
        self.win_factory = WindowFactory(self.logs_perf)
        self.data_perf = None
        
    def acquire_lock(self):
        lockfile_dir = os.path.dirname(self._lockfile)
        os.makedirs(lockfile_dir, exist_ok=True)
        
        self.fd = open(self._lockfile, 'w')
        try:
            portalocker.lock(self.fd, portalocker.LOCK_EX | portalocker.LOCK_NB)
            
        except portalocker.LockException:
            main_window = self.win_factory.create_main()
            
            from app.window.dialog import Dialog
            Dialog(self.logs_perf).show_error('Программа уже запущена!', main_window)
            
            main_window.destroy()
            exit(0)
            
        except PermissionError:
            pass
            
    def release_lock(self):        
        try:
            portalocker.unlock(self.fd)
            self.fd.close()
            os.unlink(self._lockfile)
            
        except PermissionError:
            pass
        
    def try_to_update(self):
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.CHECK_UPDATER_MESS_ID)
        
        main_window = self.win_factory.create_main()
        
        self.data_perf = DataPerformer(main_window, self.logs_perf)
        self.data_perf.load_service_data()
        
        latest_version = self.data_perf.service_data[self.data_perf.latest_version_key]
        archive_file = f'Network.Folders.v.{latest_version}.Setup.zip'
        
        if os.path.exists(archive_file):
            self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.FOUND_UPDATER_MESS_ID, (archive_file,))
            
            installer_file = 'Network Folders Setup.exe'
            updater_file = 'update.py'
            
            import zipfile
            with zipfile.ZipFile(archive_file, 'r') as zip_ref:
                zip_ref.extractall('.', (installer_file, updater_file,))
                
            import subprocess
            args = [archive_file, installer_file, updater_file,]
            subprocess.Popen(['python', updater_file] + args)
            
            main_window.destroy()
            
            return True
            
        else:
            self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.NO_UPDATER_MESS_ID)
            
            main_window.destroy()
            
            return False
        
    def start(self):
        from time import time
        start_time = time()
        
        session_name = self.generate_session_name(5)
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.APP_LAUNCH_MESS_ID, (session_name,))
                
        loading_window = self.win_factory.create_and_preapare_loader()
        main_window = self.win_factory.create_main()
        
        if not self.data_perf:
            self.data_perf = DataPerformer(main_window, self.logs_perf)
            self.data_perf.load_service_data()
        self.data_perf.root = main_window
        
        from app.util.validator import Validator
        raw_app_data = self.data_perf.load_application_data_locally()
        valid_app_data = Validator(self.logs_perf).validate_app_data(raw_app_data, main_window)
        
        from app.util.updater import Updater
        updater = Updater(self.logs_perf)
        
        from threading import Thread
        Thread(
            target=self.data_perf.update_application_file,
            name='Appearance data updating thread',
        ).start()
        Thread(
            target=updater.check_for_update,
            args=(self.data_perf,),
            name='Application auto update thread',
        ).start()
        
        first_launched = self.data_perf.service_data[self.data_perf.first_launch_key]
            
        if first_launched is True or self.data_perf.service_data[self.data_perf.creds_import_mode_key] == 'True':
            self.data_perf.save_credentials(
                valid_app_data['credentials']['username'],
                valid_app_data['credentials']['password'],
            )
            
            if first_launched is True:
                self.data_perf.save_first_launch(False)
            
        self.win_factory.prepare_main(main_window, valid_app_data, self.data_perf)
        
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.DESTROY_LOADER_MESS_ID)
        
        loading_window.destroy()
        
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.DESTROY_LOADER_SUCC_MESS_ID)
        
        from decimal import Decimal, ROUND_DOWN
        time_delta = float(Decimal(str(time() - start_time)).quantize(Decimal('0.000'), rounding=ROUND_DOWN))
        
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.TIME_LAUNCH_MESS_ID, (time_delta,))
        
        optimal_time = 8
        if time_delta >= optimal_time:
            self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.WARN_TIME_LAUNCH_MESS_ID, (optimal_time,))
        
        main_window.mainloop()
        
    def generate_session_name(self, length=10):
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