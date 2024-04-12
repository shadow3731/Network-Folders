import tkinter as tk

from performers.expanded_tkinter import ExpandedTopLevel
from dialog import Dialog

class MenuPerformer():
    """The class for toolbar menu handling.
    
    Attributes:
        menu (optional): The toolbar menu object of tkinter.
        dp (DataPerformer): The DataPerformer object for handling the data.
        wp (WindowPerformer): The WindowPerformer object for a window control.
        lp (LogsPerformer): The LogsPerformer object for app logging.
    """
    
    
    def __init__(self, canvas, dp, lp=None):
        """Initializes MenuPerformer instance."""
        
        self.menu = None
        
        self.canvas = canvas
        self.dp = dp
        self.lp = lp
        
    
    def show_menu(self, root):
        """Shows the toolbar menu.

        Args:
            root (tk.Tk): The root window where the toolbar menu is displayed.
        """
        
        self.lp.log(self.lp.INFO, self.lp.SHOW_MENU_MESS_ID)
        
        self.menu = tk.Menu(master=root, tearoff=0)
        root.config(menu=self.menu)
        
        self.menu.add_cascade(
            label='Опции', 
            menu=self._show_options_menu(root),
        )
        self.menu.add_cascade(
            label='Помощь', 
            menu=self._show_help_menu(root),
        )
        
        self.lp.log(self.lp.INFO, self.lp.SHOW_MENU_SUCC_MESS_ID)
        
    def _show_options_menu(self, root):
        """Shows inner menu of the main toolbar menu.

        Args:
            root (tk.Tk): The main toolbar menu element.

        Returns:
            tk.Menu: Inner toolbar menu element.
        """
        
        options_menu = tk.Menu(master=root, tearoff=0)
        options_menu.add_cascade(
            label='Файл конфигурации',
            menu=self._show_config_file_menu(options_menu),
        )
        options_menu.add_cascade(
            label='Сетевые учетные данные',
            menu=self._show_cred_settings_menu(options_menu),
        )
        
        return options_menu
    
    def _show_config_file_menu(self, master_menu):
        """Shows specififc options of certain inner menu element.
        
        Perfoms operations for opening built-in dialog window 
        to find the file with application data.

        Args:
            master_menu (tk.Menu): The inner menu element.

        Returns:
            tk.Menu: Options of the inner menu element.
        """
        
        config_file_menu = tk.Menu(master=master_menu, tearoff=0)
        config_file_menu.add_command(
            label='Импортировать', 
            command=lambda: self._import_file(master_menu),
        )
        
        return config_file_menu
    
    def _show_cred_settings_menu(self, master_menu):
        """Shows specififc options of certain inner menu element.
        
        Perfoms operations for opening custom dialog window 
        to print and save network credentials.

        Args:
            master_menu (tk.Menu): The inner menu element.

        Returns:
            tk.Menu: Options of the inner menu element.
        """
        
        config_file_menu = tk.Menu(master=master_menu, tearoff=0)
        config_file_menu.add_command(
            label='Изменить', 
            command=lambda: self._set_network_credentials(master_menu),
        )
        
        return config_file_menu
    
    def _set_network_credentials(self, root):
        """Sets the network credentials.
        
        Creates Toplevel dialog window with some elements 
        to write and save the network credentials.
        
        If the credentials have been saved before, shows these data.

        Args:
            root (tk.Menu): The toolbar menu element of tkinter.
        """
        
        self.lp.log(self.lp.INFO, self.lp.OPEN_CREDS_MODAL_MESS_ID)
        
        modal_window = ExpandedTopLevel(root)
        modal_window.configure(
            width=400, 
            height=120, 
            title='Изменить сетевые учетные данные',
            toolwindow=True,
        )
        modal_window.grab_set()
        
        s_data = self.dp.service_data
        
        label_username = tk.Label(
            master=modal_window,
            text='Имя пользователя',
        )
        label_username.pack(anchor=tk.W, padx=5, pady=(5, 0))
        
        entry_username = tk.Entry(
            master=modal_window,
            width=modal_window.winfo_screenwidth(),
        )
        entry_username.insert(0, s_data[self.dp.username_cred_key])
        entry_username.pack(anchor=tk.CENTER, padx=5)
        
        label_password = tk.Label(
            master=modal_window,
            text='Пароль',
        )
        label_password.pack(anchor=tk.W, padx=5)
        
        entry_password = tk.Entry(
            master=modal_window,
            width=modal_window.winfo_screenwidth(),
            show='*',
        )
        entry_password.insert(0, s_data[self.dp.password_cred_key])
        entry_password.pack(anchor=tk.CENTER, padx=5, pady=(0, 5))
        
        button = tk.Button(
            master=modal_window, 
            text='Изменить',
            width=12,
            command=lambda: self._save_network_credentials(
                event=None,
                window=modal_window,
                user=entry_username.get(),
                passw=entry_password.get()
            )
        )
        button.pack(side=tk.RIGHT, padx=5)
        button.bind(
                '<Return>', 
                lambda e, 
                window=modal_window, 
                user=entry_username.get(),
                passw=entry_password.get(): 
                    self._save_network_credentials(e, window, user, passw)
            )
        
        modal_window.wait_window()
        
    def _save_network_credentials(self, event, window, user, passw):
        """Saves the network credentials.
        
        Creates a dictionary and saves them as a part 
        of the service data.

        Args:
            window (tk.Toplevel): The dialog window of credentials.
            user (str): The username of credentials.
            passw (str): The password of credentials.
        """
        
        # self.lp.log(self.lp.INFO, self.lp.EDIT_S_DATA_MESS_ID, (self.dp.creds_import_mode_key, s_data[self.dp.username_cred_key],))
        # self.lp.log(self.lp.INFO, self.lp.EDIT_S_DATA_MESS_ID, (self.dp.username_cred_key, s_data[self.dp.username_cred_key],))
        # self.lp.log(self.lp.INFO, self.lp.EDIT_S_DATA_MESS_ID, (self.dp.password_cred_key, s_data[self.dp.password_cred_key],))
                
        self.dp.save_credentials_import_mode('False')
        self.dp.save_credentials(user, passw)
        
        window.destroy()
        
        self.lp.log(self.lp.INFO, self.lp.CLOSE_CREDS_MODAL_MESS_ID)
            
    def _import_file(self, root):
        """Opens the built-in filedialog to find the file 
        with data. If user found it, the application saves it."""
        
        self.lp.log(self.lp.INFO, self.lp.OPEN_DIALOG_LOAD_A_DATA_MESS_ID)
        
        title = 'Открыть файл конфигурации'
        filedir = Dialog(self.lp).open_file_dialog(title, root)
        
        if filedir:
            self.lp.log(self.lp.INFO, self.lp.GOT_A_DATA_FILEDIR_MESS_ID, (dir,))
            
            from threading import Thread
            Thread(target=self._save_new_app_data, args=(root, filedir,)).start()
        
        self.lp.log(self.lp.INFO, self.lp.CLOSE_DIALOG_LOAD_A_DATA_MESS_ID)
            
    def _check_new_app_data(self, filedir, root):
        """Saves filedirectory of the application data 
        as a part of the service data.
        
        If the service data exists, performs this action.

        Args:
            dir (str): The directory of the file with the application data.
        """
        
        if filedir:
            self.lp.log(self.lp.INFO, self.lp.GOT_A_DATA_FILEDIR_MESS_ID, (dir,))

            #     self.lp.log(self.lp.INFO, self.lp.EDIT_S_DATA_MESS_ID, (self.dp.a_serv_data_key, s_data[self.dp.a_serv_data_key],))
            #     self.lp.log(self.lp.INFO, self.lp.EDIT_S_DATA_MESS_ID, (self.dp.a_serv_data_mtime_key, s_data[self.dp.a_serv_data_mtime_key],))
            #     self.lp.log(self.lp.INFO, self.lp.EDIT_S_DATA_MESS_ID, (self.dp.creds_import_mode_key, s_data[self.dp.creds_import_mode_key],))
            
            from threading import Thread
            Thread(target=self._save_new_app_data, args=(root, filedir,)).start()
                    
    def _save_new_app_data(self, root, filedir):
        from performers.network_performer import NetworkPerformer
        self.dp.server_device_name = NetworkPerformer(self.lp).get_network_device_identifier(filedir)
        serv_app_data = self.dp.load_application_data_from_server(filedir)
            
        if serv_app_data:
            from validator import Validator
            validatable = Validator(self.lp).check_app_data(root, serv_app_data)
                
            if validatable:
                self.dp.save_server_application_data_directory(filedir)
                self.dp.save_modification_time()
                self.dp.save_credentials_import_mode('True')
                self.dp.save_application_data(serv_app_data, True)
                
    def _show_help_menu(self, root):
        """Shows inner menu of the main toolbar menu.

        Args:
            root (tk.Tk): The main toolbar menu element.

        Returns:
            tk.Menu: Inner toolbar menu element.
        """
        
        help_menu = tk.Menu(master=root, tearoff=0)
        help_menu.add_command(
            label='Справка',
            command=lambda: self._show_help(
                root=help_menu,
                title='Справка',
                filepath=self.dp.help_file_dir
            )
        )
        help_menu.add_command(
            label='Описание обновлений',
            command=lambda: self._show_help(
                root=help_menu,
                title='Описание обновлений',
                filepath=self.dp.updates_file_dir
            )
        )
        help_menu.add_command(
            label='Открыть логи',
            command=lambda: self._show_log(root),
        )
        
        return help_menu
    
    def _show_help(self, root, title, filepath):
        """Shows the help window.
        
        Creates Toplevel dialog window with some elements 
        for reading instructions about the application.
        
        Instructions are contained in a text file.
        
        Disables Scrollbar for the main window because of 
        mutual scrolling. After closing the help window, 
        enables Scrollbar for the main one.

        Args:
            root (tk.Menu): The toolbar menu element of tkinter.
            title (str): The title of a dilog window.
            filepath (str): The path to the cerain help file.
        """
        
        self.lp.log(self.lp.INFO, self.lp.OPEN_HELP_DIALOG_MESS_ID, (title,))
        
        modal_window = ExpandedTopLevel(root)
        modal_window.configure(
            width=400, 
            height=530, 
            title=title, 
            toolwindow=True
        )
        self.canvas.unbind_scrolling()

        modal_window.grab_set()
        modal_window.protocol(
            'WM_DELETE_WINDOW', 
            lambda: modal_window.on_close(self.canvas, self.lp)
        )
        
        content = self.dp.load_content_file(filepath)
            
        upper_frame = tk.Frame(master=modal_window)
        upper_frame.pack(
            side=tk.TOP,
            fill=tk.X
        )
        
        text_field = tk.Text(
            master=upper_frame,
            wrap=tk.NONE,
            width=54,
            height=28,
            bd=0,
            highlightthickness=0,
            font=('Times New Roman', 11),
            bg=modal_window.cget('bg')
        )
        text_field.insert(tk.END, content)
        text_field.pack(side=tk.LEFT)
        
        scrollbar = tk.Scrollbar(
            master=upper_frame,
            command=text_field.yview
        )
        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )
        
        text_field.config(
            state=tk.DISABLED, 
            cursor='',
            yscrollcommand=scrollbar.set
        )
        
        close_button = tk.Button(
            master=modal_window,
            width=10,
            text='Закрыть',
            command=lambda: modal_window.on_close(self.canvas, self.lp)
        )
        close_button.pack(side=tk.RIGHT, padx=5)
        
        modal_window.wait_window()
        
    def _show_log(self, root):
        from performers.network_performer import NetworkPerformer
        filepath = f'{self.dp.get_base_path()}\\{self.dp.log_file_dir}'
        command = NetworkPerformer(self.lp).execute('win open file', file=filepath)
        
        if command.returncode == -1:
            message = 'Файл не найден.'
            Dialog().show_error(message, root)