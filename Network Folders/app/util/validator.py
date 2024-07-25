class Validator():
    """The class for converting the appearance data taken from a file to the correct dictionary.
    
    Attributes:
        lp (LogsPerformer): The LogsPerformer object for app logging.
    """
    
    def __init__(self, lp=None):
        """Initializes Application instance."""
        
        self.lp = lp
    
    def validate_app_data(self, raw_data, root): 
        """Returns correct dictionary of the application data.
        
        Creates new application data based on the one taken from a file.
        This new application data is a dictionary which has
        necessary keys and values with right types.
        
        If there is no any necessary key in the raw application data,
        puts a default value to the necessary key in the valid application data.
        
        Args:
            raw_data (dict): The raw application data taken from a file.
            return_none (bool, optional): Defines wether return None or make a dictionary with default values. Defaults to True.
            
        Returns:
            dict: The valid application data with correct values and its types.
        """
        
        self.lp.log(self.lp.INFO, self.lp.VALID_A_DATA_MESS_ID)
        
        error_stack = []
                
        if not raw_data:
            raw_data = {}
        
        data = {}
        
        data['app_name'] = 'Network Folders' if not raw_data.get('app_name') else raw_data['app_name']
        
        data['credentials'] = {} if not raw_data.get('credentials') else raw_data['credentials']
        if raw_data.get('credentials'):
            data['credentials']['username'] = '' if not raw_data['credentials'].get('username') else raw_data['credentials']['username']
            data['credentials']['password'] = '' if not raw_data['credentials'].get('password') else raw_data['credentials']['password']
        
        else:
            self._put_defaults(
                data=data, 
                flag='credentials'
            )
        
        data['window'] = {} if not raw_data.get('window') else raw_data['window']
        if raw_data.get('window'):
            try:
                data['window']['width'] = 695 if not raw_data['window'].get('width') else int(raw_data['window']['width'])
                data['window']['padding'] = 5 if not raw_data['window'].get('padding') else int(raw_data['window']['padding'])
                data['window']['r_padding'] = 15 if not raw_data['window'].get('r_padding') else int(raw_data['window']['r_padding'])
                data['window']['button_width'] = 90 if not raw_data['window'].get('button_width') else int(raw_data['window']['button_width'])
                data['window']['button_height'] = 40 if not raw_data['window'].get('button_height') else int(raw_data['window']['button_height'])
            
            except ValueError as e:
                error_stack.append(e)
                self._put_defaults(
                        data=data, 
                        flag='window'
                    )
        
        else:
            self._put_defaults(
                data=data, 
                flag='window'
            )
        
        try:
            data['dir_open_timeout'] = 10.0 if not raw_data.get('dir_open_timeout') else float(raw_data['dir_open_timeout'])
            
        except ValueError as e:
            error_stack.append(e)
            self._put_defaults(
                    data=data, 
                    flag='dir_open_timeout'
                )
        
        if raw_data.get('groups'):
            data['groups'] = {}
            
            i = 1
            while True:
                if raw_data['groups'].get(f'group{i}'):
                    data['groups'][f'group{i}'] = {}
                    data['groups'][f'group{i}']['name'] = f'Group {i}' if not raw_data['groups'][f'group{i}'].get('name') else raw_data['groups'][f'group{i}']['name']
                    data['groups'][f'group{i}']['buttons'] = {}
                    
                    j = 1
                    while True:
                        if raw_data['groups'][f'group{i}']['buttons'].get(f'button{j}'):
                            data['groups'][f'group{i}']['buttons'][f'button{j}'] = {}
                            data['groups'][f'group{i}']['buttons'][f'button{j}']['name'] = f'Button {j}' if not raw_data['groups'][f'group{i}']['buttons'][f'button{j}'].get('name') else raw_data['groups'][f'group{i}']['buttons'][f'button{j}']['name']
                            data['groups'][f'group{i}']['buttons'][f'button{j}']['path'] = '' if not raw_data['groups'][f'group{i}']['buttons'][f'button{j}'].get('path') else raw_data['groups'][f'group{i}']['buttons'][f'button{j}']['path']
                            
                            try:
                                data['groups'][f'group{i}']['buttons'][f'button{j}']['size'] = 1 if not raw_data['groups'][f'group{i}']['buttons'][f'button{j}'].get('size') else int(raw_data['groups'][f'group{i}']['buttons'][f'button{j}']['size'])
                            
                            except ValueError as e:
                                error_stack.append(e)
                                data['groups'][f'group{i}']['buttons'][f'button{j}']['size'] = 1
                            
                            data['groups'][f'group{i}']['buttons'][f'button{j}']['bg_color'] = 'white' if not raw_data['groups'][f'group{i}']['buttons'][f'button{j}'].get('bg_color') else raw_data['groups'][f'group{i}']['buttons'][f'button{j}']['bg_color']
                            data['groups'][f'group{i}']['buttons'][f'button{j}']['fg_color'] = 'black' if not raw_data['groups'][f'group{i}']['buttons'][f'button{j}'].get('fg_color') else raw_data['groups'][f'group{i}']['buttons'][f'button{j}']['fg_color']
                            
                            j += 1
                            
                        else:
                            break
                    
                    i += 1
                    
                else:
                    break
                
        if len(error_stack) > 0:
            self._redirect_error(root, error_stack)
        else:
            self.lp.log(self.lp.INFO, self.lp.VALID_A_DATA_SUCC_MESS_ID)
            
        return data
    
    def check_app_data(self, root, raw_data):
        self.lp.log(self.lp.INFO, self.lp.VALID_A_DATA_MESS_ID)
        
        error_stack = []
        
        if raw_data:       
            if raw_data.get('window'):
                keys = [
                        'width', 
                        'padding', 
                        'r_padding', 
                        'button_width', 
                        'button_height',
                ]
                
                for key in keys:
                    try:
                        if raw_data['window'].get(key):
                            int(raw_data['window'][key])
                    except ValueError as e:
                        error_stack.append(str(e))
                    
            if raw_data.get('dir_open_timeout'):
                try:
                    float(raw_data['dir_open_timeout'])
                except ValueError as e:
                    error_stack.append(str(e))
                    
            if raw_data.get('groups'):
                i = 1
                while True:
                    if raw_data['groups'].get(f'group{i}') and raw_data['groups'][f'group{i}'].get('buttons'):
                        j = 1
                        while True:
                            if raw_data['groups'][f'group{i}']['buttons'].get(f'button{j}') and raw_data['groups'][f'group{i}']['buttons'][f'button{j}'].get('size'):
                                try:
                                    int(raw_data['groups'][f'group{i}']['buttons'][f'button{j}']['size'])
                                except ValueError as e:
                                    error_stack.append(str(e))

                                j += 1
                                    
                            else:
                                break
                                    
                        i += 1
                        
                    else:
                        break
            
        else:
            error_stack.append('Файл конфигурации не может быть пустым.')
            
        if len(error_stack) > 0:
            self._redirect_error(root, error_stack)
            return False
        
        self.lp.log(self.lp.INFO, self.lp.VALID_A_DATA_SUCC_MESS_ID)
        
        return True
    
    def _redirect_error(self, root, errors):
        """Redirects error message and description to show them to the user.

        Args:
            e (ValueError): Error description.
        """
        
        from app.window.dialog import Dialog
        parts = '\n'.join(errors)
        message = f"Обнаружено недопустимое значение параметров в файле конфигурации. Будут выгружены значения из локального файла конфигурации.\n\n{parts}"
        
        self.lp.log(self.lp.ERR, self.lp.VALID_A_DATA_FAIL_MESS_ID, (message,))
        
        Dialog(self.lp).show_error(message, root)
        
    def _put_defaults(self, data, flag):
        """Puts some deafault values to the application data.

        Args:
            data (dict): The application data.
            flag (str): The group of parameters that need to set default values into.
        """
        
        self.lp.log(self.lp.WARN, self.lp.VALID_A_DATA_DEFAULT_MESS_ID)
        
        if flag == 'credentials':
            data['credentials']['username'] = ''
            data['credentials']['password'] = ''
            
        elif flag == 'window':
            data['window']['width'] = 695
            data['window']['padding'] = 5
            data['window']['r_padding'] = 15
            data['window']['button_width'] = 90
            data['window']['button_height'] = 40
        
        elif flag == 'dir_open_timeout':
            data['dir_open_timeout'] = 10.0