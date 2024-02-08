from tkinter import Tk

from performers.logs_performer import LogsPerformer


class FrameController():
    """The class for application windows control.
    
    Attributes:
        lp (LogsPerformer): The LogsPerformer object for app logging.
        root (tk.TK): the root window."""
    
    def __init__(self, lp: LogsPerformer) -> None:
        """Initializes FrameController instance."""
        
        self.lp: LogsPerformer = lp
        
        self.root: Tk = None
    
    def create_root(self):
        """Creates root window."""
        
        self.lp.log(self.lp.INFO, self.lp.CREATE_ROOT_MESS_ID)
        
        self.root = Tk()
        
        self.lp.log(self.lp.INFO, self.lp.CREATE_ROOT_SUCC_MESS_ID)
        
    def destroy_root(self):
        """Destroyes root windows and all inner elements."""
        
        self.root.destroy()
        
        self.lp.log(self.lp.INFO, self.lp.DESTROY_ROOT_SUCC_MESS_ID)