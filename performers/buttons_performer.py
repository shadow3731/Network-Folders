import tkinter as tk
import _tkinter, re, subprocess

import gevent.queue

from dialog import Dialog


class ButtonsPerformer():
    """The class for a Button handling.
    
    Attributes:
        cursor (Cursor): The Cursor object for placing object on the window.
        dp (DataPerformer): The DataPerformer object for handling the data.
        lp (LogsPerformer): The LogsPerformer object for app logging.
    """
    
    def __init__(self, dp, lp=None):
        """Initializes ButtonPerformer instance."""
        
        self.dp = dp
        self.lp = lp
    
    def configure_buttons(self, data, cursor):
        """Configures a Button placement on the window.
        
        Creates an empty list, which may contain Buttons placement 
        on the window divided with Groups. If the application data 
        has information about Groups and Buttons, 
        the list will be added with Buttons. For each group 
        extracts the information about Buttons. Refers to Cursor 
        for getting this Button positions represented as a tuple.
        
        Groups and Buttons can be identified only with sequence numbers. 
        If this sequence is interrupted, the Group is supposed to have 
        no more Buttons and goes to the new Group if it exists.
        
        Args:
            data (dict): The application data.
            
        Returns:
            list: Positions of all the buttons on the window. 
            None: If there are no Groups or Buttons in the application data.
        """
        
        self.lp.log(self.lp.INFO, self.lp.CONFIG_BUTTONS_MESS_ID)
        
        positions = []
        
        if data.get('groups'):
            groups_data = data['groups']
            group_index = 0
                
            while True:
                group_index += 1
                    
                if groups_data.get(f'group{group_index}') and groups_data[f'group{group_index}'].get('buttons'):
                    buttons_data = groups_data[f'group{group_index}']['buttons']
                    button_index = 0
                    positions.append([])
                        
                    while True:
                        button_index += 1
                            
                        if buttons_data.get(f'button{button_index}'):               
                            positions[group_index-1].append(
                                cursor.place_button(
                                    buttons_data[f'button{button_index}']
                                )
                            )
                            
                        else:
                            cursor.move_to_new_group()  
                            break
                else:
                    self.lp.log(self.lp.INFO, self.lp.CONFIG_BUTTONS_SUCC_MESS_ID)
                    
                    return positions
                
        self.lp.log(self.lp.WARN, self.lp.NO_CONFIG_BUTTONS_MESS_ID)
                
        return None
            
    def show_buttons(self, data, positions, root, window):
        """Shows Buttons on the window.
        
        Before displayng, loads the service data for network credentials. 
        If there are Buttons, displays them on the screen at the positions, 
        given by the Cursor. A Button gets certain styles and is binded 
        to open a certain directory or file. Binding starts working by 
        clicking either left mouse button or Enter button.
        
        Args:
            data (dict): The application data,
            positions (list): The positions of all Buttons.
            root (tk.Frame): The root element where Buttons are displayed.
        """
        
        self.lp.log(self.lp.INFO, self.lp.SHOW_BUTTONS_MESS_ID)
        
        s_data = self.dp.service_data
        credentials = {
            'username': s_data[self.dp.username_cred_key],
            'password': s_data[self.dp.password_cred_key]
        }
        timeout = data['dir_open_timeout']
        
        for i in range(len(positions)):
            group_data = data['groups'][f'group{i+1}']
            
            for j in range(len(positions[i])):
                button_data = group_data['buttons'][f'button{j+1}']
                
                try:
                    button = tk.Button(
                        master=root,
                        text=button_data['name'],
                        font=('Calibri', 11, 'bold'),
                        relief=tk.SOLID,
                        borderwidth=1,
                        bg=button_data['bg_color'],
                        fg=button_data['fg_color']
                    )
                except _tkinter.TclError as e:
                    message = f"Обнаружен недопустимый параметр для кнопки.\n\n{e}"
                    Dialog(self.lp).show_error(message, window)  
                
                button.bind(
                    '<Button-1>', 
                    lambda e, 
                        button=button,
                        data=button_data,
                        credentials=credentials: 
                            self._start_action(e, button, data, credentials, timeout, window)
                )
                
                button.bind(
                    '<Return>', 
                    lambda e, 
                        button=button,
                        data=button_data,
                        credentials=credentials: 
                            self._start_action(e, button, data, credentials, timeout, window)
                )
                    
                button.place(
                    x=positions[i][j][0],
                    y=positions[i][j][1],
                    width=positions[i][j][2],
                    height=positions[i][j][3]
                )
                
        self.lp.log(self.lp.INFO, self.lp.SHOW_BUTTONS_SUCC_MESS_ID)
                
    def _start_action(self, event, button, b_data, s_data, timeout, root):
        """Starts some actions after clicking a Button.
        
        Gets name and directory from the clicked Button and renames it 
        to show that the Button was clicked. Starts a thread where 
        the directory is being opened. This action performs in 
        another thread in the purpose not to stop the main thread working.
        
        Args:
            button (tk.Button): The Button object of tkinter,
            b_data (dict): The application data of this Button,
            s_data (dict): The service data,
            timeout (float): The time gap while the app is trying to open a network directory.
        """
        
        self.lp.log(self.lp.INFO, self.lp.PRESS_BUTTON_MESS_ID, (b_data['name'],))
        
        button_name = b_data['name']
        button_dir = b_data['path']
        button.config(text='Подождите')
        
        from threading import Thread
        Thread(
            target=self._open_directory,
            args=(button_dir, button, button_name, s_data, timeout, root),
            name='Directory opening thread',
        ).start()
        
        button.config(
            relief=tk.SOLID,
            borderwidth=1,
            bg=b_data['bg_color'],
            fg=b_data['fg_color']
        )
    
    def _open_directory(self, path, btn, name, creds, timeout, root):
        """Opens a certain directory.
        
        Defines the user's operation system and if this OS is not 
        specific, tries to open the directory within a certain time.
        Tries to open directory using network credentials and if opened, 
        deletes the connection with this network directory. 
        If some operaion failed, shows 'askerror' window with 
        description of the error.
        
        Args:
            dir (str): The network directory to be opened,
            btn (Button): The Button object of tkinter,
            name (str): The name of the Button,
            creds (dict): Network credentials,
            timeout (float): The time gap while the app is trying to open a network directory.
        """
        
        self.lp.log(self.lp.INFO, self.lp.OPEN_DIR_MESS_ID, (path,))
        
        from platform import system
        if system() == 'Windows':            
            try:
                from performers.network_performer import NetworkPerformer
                net_perf = NetworkPerformer(self.lp)
                network_device_name = net_perf.get_network_device_identifier(path)
                
                if network_device_name:                    
                    network_device_ip = net_perf.get_network_device_ip(network_device_name)

                    map_command = net_perf.execute(
                        'win create map', 
                        identifier=network_device_ip,
                        username=creds['username'],
                        password=creds['password'],
                        timeout=timeout,
                        hide_cmd=True,
                    )
                    
                    if map_command.returncode == 0:     
                        self.lp.log(self.lp.INFO, self.lp.RUN_CMD_SUCC_MESS_ID)
                                           
                        directory = path.replace(network_device_name, network_device_ip)
                            
                        self._open_windows_directory(directory, net_perf, timeout, root)
                                
                        del_command = net_perf.execute(
                            'win delete map',
                            identifier=network_device_ip,
                            timeout=timeout,
                            hide_cmd=True,
                        )
                            
                        if del_command.returncode == 0:
                            self.lp.log(self.lp.INFO, self.lp.RUN_CMD_SUCC_MESS_ID)
                            
                        else:
                            self.lp.log(self.lp.INFO, self.lp.RUN_CMD_FAIL_MESS_ID)
                            
                            self._show_error(root, command_result=del_command)
                                
                    else:
                        self.lp.log(self.lp.INFO, self.lp.RUN_CMD_FAIL_MESS_ID)
                        
                        self._show_error(root, command_result=map_command) 
                        
                else:
                    self._open_windows_directory(path, net_perf, timeout, root)
                    
            except subprocess.CalledProcessError as e:
                self._show_error(root, command_result=e)
            except (subprocess.TimeoutExpired, gevent.Timeout) as e:
                message = f'Превышено время ожидания ответа в {timeout} секунд.'
                self._show_error(root, message)
                # Dialog(self.lp).show_error(message, root)
            except FileNotFoundError as e:
                message = 'Не удается найти указанный файл или папку.'
                self._show_error(root, error=e, message=message)
            except PermissionError:
                message = 'Отсутсвует разрешение на открытие указанного файла или папки.'
                self._show_error(root, error=e, message=message)
            except OSError as e:
                self._show_error(root, error=e)
            except Exception as e:
                message = 'Не удалось получить IP-адрес объекта.'
                self._show_error(message, root)
                
            finally:
                btn.config(text=name)
        
        else:
            try:
                subprocess.run(
                    f'echo "{creds["password"]}" | sudo -S open "{path}"'
                )
                
            except subprocess.CalledProcessError as e:
                message = f"Ошибка выполнения консольной команды.\n\n{e}"
                Dialog(self.lp).show_error(message, root)
            except FileNotFoundError as e:
                message = f"Не удалось открыть файл или папку. Возможно имеются проблемы с сетью либо данной директории не существует.\n\n{e}"
                Dialog(self.lp).show_error(message, root)
            except OSError as e:
                message = f"Ошибка в системе.\n\n{e}"
                Dialog(self.lp).show_error(message, root)
            except ValueError as e:
                message = f"Неверное значение.\n\n{e}"
                Dialog(self.lp).show_error(message, root)
            except subprocess.TimeoutExpired as e:
                message = f"Превышено время ожидания открытия файла или папки.\n\n{e}"
                Dialog(self.lp).show_error(message, root)
                
            finally:
                btn.config(text=name)

    def _open_windows_directory(self, directory, net_perf, timeout, root):
        if self._is_file(directory):
            dir_command = net_perf.execute(
                'win open file',
                file=directory,
                timeout=timeout,
            )
            
            if dir_command.returncode == 0:
                self.lp.log(self.lp.INFO, self.lp.RUN_CMD_SUCC_MESS_ID)
            
            if dir_command.returncode == -1:
                self.lp.log(self.lp.INFO, self.lp.RUN_CMD_FAIL_MESS_ID)
                
                message = 'Не найден путь к файлу.'
                self._show_error(root, message=message)
            
        else:
            dir_command = net_perf.execute(
                'win open folder',
                path=directory,
                timeout=timeout,
            )
            
            if dir_command.returncode == 0 or dir_command.returncode == 1:
                self.lp.log(self.lp.INFO, self.lp.RUN_CMD_SUCC_MESS_ID)
                
            else:
                self.lp.log(self.lp.INFO, self.lp.RUN_CMD_FAIL_MESS_ID)
                
                self._show_error(root, command_result=dir_command)
                            
    def _show_error(self, root, message=None, command_result=None, error=None):
        """Shows error if any occured.
        
        Composes a message with the error description and shows it 
        in 'askerror' window.

        Args:
            message (str): The error description,
            command_result (_type_, optional): The subprocess error,
            error (_type_, optional): The OS error.
        """
        
        if command_result:
            msg_cmd = f'net helpmsg {command_result.returncode}'
            msg_cmd_res = subprocess.run(msg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if message:
                msg = f'{message}\n\nСетевая ошибка {command_result.returncode}.\n\n{msg_cmd_res.stdout.decode("ibm866").strip()}\n\n{command_result.stderr.decode("ibm866").strip()}'
            else:
                msg = f'Возникла ошибка при выполнении операции.\n\nСетевая ошибка {command_result.returncode}.\n\n{msg_cmd_res.stdout.decode("ibm866").strip()}\n\n{command_result.stderr.decode("ibm866").strip()}'
        
        elif error:
            if message:
                msg = f'{message}\n\n{error}'
            else:
                msg = f'Возникла ошибка при выполнении операции.\n\n{error}'
                
        else:
            if message:
                msg = message
            else:
                msg = 'Возникла ошибка при выполнении операции.'
                
        Dialog(self.lp).show_error(msg, root)
        
    def _is_file(self, path):
        """Defines if the direcory is file with RegEx.
        
        Returns:
            bool (True): If the directory is a file.
            bool (False): If the direcory is a folder.
        """
        
        file_types = ['.exe', '.txt', '.rtf', '.md', '.html', '.htm', '.xml', '.json', '.csv', '.doc', '.docx', '.xls', '.xlsx', '.xlsm', '.ini', '.yaml', '.yml', '.log', '.sh', '.py', '.js', '.jpg', '.jpeg', '.png', '.bat', '.mp3', '.mp4', '.avi', '.wav', '.wmv', '.mkv']
        pattern = fr'\b(?:{"|".join(re.escape(file_type) for file_type in file_types)})\b'
        return bool(re.search(pattern, path))