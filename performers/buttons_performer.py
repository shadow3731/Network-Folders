import tkinter as tk
from tkinter.font import Font
import _tkinter, re, subprocess, platform, threading, socket
from typing import Optional, Union

from cursor import Cursor
from dialog import Dialog
from performers.data_performer import DataPerformer
from performers.logs_performer import LogsPerformer


class ButtonsPerformer():
    """The class for a Button handling.
    
    Attributes:
        cursor (Cursor): The Cursor object for placing object on the window.
        dp (DataPerformer): The DataPerformer object for handling the data.
        lp (LogsPerformer): The LogsPerformer object for app logging.
    """
    
    def __init__(self, cursor: Cursor, dp: DataPerformer, lp: LogsPerformer):
        """Initializes ButtonPerformer instance."""
        
        self.cursor = cursor
        self.dp = dp
        self.lp = lp
    
    def configure_buttons(self, data: dict) -> list:
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
        
        positions: list = []
        
        if data.get('groups'):
            groups_data: dict = data['groups']
            group_index = 0
                
            while True:
                group_index += 1
                    
                if groups_data.get(f'group{group_index}') and groups_data[f'group{group_index}'].get('buttons'):
                    buttons_data: dict = groups_data[f'group{group_index}']['buttons']
                    button_index = 0
                    positions.append([])
                        
                    while True:
                        button_index += 1
                            
                        if buttons_data.get(f'button{button_index}'):               
                            positions[group_index-1].append(
                                self.cursor.place_button(
                                    buttons_data[f'button{button_index}']
                                )
                            )
                            
                        else:
                            self.cursor.move_to_new_group()  
                            break
                else:
                    self.lp.log(self.lp.INFO, self.lp.CONFIG_BUTTONS_SUCC_MESS_ID)
                    
                    return positions
                
        self.lp.log(self.lp.WARN, self.lp.NO_CONFIG_BUTTONS_MESS_ID)
                
        return None
            
    def show_buttons(self, data: dict, positions: list, root: tk.Frame):
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
            group_data: dict = data['groups'][f'group{i+1}']
            
            for j in range(len(positions[i])):
                button_data = group_data['buttons'][f'button{j+1}']
                
                try:
                    button = tk.Button(
                        master=root,
                        text=button_data['name'],
                        font=Font(family='Calibri', size=11, weight='bold'),
                        relief=tk.SOLID,
                        borderwidth=1,
                        bg=button_data['bg_color'],
                        fg=button_data['fg_color']
                    )
                except _tkinter.TclError as e:
                    message = f"Обнаружен недопустимый параметр для кнопки.\n\n{e}"
                    Dialog(self.lp).show_error(message)  
                
                button.bind(
                    '<Button-1>', 
                    lambda e, 
                        button=button,
                        data=button_data,
                        credentials=credentials: 
                            self._start_action(e, button, data, credentials, timeout)
                )
                
                button.bind(
                    '<Return>', 
                    lambda e, 
                        button=button,
                        data=button_data,
                        credentials=credentials: 
                            self._start_action(e, button, data, credentials, timeout)
                )
                    
                button.place(
                    x=positions[i][j][0],
                    y=positions[i][j][1],
                    width=positions[i][j][2],
                    height=positions[i][j][3]
                )
                
        self.lp.log(self.lp.INFO, self.lp.SHOW_BUTTONS_SUCC_MESS_ID)
                
    def _start_action(
        self, 
        event, 
        button: tk.Button, 
        b_data: dict,
        s_data: dict,
        timeout: float
    ):
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
        
        threading.Thread(
            target=self._open_directory,
            args=(button_dir, button, button_name, s_data, timeout)
        ).start()
        
        button.config(
            relief=tk.SOLID,
            borderwidth=1,
            bg=b_data['bg_color'],
            fg=b_data['fg_color']
        )
    
    def _open_directory(
        self, 
        dir: str, 
        btn: tk.Button, 
        name: str,
        creds: dict,
        timeout: float
    ):
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
        
        self.lp.log(self.lp.INFO, self.lp.OPEN_DIR_MESS_ID, (dir,))
        
        if platform.system() == 'Windows':
            try:
                network_device_name = self._get_network_device_name(dir)
                network_device_ip = self._get_network_device_ip(network_device_name)
                if network_device_name:
                    map_cmd = f'net use "\\\\{network_device_ip}" /user:"{creds["username"]}" "{creds["password"]}"'
                    map_cmd_res = self._run_command(
                        cmd=map_cmd,
                        timeout=timeout,
                        hide_cmd_window=True
                    )
                    
                    if map_cmd_res.returncode == 0:
                        self.lp.log(self.lp.INFO, self.lp.RUN_CMD_SUCC_MESS_ID, (map_cmd,))
                        
                        dir_cmd = dir.replace(network_device_name, network_device_ip)
                        self._define_dir_type(
                            cmd=dir_cmd,
                            timeout=timeout
                        )
                        
                        del_cmd = f'net use "\\\\{network_device_ip}" /delete /yes'
                        del_cmd_res = self._run_command(
                            cmd=del_cmd,
                            timeout=timeout,
                            hide_cmd_window=True
                        )
                        
                        if del_cmd_res.returncode == 0:
                            self.lp.log(self.lp.INFO, self.lp.RUN_CMD_SUCC_MESS_ID, (del_cmd,))
                        
                        else:
                            self.lp.log(self.lp.ERR, self.lp.RUN_CMD_FAIL_MESS_ID, (del_cmd,))
                            
                            self._show_error(command_result=del_cmd_res)
                            
                    else:
                        self.lp.log(self.lp.ERR, self.lp.RUN_CMD_FAIL_MESS_ID, (map_cmd,))
                        
                        self._show_error(command_result=map_cmd_res)  
                        
                else:
                    self._define_dir_type(
                        cmd=dir,
                        timeout=timeout
                    )
                    
            except subprocess.CalledProcessError as e:
                self._show_error(command_result=e)
            except subprocess.TimeoutExpired as e:
                message = f'Превышено время ожидания ответа в {timeout} секунд.'
                Dialog(self.lp).show_error(message)
            except FileNotFoundError as e:
                message = 'Не удается найти указанный файл или папку.'
                self._show_error(error=e, message=message)
            except PermissionError:
                message = 'Отсутсвует разрешение на открытие указанного файла или папки.'
                self._show_error(error=e, message=message)
            except OSError as e:
                self._show_error(error=e)
        
        else:
            try:
                subprocess.run(
                    f'echo "{creds["password"]}" | sudo -S open "{dir}"'
                )
                
            except subprocess.CalledProcessError as e:
                message = f"Ошибка выполнения консольной команды.\n\n{e}"
                Dialog(self.lp).show_error(message)
            except FileNotFoundError as e:
                message = f"Не удалось открыть файл или папку. Возможно имеются проблемы с сетью либо данной директории не существует.\n\n{e}"
                Dialog(self.lp).show_error(message)
            except OSError as e:
                message = f"Ошибка в системе.\n\n{e}"
                Dialog(self.lp).show_error(message)
            except ValueError as e:
                message = f"Неверное значение.\n\n{e}"
                Dialog(self.lp).show_error(message)
            except subprocess.TimeoutExpired as e:
                message = f"Превышено время ожидания открытия файла или папки.\n\n{e}"
                Dialog(self.lp).show_error(message)
                
        btn.config(text=name)
        
    def _show_error(
        self, 
        message: str=None,
        command_result=None,
        error=None
    ):
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
                
        Dialog(self.lp).show_error(msg)
        
    def _is_file(self, path: str) -> bool:
        """Defines if the direcory is file with RegEx.
        
        Returns:
            bool (True): If the directory is a file.
            bool (False): If the direcory is a folder.
        """
        
        file_types = ['.exe', '.txt', '.json', '.csv', '.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.xlsm', '.bat', '.mp3', '.mp4', '.avi', '.wav', '.wmv', '.mkv']
        pattern = fr'\b(?:{"|".join(re.escape(file_type) for file_type in file_types)})\b'
        return bool(re.search(pattern, path))
    
    def _get_network_device_name(self, dir: str) -> Optional[Union[str, None]]:
        """Gets name of the network device (using RegEx) 
        which the user connects to.

        Args:
            dir (str): Network directory which might have the network device name.

        Returns:
            str: If it is able to extract the network device name.
            None: If not.
        """

        matches = re.match(r'\\\\([^\\]+)', dir)
        return matches.group(1) if matches else None
    
    def _get_network_device_ip(self, identifier: str=None) -> Optional[Union[str, None]]:
        """Gets IP-address of the network device
        which the user connects to.

        Args:
            identifier (str): The network device identifier. Defaults to None

        Returns:
            str: Network device IP-address.
            None: If not.
        """
        
        return socket.gethostbyname(identifier) if identifier else None
    
    def _define_dir_type(self, cmd: str, timeout: float):
        """Defines directory type to open it next.
        
        Uses different commands for opening a directory 
        which contains either a file or a folder.

        Args:
            cmd (str): The network directory.
            timeout (float): Quanity of seconds of the possibility to open the directory.
        """
        
        if self._is_file(cmd):
            file_cmd_res = self._run_command(cmd)
                          
            if file_cmd_res.returncode == 0 or file_cmd_res.returncode == 1:
                self.lp.log(self.lp.INFO, self.lp.RUN_CMD_SUCC_MESS_ID, (cmd,))
            
            else:
                self.lp.log(self.lp.ERR, self.lp.RUN_CMD_FAIL_MESS_ID, (cmd,))
                
                self._show_error(command_result=file_cmd_res)
                                
        else:
            dir_cmd_res = self._run_command(
                cmd=f'explorer "{cmd}"',
                timeout=timeout
            )
            
            if dir_cmd_res.returncode == 0 or dir_cmd_res.returncode == 1:
                self.lp.log(self.lp.INFO, self.lp.RUN_CMD_SUCC_MESS_ID, (cmd,))
                
            else:
                self.lp.log(self.lp.ERR, self.lp.RUN_CMD_FAIL_MESS_ID, (cmd,))
                
                self._show_error(command_result=dir_cmd_res)
    
    def _run_command(self, cmd: str, timeout: float=0.0, hide_cmd_window: bool=False):
        """Runs a command to open directory.

        Args:
            cmd (str): The command which the application opens directory with.
            timeout (float): Quanity of seconds of the possibility to open the directory. If timeout is 0 s, tries to open directory without any timeout. Defaults to 0.0
            hide_cmd_window (bool, optional): Defines if the CMD window must be hidden while running the command. Defaults to False.

        Returns:
            subprocess.CompletedProcess[bytes]: The metadata of completed command.
        """
        
        self.lp.log(self.lp.INFO, self.lp.RUN_CMD_MESS_ID, (cmd,))
        
        if hide_cmd_window:
            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup_info.wShowWindow = subprocess.SW_HIDE
            
            if timeout == 0.0:
                return subprocess.Popen(
                    args=cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startup_info
                )
            else:
                return subprocess.run(
                    args=cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    startupinfo=startup_info,
                    timeout=timeout
                )
            
        else:
            if timeout == 0.0:
                return subprocess.run(
                    args=cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE
                )
                
            else:
                return subprocess.run(
                    args=cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    timeout=timeout
                )