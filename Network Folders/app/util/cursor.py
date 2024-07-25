class Cursor():
    """The class for calculating objects placement on the window.
    
    Attributes:
        x (int): X-coordinate of the object on the screen.
        y (int): X-coordinate of the object on the screen.
        width (int): The width of the object on the screen.
        height (int): The height of the object on the screen.
        padding (int): The distance between the total object area and the real one.
        right_padding (int): The distance between the last object in the row and right edge of the window.
        scr_width (int): The window width.
    """
    
    def __init__(self, init_x=0, init_y=0, width=0, height=0, padding=0, right_padding=0, scr_width = 0):
        """Initializes Cursor instance."""
        
        self.x = init_x
        self.y = init_y
        self.width = width
        self.height = height
        self.padding = padding
        self.right_padding = right_padding
        self.screen_width = scr_width
        
        self.default_values = {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'padding': self.padding,
            'right_padding': self.right_padding,
            'screen_width': self.screen_width,
        }
        
    def load_deafault_values(self):
        self.x = self.default_values['x']
        self.y = self.default_values['y']
        self.width = self.default_values['width']
        self.height = self.default_values['height']
        self.padding = self.default_values['padding']
        self.right_padding = self.default_values['right_padding']
        self.screen_width = self.default_values['screen_width']
        
    def save_default_values(self, init_x=0, init_y=0, width=0, height=0, padding=0, right_padding=0, scr_width = 0):
        self.default_values = {
            'x': init_x,
            'y': init_y,
            'width': width,
            'height': height,
            'padding': padding,
            'right_padding': right_padding,
            'screen_width': scr_width,
        }
    
    def place_button(self, button):
        """Calculates a button positions.
        
        Positions of the button contain X- and Y-coordinate,
        width and height. These values are saved in a tuple,
        which is returned after calculation.
        
        If X-coordinate of the Cursor and width of the current button
        are out of the width of the window, X- and Y-coordinate
        of the Cursor transfer to new position.
        
        After calulating a button positions, Cursor changes 
        its X-coordinate.
        
        Args:
            button (dict): The application data of a button.
            
        Returns:
            tuple: Positions of a button on the window.
        """
        
        if self.x + button['size']*self.width > self.screen_width - self.padding - self.right_padding:
            self.x = self.padding
            self.y += self.height - self.padding
            
        button_positions = (
            self.x + self.padding,
            self.y + 4*self.padding,
            button['size']*self.width + (button['size']-1)*self.padding,
            self.height - 2*self.padding
        )
        
        
        # if self.x + button['size']*self.width > self.screen_width - self.padding - self.right_padding:
        #     self.x = self.padding
        #     self.y += self.height - self.padding
            
        # button_positions = (
        #     self.x + self.padding,
        #     self.y + 4*self.padding,
        #     button['size']*self.width + (button['size']-1)*self.padding,
        #     self.height - 2*self.padding
        # )
        
        self.x += button['size']*self.width + button['size']*self.padding
            
        return button_positions
    
    def place_group(self, lower_y):
        """Calculates a group positions.
        
        Positions of the group contain X- and Y-coordinate,
        width and height. These values are saved in a tuple,
        which is returned after calculation.
        
        After calulating a group positions, Cursor changes 
        its Y-coordinate.
        
        Args:
            lower_y (int): The lower Y-coordinate of the last button in this group.
            
        Returns:
            tuple: Positions of a group on the window.
        """
        
        # group_positions: tuple = (
        #     self.x,
        #     self.y,
        #     self.screen_width - 2*self.padding - self.right_padding,
        #     lower_y + 2*self.padding - self.y
        # )
        
        # self.y = lower_y + self.padding/2
        
        
        
        group_positions = (
            self.x,
            self.y,
            self.screen_width - 2*self.padding - self.right_padding,
            lower_y + self.padding - self.y
        )
        
        self.y = lower_y + self.padding
        
        return group_positions
    
    def move_to_new_group(self):
        """Moves Cursor to new position."""
       
        # self.x = self.padding
        # self.y += self.height + self.padding/2 + 20
       
        
        self.x = self.padding
        self.y += self.height + 3*self.padding