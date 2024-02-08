import sys, os, threading
import tkinter as tk

from dialog import Dialog
from performers.logs_performer import LogsPerformer


class WindowPerformer():
    """The class for a window handling.
    
    Attributes:
        canvas (tk.Canvas): The Canvas element where all the visual data of the main window are displayed.
        lp (LogsPerformer): The LogsPerformer object for app logging.
    """
    
    def __init__(self, lp: LogsPerformer):
        """Initializes WindowPerformer instance."""
        
        self.canvas: tk.Canvas = None
        self.lp = lp
    
    def show_main_window(self, roots: dict, data: dict=None, groups_pos: list=None):
        """Shows main window.
        
        Sets title, icon, screen size options to the window.
        
        Gets values of width and height of the window from 
        the application data. If there are no such values, 
        sets the default ones.

        Args:
            roots (dict): Roots elements of the main window.
            data (dict, optional): The application data. Defaults to None.
            groups_pos (list, optional): The positions of the Groups. Defaults to None.
        """
        
        self.lp.log(self.lp.INFO, self.lp.CONFIG_ROOT_MESS_ID)
        
        roots['root'].title(data['app_name'])
        roots['root'].iconbitmap(self.get_content_path('icon.ico'))
        roots['root'].resizable(width=False, height=False)
        
        window_width = 500
        window_height = 0
        widgets_height = 0
        
        try:
            window_width = data['window']['width']
                        
        except ValueError as e:
            self.lp.log(self.lp.ERR, self.lp.CONFIG_ROOT_WIDTH_ERR_MESS_ID, (window_width,))
            
            message = f'Неправильные значения размеров окна. Проверьте файл визуализации.\n\n{e}'
            dialog = Dialog(self.lp)
            threading.Thread(
                target=dialog.show_error,
                args=(message,)
            ).start()
                
            window_width = 680
        
        if groups_pos and len(groups_pos) > 0:
            window_height = groups_pos[-1][1] + groups_pos[-1][-1]
            widgets_height = window_height
                
            if window_height > 515:
                window_height = 515
                
        self._congigure_roots(roots, widgets_height)
            
        self.center_window(
            root=roots['root'],
            width=window_width,
            height=window_height
        )
        
        self.lp.log(self.lp.INFO, self.lp.CONFIG_ROOT_SUCC_MESS_ID)
        
    def center_window(self, root: tk.Tk, width: int, height: int):
        """Places the window at the center of the root element.
        
        Gets screen width and height of the root element, 
        calculates its center point and places this window 
        at the center of the root.
        
        Args:
            root (tk.Tk): The root element of tkinter.
            width (int): Custom width of the window.
            height (int): Custom height of the window.
        """
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        x_offset = (screen_width - width) // 2
        y_offset = (screen_height - height) // 2
        
        root.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
        
    def configure_window(self, window: tk.Tk):
        """Sets some configurations to the window.
        
        Sets if the window can be resizable, an icon, 
        and if the window has tool buttons at the top right corner.

        Args:
            window (tk.Tk): The window element of tkinter.
        """
        
        window.resizable(width=False, height=False)
        window.iconbitmap('')
        window.attributes('-toolwindow', 1)
        
    def bind_scrolling(self, canvas: tk.Canvas=None):
        """Binds scrollig for a Canvas element.
        
        Also saves the Canvas element inside of this class, 
        if it has not been saved before.
        
        Args:
            canvas (tk.Canvas): The Canvas element where all the visual data of the main window are displayed."""
        
        if self.canvas == None:
            self.canvas = canvas
        
        self.canvas.bind_all(
            '<MouseWheel>', 
            lambda e, 
                canvas=self.canvas: 
                    self._on_mousewheel(e, canvas)
        )
        
    def unbind_scrolling(self):
        """Unbinds scrolling for a Canvas element."""
        
        self.canvas.unbind_all('<MouseWheel>')
        
    def get_content_path(self, rel_path: str) -> str:
        """Gets the directory of the application icon.
        
        Searches the icon inside of Temp folder, 
        where the application was extracted. If there is no 
        such a folder, searches it inside of the same directory 
        as the executable file.
        
        Args:
            rel_path (str): The relative path of the icon.
            
        Returns:
            str: The directory of the icon.
        """
        
        try:
            base_path = f'{sys._MEIPASS}\\network_folders_py\\'
        except Exception:
            base_path = os.path.abspath('.')
            
        return os.path.join(base_path, rel_path)
        
    def _on_mousewheel(self, event, canvas: tk.Canvas):
        """Listens to the scroll event.
        
        Displays that part of the window, where a user scrolled to.
        
        Args:
            canvas (tk.Canvas): Canvas object of tkinter. Actually the object containing all the visible objects.
        """
        canvas.yview_scroll(-1*(event.delta // 120), 'units')
        
    def _congigure_roots(self, roots: dict, height: int):
        """Configures some attributes of root elements of the main window.
        
        Args:
            roots (dict): The roots elements of the main window.
            height (int): Custom height of the root elements.
        """
        
        roots['frame'].config(height=height)
        roots['canvas'].config(height=height)