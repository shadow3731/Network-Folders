import tkinter as tk
import time, decimal

from app.frame_controller import FrameController
from cursor import Cursor
from converter import Converter
from dialog import Dialog
from performers.window_performer import WindowPerformer
from performers.menu_performer import MenuPerformer
from performers.groups_performer import GroupsPerformer
from performers.buttons_performer import ButtonsPerformer
from performers.data_performer import DataPerformer
from performers.logs_performer import LogsPerformer


class Application():
    """The class for application control.
    
    Attributes:
        cursor (Cursor): The Cursor object for placing object on the window.
        lp (LogsPerformer): The LogsPerformer object for app logging.
        fc (FrameController): The FrameController object for app windows control.
        dp (DataPerformer): The DataPerformer object for service and application data control.
        wp (WindowPerformer): The WindowPerformer object for a window control.
        mp (MenuPerformer): The MenuPerformer object for a tool menu control.
        gp (GroupsPerformer): The GroupsPerformer object for groups control.
        bp (ButtonsPerformer): The ButtonsPerformer object for buttons control.
        session_name (str): The current app session name.
    """
    
    def __init__(self, session_name: str):
        """Initializes Application instance."""
        
        self.cursor = Cursor()
        self.lp = LogsPerformer()
        self.dp = DataPerformer(self.lp)
        self.wp = WindowPerformer(self.lp)
        self.fc = FrameController(self.lp)
        self.mp = MenuPerformer(self.dp, self.wp, self.lp)
        self.gp = GroupsPerformer(self.cursor, self.lp)
        self.bp = ButtonsPerformer(self.cursor, self.dp, self.lp)
        
        self.session_name = session_name
        
    def start(self, use_local_data: bool=False):
        """Starts the application.
    
        Creates root (main) window object, hides it and gets service and application data.
        If `use_local_data` is `False` and application data was modified, 
        loads the raw application data. If there's no loaded data or this data 
        was not converted correctly, restarts the application and tries to load 
        the application data locally. If converted application data is valid, 
        saves it, extractes credentials and shows application root window. 
        
        The service data is used for only backend working of the application,
        the application one is used for both backend and frontend working.
        
        The application data is taken from a JSON-file,
        so it has only string-type values and might have unnecessary keys.
        So that this data is being converted to a suitable dictionary,
        that optimizes working of the application. After converting, 
        the application data is used for visualizing the application main window 
        and for saving network credentials. If credentials data are updatable, 
        gets credentials from the application data and rewrites them to the service data.
        
        Args:
            use_local_data (bool, optional): The flag defining if the application must use server or local application data. Defaults to False.
        """
        
        start_time = time.time()
        self.lp.log(self.lp.INFO, self.lp.APP_LAUNCH_MESS_ID, (self.session_name, self.dp.current_app_version))
        
        self.fc.create_root()
        self.fc.root.iconify()
        self.fc.root.protocol('WM_DELETE_WINDOW', self._on_closing)
    
        self.dp.load_service_data()
        s_data = self.dp.service_data
        
        if use_local_data is False and self.dp.check_file_modified(s_data[self.dp.a_data_key]) is True:    
            raw_data = self.dp.load_application_data_from_server(s_data[self.dp.a_data_key])
            if not raw_data:
                self.restart(True)
            else:
                formatted_data = Converter(self.lp).return_valid_dictionary(raw_data)
                    
                if not formatted_data:
                    self.restart(True)
                else:
                    self.dp.save_appearance_data(
                        savable_data=formatted_data
                    )
                        
                    self._import_credentials(
                        s_data=s_data,
                        a_data=formatted_data
                    )
                        
                    self._show(formatted_data, start_time)
                    
        else:
            raw_data = self.dp.load_application_data_locally()
            formatted_data = Converter(self.lp).return_valid_dictionary(
                raw_data=raw_data,
                return_null=False
            )
                 
            self._show(formatted_data, start_time)
            
    def restart(self, use_local_data: bool=False):
        """Restarts this application by destroying all the elements.

        Args:
            use_local_data (bool, optional): The flag defining if the application must use server or local application data. Defaults to False.
        """
        self.lp.log(self.lp.INFO, self.lp.RESTART_APP_MESS_ID)
        
        self.fc.destroy_root()
        self.start(use_local_data)
        
    def _show(self, a_data: dict, start_time: float):
        """Starts the sequence of operations to show all application elements.
        
        Firstly shows tool menu bar, then creates field for displaying
        groups and buttons with ceratain parameters.
        If there is the application data, set initial Cursor values,
        calculates positions of buttons and groups and displays them 
        (if they exists). After this configures main window parameters 
        and creates a scroll bar for scrolling the window
        if there are too much buttons. Then shows the main window to a user.
        
        Args:
            a_data (dict): The application data.
        """
        
        self.lp.log(self.lp.INFO, self.lp.SHOW_ROOT_PREPARE_MESS_ID)
        
        self.fc.root.deiconify()
        
        self.mp.show_menu(self.fc.root)
        
        self.lp.log(self.lp.INFO, self.lp.PREPARE_ROOT_BG_MESS_ID)
        
        canvas = tk.Canvas(master=self.fc.root)
        canvas.place(x=0, y=-5, relwidth=1, relheight=1)
        
        frame = tk.Frame(
            master=canvas, 
            width=canvas.winfo_screenwidth(),
            height=canvas.winfo_screenheight()
        )
        
        self.wp.bind_scrolling(canvas)
        
        root_elements = {
            'root': self.fc.root,
            'canvas': canvas,
            'frame': frame
        }
        
        if a_data and len(a_data) > 0:
            if self._set_cursor_values(a_data):
                buttons_pos = self.bp.configure_buttons(a_data)
            
                if buttons_pos and len(buttons_pos) > 0:
                    if self._set_cursor_values(a_data):
                        groups_pos = self.gp.configure_groups(buttons_pos)
                    
                        self.gp.show_groups(
                            data=a_data, 
                            positions=groups_pos,
                            root=frame
                        )
                        self.bp.show_buttons(
                            data=a_data, 
                            positions=buttons_pos,
                            root=frame
                        )
                    
                        self.wp.show_main_window(
                            roots=root_elements, 
                            data=a_data, 
                            groups_pos=groups_pos
                        )
                    
                else:
                    self.wp.show_main_window(roots=root_elements, data=a_data)
            
        else:
            self.wp.show_main_window(roots=root_elements)
        
        frame.update_idletasks()
        
        canvas.config(scrollregion=(0, 0, frame.winfo_reqwidth(), frame.winfo_reqheight()))
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)
        
        scrollbar = tk.Scrollbar(
            master=self.fc.root, 
            width=self.cursor.right_padding+2,
            command=canvas.yview
        )
        scrollbar.place(relx=1, rely=0, relheight=1, anchor=tk.NE)
        
        canvas.config(yscrollcommand=scrollbar.set)
        
        self.lp.log(self.lp.INFO, self.lp.SHOW_ROOT_MESS_ID)
        self._log_about_time_delta(start_time)
        
        self.fc.root.mainloop()
        
    def _set_cursor_values(self, data: dict) -> bool:
        """Sets certain values for Cursor.
        
        The values are taken from the application data.
        If there is any invalid value, shows 'askerror' window 
        with error description.
        
        Args:
            data (dict): The application data.
            
        Returns:
            bool (True): If all data are correctly set.
            bool (False): If not.
        """
        
        self.lp.log(self.lp.INFO, self.lp.SET_CURS_VALS_MESS_ID)
        
        try:
            self.cursor.x = data['window']['padding']
            self.cursor.y = data['window']['padding']
            self.cursor.width = data['window']['button_width']
            self.cursor.height = data['window']['button_height']
            self.cursor.padding = data['window']['padding']
            self.cursor.right_padding = data['window']['r_padding']
            self.cursor.screen_width = data['window']['width']
            
            return True
        
        except ValueError as e:
            message = f'Неправильные значения размеров окна. Проверьте файл визуализации.\n\n{e}'
            Dialog(self.lp).show_error(message)
            
            return False
        
    def _import_credentials(self, s_data: dict, a_data: dict):
        """Imports network credentials to the service data 
        if the value of a specific parameter in this data allows it.

        Args:
            s_data (dict): The service data.
            a_data (dict): The application data.
        """
        
        self.lp.log(self.lp.INFO, self.lp.IMPORT_CREDS_FROM_A_DATA_MESS_ID)
        
        if s_data[self.dp.creds_import_mode_key] == 'True':
            if a_data.get('credentials'):
                s_data[self.dp.username_cred_key] = a_data['credentials']['username']
                s_data[self.dp.password_cred_key] = a_data['credentials']['password']
                
                self.lp.log(self.lp.INFO, self.lp.EDIT_S_DATA_MESS_ID, (self.dp.username_cred_key, s_data[self.dp.username_cred_key],))
                self.lp.log(self.lp.INFO, self.lp.EDIT_S_DATA_MESS_ID, (self.dp.password_cred_key, s_data[self.dp.password_cred_key],))

                self.dp.save_service_data(s_data)
                
    def _log_about_time_delta(self, start_time: float):
        """Logs about app lauch duration.
        
        Calculates the difference in time 
        between app launching and showing ready root window 
        and logs about that. If the time is more than 
        the certain one logs about that as well.

        Args:
            start_time (float): The timestamp of app launching.
        """
        
        time_delta = float(decimal.Decimal(str(time.time() - start_time)).quantize(decimal.Decimal('0.000'), rounding=decimal.ROUND_DOWN))
        
        self.lp.log(
            level=self.lp.INFO, 
            message_id=self.lp.TIME_LAUNCH_MESS_ID, 
            vars=(time_delta,)
        )
        
        optimal_time = 8
        if time_delta >= optimal_time:
            self.lp.log(
                level=self.lp.WARN, 
                message_id=self.lp.WARN_TIME_LAUNCH_MESS_ID, 
                vars=(optimal_time,)
            )
            
    def _on_closing(self):
        """Handels app closing event.
        
        Destroyes the app root window."""
        
        self.fc.destroy_root()
        
        self.lp.log(self.lp.INFO, self.lp.APP_CLOSED_MESS_ID, (self.session_name,))