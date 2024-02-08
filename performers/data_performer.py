import json, pickle, re, os, subprocess, socket, threading, time

from dialog import Dialog
from performers.logs_performer import LogsPerformer

class DataPerformer():
    """The class for manipulating with service and application data.
    
    Attributes:
        service_data (dict): the app service data.
        current_app_version (str): the current application version.
        support_versions_key (str): the key of the service data which contains application versions that are suitable to this service data.
        lp (LogsPerformer): The LogsPerformer object for app logging.
        a_data_key (str): the key of the service data which contains the filepath to JSON application file.
        a_data_mtime_key (str): the key of the service data representing last modification time of the appearance data located in server.
        creds_import_mode_key (str): the key representing if network credentials are imported from the application data.
        username_cred_key (str): the key of the service data which contains the username of network credentials.
        password_cred_key (str): the key of the service data which contains the password of network credentials.
        server_device_name (str | None): the computer name where the application data is taken from.
        valid_service_data_pattern (dict): the pattern of the service data.
        service_file_dir (str): the service data directory.
        data_file_dir (str): the local application data directory.
    """
    
    def __init__(self, lp: LogsPerformer):
        """Initializes DataPerformer instance."""
        
        self.service_data: dict = None
        self.server_device_name: str = None
        
        self.lp = lp
        
        self.current_app_version = '1.6'
        self.suppotred_versions = [
            '1.5', '1.6'
        ]
        
        self.support_versions_key = 'supports'
        self.a_data_key = 'app_data_file_path'
        self.a_data_mtime_key = 'app_data_mtime'
        self.creds_import_mode_key = 'credentials_import_mode'
        self.username_cred_key = 'username_credentials'
        self.password_cred_key = 'password_credentials'
        
        self.valid_service_data_pattern = {
            self.support_versions_key: ', '.join(self.suppotred_versions),
            self.a_data_key: '',
            self.a_data_mtime_key: time.mktime((2000, 1, 1, 0, 0, 0, 0, 0, 0)),
            self.creds_import_mode_key: 'False',
            self.username_cred_key: '',
            self.password_cred_key: ''
        }
        
        self.service_file_dir = 'config\\local_data.picke'
        self.data_file_dir = 'config\\local_app_data.json'
                
    def load_service_data(self):  
        """Loads the service data.
        
        Tries to get file with the service data of the application. 
        If there is no file containing the service data, creates it.
        Checks if loaded service data is valid. 
        Gets server IP-address or name.
        
        Returns:
            dict: The service data, if the service data from file was read successfully.
        """
        
        self.lp.log(self.lp.INFO, self.lp.LOAD_S_DATA_MESS_ID, (self.service_file_dir,))
            
        self._create_if_not_exists('service_data', self.service_file_dir)
            
        with open(self.service_file_dir, 'rb') as f:
            data: dict = pickle.load(f)
            
        self.service_data = self._get_valid_service_data(data)
                
        self.server_device_name = self._get_computer_ip_or_name(
            filepath=data[self.a_data_key]
        )
        
        self.lp.log(self.lp.INFO, self.lp.LOAD_S_DATA_SUCC_MESS_ID, (self.service_file_dir,))
        
    def save_service_data(self, savable_data: dict):
        """Saves the service data.
        
        Tries to save new or updated service data.
        If failed, shows the error message.
        
        Args:
            savable_data (dict): the new or updated service data.
        """
        
        self.lp.log(self.lp.INFO, self.lp.SAVE_S_DATA_MESS_ID, (self.service_file_dir,))
        
        try:
            with open(self.service_file_dir, 'wb') as f:
                pickle.dump(savable_data, f)
                self.service_data = savable_data
                
                self.lp.log(self.lp.INFO, self.lp.SAVE_S_DATA_SUCC_MESS_ID, (self.service_file_dir,))
                
        except PermissionError as e:
            self.lp.log(self.lp.ERR, self.lp.SAVE_S_DATA_FAIL_MESS_ID, (self.service_file_dir, e,))
            
            message = (
                'Не удалось создать служебный файл из-за отсутствия необходимых прав. '
                'Запустите программу с правами администратора или '
                'обратитесь за помощью к системному администратору.'
            )
            Dialog(self.lp).show_error(message)
                
    def load_application_data_from_server(self, filepath: str) -> dict:
        """Loads the application data from a server.
        
        If the server is defined and is currently online,
        connects to the filepath of the server, where the application data is.
        If the filepath exists, reads the application data
        and returns it.
        
        UTF-8-sig is used as a decoder of the application data,
        because the file with the application data might have
        unrecognized for regular UTF-8 decoder characters.
        
        If the file has invalid JSON syntaxis or unrecognized
        for UTF-8-sig decoder characters, creates 'askerror' window
        with error description and tries to load the application data locally.
        
        Args:
            filepath (str): the filepath of the file with application data which is on the server computer.
            
        Returns:
            dict: The application data, if the file was found and was correctly read or tries to do it locally.
        """
        
        self.lp.log(self.lp.INFO, self.lp.LOAD_A_DATA_FROM_SERV_MESS_ID, (filepath,))
        
        if self.server_device_name and self._is_server_online(self.server_device_name):
            if os.path.exists(filepath):
                try:
                    with open(filepath, encoding='utf-8-sig') as f:
                        self.lp.log(self.lp.INFO, self.lp.LOAD_A_DATA_FROM_SERV_SUCC_MESS_ID, (filepath,))
                        
                        return json.load(f)
                    
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    self.lp.log(self.lp.ERR, self.lp.LOAD_A_DATA_FROM_SERV_FAIL_MESS_ID, (filepath, e))
                    
                    message = f'Не удалось выгрузить данные из файла конфигурации, находящегося на сервере.\n\n{e}'
                        
                    dialog = Dialog(self.lp)
                    threading.Thread(
                        target=dialog.show_error,
                        args=(message,)
                    ).start()
                    
        self.lp.log(self.lp.INFO, self.lp.LOAD_A_DATA_TRY_LOCAL_MESS_ID)
        
        return self.load_application_data_locally()
        
    def load_application_data_locally(self) -> dict:
        """Loads the application data from the user's local computer.
        
        If the path to the file with application data exists, reads and returns it.
        
        UTF-8-sig is used as a decoder of the application data,
        because the file with the application data might have
        unrecognized for regular UTF-8 decoder characters.
        
        If the file has invalid JSON syntaxis or unrecognized
        for UTF-8-sig decoder characters, creates 'askerror' window
        with error description.
            
        Returns:
            dict: The application data, if the file was found and was correctly read. 
            None: If filepath to the file does not exist, or if an error occured while reading the file.
        """
        
        self.lp.log(self.lp.INFO, self.lp.LOAD_A_DATA_LOCAL_MESS_ID, (self.data_file_dir,))
        
        if os.path.exists(self.data_file_dir):
            try:
                with open(self.data_file_dir, encoding='utf-8-sig') as f:
                    self.lp.log(self.lp.INFO, self.lp.LOAD_A_DATA_LOCAL_SUCC_MESS_ID, (self.data_file_dir,))
                    
                    return json.load(f)
                    
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                self.lp.log(self.lp.ERR, self.lp.LOAD_A_DATA_LOCAL_FAIL_MESS_ID, (self.data_file_dir, e))
                
                message = f'Не удалось выгрузить данные из файла визуализации, находящегося на этом устройстве.\n\n{e}'
                dialog = Dialog(self.lp)
                threading.Thread(
                    target=dialog.show_error,
                    args=(message,)
                ).start()
        
        return None
    
    def save_appearance_data(self, savable_data: dict):
        """Saves the application data.
        
        Before saving, rewrites last modification time of the application data.
        
        UTF-8-sig is used as an encoder of the application data,
        because the savable application data might have
        unrecognized for regular UTF-8 encoder characters.
        
        Args:
            savable_data (dict): the new or updated application data.
        """
        
        try:
            with open(self.data_file_dir, 'w', encoding='utf-8-sig') as f:
                json.dump(savable_data, f, indent=4)
                
            self.service_data[self.a_data_mtime_key] = os.path.getmtime(self.service_data[self.a_data_key])
            
            self.lp.log(self.lp.INFO, self.lp.EDIT_S_DATA_MESS_ID, (self.a_data_mtime_key, self.service_data[self.a_data_mtime_key],))
            
            self.save_service_data(self.service_data)
        
        except PermissionError:
            message = (
                'Не удалось сохранить файл конфигурации из-за отсутствия необходимых прав. '
                'Запустите программу с правами администратора или '
                'обратитесь за помощью к системному администратору.'
            )
            Dialog(self.lp).show_error(message)
    
    def _create_if_not_exists(self, target: str, filepath: str=None):
        """Creates file if it does not exist.
        
        The file with service data is required to be not readable 
        with regular methods, so it is encrypted 
        (and then decrypted when is loaded) with pickle module.
        
        Args:
            target (str): the file which is needed to create,
            filepath (str): the path of this file.
        """
        
        self.lp.log(self.lp.INFO, self.lp.CHECK_S_DATA_EXISTS_MESS_ID)
        
        if target == 'service_data':
            if not os.path.exists(filepath):
                self.lp.log(self.lp.WARN, self.lp.NO_S_DATA_AND_CREATE_MESS_ID, (self.service_file_dir,))
                
                self.save_service_data(self.valid_service_data_pattern)
                
            else:
                self.lp.log(self.lp.INFO, self.lp.S_DATA_EXISTS_MESS_ID)
                    
    def _get_valid_service_data(self, data: dict) -> dict:
        """Returns valid service data.
        
        If incoming service data is valid, just returns it.
        If not, saves and returns the new one.

        Args:
            data (dict): the service data.

        Returns:
            dict: the valid service data.
        """
        
        self.lp.log(self.lp.INFO, self.lp.CHECK_S_DATA_VALID_MESS_ID)
        
        if data.get(self.support_versions_key) and self.current_app_version in data.get(self.support_versions_key):
            self.lp.log(self.lp.INFO, self.lp.S_DATA_VALID_MESS_ID)
            
            return data
        
        else:
            self.lp.log(self.lp.WARN, self.lp.S_DATA_INVALID_AND_CREATE_MESS_ID)
            
            data = self.valid_service_data_pattern
            self.save_service_data(data)
            return data
        
    def _get_computer_ip_or_name(self, filepath: str) -> str:
        """Gets the server computer IP or name.
        
        Defines the server computer IP or name by the path
        where the file with the application data is.
        Separates the server name from the filepath by RegEx.
        
        Args:
            filepath (str): the path to the file with the application data.
            
        Returns:
            str: The server computer IP or name if defined.
            None: If not.
        """
        
        self.lp.log(self.lp.INFO, self.lp.CHECK_SERV_NAME_MESS_ID)
        
        match = re.match(r'//([^/]+)', filepath)
        
        if match:
            identifier = match.group(1)
            
            self.lp.log(self.lp.INFO, self.lp.GOT_SERV_NAME_MESS_ID, (identifier,))
            
            return identifier
        
        self.lp.log(self.lp.WARN, self.lp.NO_SERV_NAME_MESS_ID)
        
        return None
        
    def _is_server_online(self, host: str) -> bool:
        """Defines if the server computer is online.
        
        Run command to define if the server computer is online.
        The command pings the server computer sending there
        1 packet within 1 second. After that generates a code
        of the command result. If it differs from 0,
        tries to connect to the server computer by sockets.
        
        Returns:
            bool (True): If the result code is 0 or the socket connection to the server computer is established.
            bool (False): If not.
        """
        
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '1', host], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if result.returncode == 0:
            return True
        
        else:
            try:
                ip = socket.gethostbyname(host)
                return True
            
            except socket.gaierror:
                return False
            
    def check_file_modified(self, filepath: str) -> bool:
        """Checks if the server application data was modified.

        Args:
            filepath (str): the path to the server application data.

        Returns:
            bool: True - if filepath is not empty and the server application data was modified. False - otherwise.
        """
        
        if filepath != '':
            try:
                server_a_data_mtime = os.path.getmtime(filepath)
                local_a_data_mtime = float(self.service_data[self.a_data_mtime_key])
                
                if not os.path.exists(self.data_file_dir) or server_a_data_mtime > local_a_data_mtime:
                    return True
                else:
                    return False
                
            except (OSError, ValueError):
                pass
            
        return False