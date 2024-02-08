import tkinter as tk
from tkinter.font import Font

from cursor import Cursor
from performers.logs_performer import LogsPerformer


class GroupsPerformer():
    """The class for a Group handling.
    
    Attributes:
        cursor (Cursor): The Cursor object for placing object on the window.
        lp (LogsPerformer): The LogsPerformer object for app logging.
    """
    
    def __init__(self, cursor: Cursor, lp: LogsPerformer):
        """Initializes GroupsPerformer instance."""
        
        self.cursor = cursor
        self.lp = lp
        
    def configure_groups(self, buttons_pos: list) -> list:
        """Gets the groups positions.
        
        Creates a list of Groups with their positions 
        in the main window. Calculation of Groups positions 
        may happen only if there are list of Buttons 
        with their positions. If there are no Buttons, 
        the list of Groups positions keeps being empty.

        Args:
            buttons_pos (list): The list of Buttons positions.

        Returns:
            list: The Groups positions
        """
        
        self.lp.log(self.lp.INFO, self.lp.CONFIG_GROUPS_MESS_ID)
        
        positions: list = []
        
        for i in range(len(buttons_pos)):
            lower_y = buttons_pos[i][-1][1] + buttons_pos[i][-1][3]
            positions.append(self.cursor.place_group(lower_y))
            
        self.lp.log(self.lp.INFO, self.lp.CONFIG_GROUPS_SUCC_MESS_ID)
        
        return positions
    
    def show_groups(self, data: dict, positions: list, root: tk.Frame):
        """Shows Groups on the window.
        
        Groups are displayed only according to the sequence numbers. 
        If the sequnce is interrupted, no more Groups are displayed.

        Args:
            data (dict): The appearance data.
            positions (list): The Groups positions.
            root (tk.Frame): The root element where the Groups are displayed.
        """
        
        self.lp.log(self.lp.INFO, self.lp.SHOW_GROUPS_MESS_ID)
        
        if data:
            for i in range(len(positions)):
                group_data: dict = data['groups'][f'group{i+1}']
                
                tk.LabelFrame(
                    master=root,
                    text=group_data['name'],
                    font=Font(family='Calibri', size=11, weight='bold')
                ).place(
                    x=positions[i][0],
                    y=positions[i][1],
                    width=positions[i][2],
                    height=positions[i][3]
                )
                
            self.lp.log(self.lp.INFO, self.lp.SHOW_GROUPS_SUCC_MESS_ID)
            
        else:
            self.lp.log(self.lp.WARN, self.lp.SHOW_NO_GROUPS_MESS_ID)