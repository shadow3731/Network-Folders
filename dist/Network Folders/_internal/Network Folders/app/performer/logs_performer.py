import logging


class LogsPerformer():
    """The class for application logging.
    
    Attributes:
        INFO (int): The constant value of logs inforamtion level.
        WARN (int): The constant value of logs warning level.
        ERR (int): The constant value of logs error level.
        message_map (Dict[int, str]): The dictionary of logs messages
    """

    def __init__(self, file_dir):
        """Initializes LogsPerformer instance."""
        
        self.__file_dir = file_dir
        
        file_handler = logging.FileHandler(
            filename=self.__file_dir,
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.root.setLevel(logging.INFO)
        logging.root.addHandler(file_handler)
        
        self.INFO = logging.INFO
        self.WARN = logging.WARNING
        self.ERR = logging.ERROR
        
        (
            self.APP_LAUNCH_MESS_ID,
            self.VER_LAUNCH_MESS_ID,
            self.TIME_LAUNCH_MESS_ID,
            self.WARN_TIME_LAUNCH_MESS_ID,
            self.CHECK_UPDATER_MESS_ID,
            self.FOUND_UPDATER_MESS_ID,
            self.UPDATE_INSTALLED_MESS_ID,
            self.NO_UPDATER_MESS_ID,
            self.CHECK_NEW_VER_MESS_ID,
            self.NO_NEW_VER_MESS_ID,
            self.CHECK_RES_CODE_SUCC_MESS_ID,
            self.CHECK_RES_CODE_FAIL_MESS_ID,
            self.NEW_VER_MESS_ID,
            self.DOWNLOAD_NEW_VER_MESS_ID,
            self.DOWNLOAD_NEW_VER_RES_CODE_FAIL_MESS_ID,
            self.DOWNLOAD_NEW_VER_RES_CODE_SUCC_MESS_ID,
            self.DOWNLOAD_NEW_VER_SUCC_MESS_ID,
            self.DOWNLOAD_NEW_VER_FAIL_MESS_ID,
            self.CREATE_LOADER_MESS_ID,
            self.DESTROY_LOADER_MESS_ID,
            self.CREATE_ROOT_MESS_ID,
            self.DESTROY_ROOT_MESS_ID,
            self.LOAD_S_DATA_MESS_ID,
            self.CHECK_S_DATA_EXISTS_MESS_ID,
            self.NO_S_DATA_AND_CREATE_MESS_ID,
            self.SAVE_S_DATA_MESS_ID,
            self.SAVE_S_DATA_SUCC_MESS_ID,
            self.SAVE_S_DATA_FAIL_MESS_ID,
            self.CHECK_S_DATA_VALID_MESS_ID,
            self.S_DATA_VALID_MESS_ID,
            self.S_DATA_INVALID_AND_CREATE_MESS_ID,
            self.CHECK_SERV_NAME_MESS_ID,
            self.GOT_SERV_NAME_MESS_ID,
            self.NO_SERV_NAME_MESS_ID,
            self.LOAD_S_DATA_SUCC_MESS_ID,
            self.CREATE_LOADER_SUCC_MESS_ID,
            self.DESTROY_LOADER_SUCC_MESS_ID,
            self.CREATE_ROOT_SUCC_MESS_ID,
            self.DESTROY_ROOT_SUCC_MESS_ID,
            self.LOAD_A_DATA_FROM_SERV_MESS_ID,
            self.LOAD_A_DATA_LOCAL_MESS_ID,
            self.LOAD_A_DATA_FROM_SERV_SUCC_MESS_ID,
            self.LOAD_A_DATA_FROM_SERV_FAIL_MESS_ID,
            self.LOAD_A_DATA_TRY_LOCAL_MESS_ID,
            self.LOAD_A_DATA_LOCAL_SUCC_MESS_ID,
            self.LOAD_A_DATA_LOCAL_FAIL_MESS_ID,
            self.SAVE_A_DATA_MESS_ID,
            self.SAVE_A_DATA_SUCC_MESS_ID,
            self.SAVE_A_DATA_FAIL_MESS_ID,
            self.CHECK_A_DATA_UPDATED_MESS_ID,
            self.A_DATA_UPDATABLE_MESS_ID,
            self.A_DATA_NOT_UPDATABLE_MESS_ID,
            self.CHECK_A_DATA_UPDATED_FAIL_MESS_ID,
            self.UPDATE_A_DATA_MESS_ID,
            self.RESTART_APP_MESS_ID,
            self.IMPORT_CREDS_FROM_A_DATA_MESS_ID,
            self.VALID_A_DATA_MESS_ID,
            self.VALID_A_DATA_FAIL_MESS_ID,
            self.VALID_A_DATA_SUCC_MESS_ID,
            self.VALID_A_DATA_DEFAULT_MESS_ID,
            self.SHOW_ROOT_PREPARE_MESS_ID,
            self.SHOW_ROOT_MESS_ID,
            self.SHOW_MENU_MESS_ID,
            self.SHOW_MENU_SUCC_MESS_ID,
            self.OPEN_DIALOG_LOAD_A_DATA_MESS_ID,
            self.SHOW_INFO_DIALOG_MESS_ID,
            self.SHOW_ERR_DIALOG_MESS_ID,
            self.GOT_A_DATA_FILEDIR_MESS_ID,
            self.EDIT_S_DATA_MESS_ID,
            self.OPEN_CREDS_MODAL_MESS_ID,
            self.CLOSE_CREDS_MODAL_MESS_ID,
            self.CLOSE_DIALOG_LOAD_A_DATA_MESS_ID,
            self.OPEN_HELP_DIALOG_MESS_ID,
            self.CLOSE_HELP_DIALOG_MESS_ID,
            self.PREPARE_ROOT_BG_MESS_ID,
            self.SET_CURS_VALS_MESS_ID,
            self.CONFIG_BUTTONS_MESS_ID,
            self.CONFIG_BUTTONS_SUCC_MESS_ID,
            self.NO_CONFIG_BUTTONS_MESS_ID,
            self.CONFIG_GROUPS_MESS_ID,
            self.CONFIG_GROUPS_SUCC_MESS_ID,
            self.SHOW_GROUPS_MESS_ID,
            self.SHOW_GROUPS_SUCC_MESS_ID,
            self.SHOW_NO_GROUPS_MESS_ID,
            self.SHOW_BUTTONS_MESS_ID,
            self.SHOW_BUTTONS_SUCC_MESS_ID,
            self.PRESS_BUTTON_MESS_ID,
            self.OPEN_DIR_MESS_ID,
            self.RUN_CMD_MESS_ID,
            self.RUN_CMD_SUCC_MESS_ID,
            self.RUN_CMD_FAIL_MESS_ID,
            self.S_DATA_EXISTS_MESS_ID,
            self.CONFIG_LOADER_MESS_ID,
            self.CONFIG_LOADER_SUCC_MESS_ID,
            self.CONFIG_ROOT_MESS_ID,
            self.CONFIG_ROOT_WIDTH_ERR_MESS_ID,
            self.CONFIG_ROOT_SUCC_MESS_ID,
            self.APP_CLOSED_MESS_ID,
        ) = range(98)
        
        self.message_map = {
            self.APP_LAUNCH_MESS_ID: (
                'Application with session name: "{}" is launching...'
            ),
            self.VER_LAUNCH_MESS_ID: (
                'Application version: {}'
            ),
            self.TIME_LAUNCH_MESS_ID: (
                'Application launched. Launch duration: {} s.'
            ),
            self.WARN_TIME_LAUNCH_MESS_ID: (
                'Launch time should not be more than {} s. '
                'Please check system performance.'
            ),
            self.CHECK_UPDATER_MESS_ID: (
                'Checking for update file...'
            ),
            self.FOUND_UPDATER_MESS_ID: (
                'Update file is found: {}.'
            ),
            self.UPDATE_INSTALLED_MESS_ID: (
                'Update is installed. Application is ready to work.'
            ),
            self.NO_UPDATER_MESS_ID: (
                'Update file is not found. Application will not update.'
            ),
            self.CHECK_NEW_VER_MESS_ID: (
                'Checking for new version of application...'
            ),
            self.NO_NEW_VER_MESS_ID: (
                'No new version of application is found.'
            ),
            self.CHECK_RES_CODE_SUCC_MESS_ID: (
                'Response code of checking the new version is 200.'
            ),
            self.CHECK_RES_CODE_FAIL_MESS_ID: (
                'Response code of checking the new version is {}.'
            ),
            self.NEW_VER_MESS_ID: (
                'New version of application is found: {}.'
            ),
            self.DOWNLOAD_NEW_VER_MESS_ID: (
                'Downloading the new version of application...'
            ),
            self.DOWNLOAD_NEW_VER_RES_CODE_SUCC_MESS_ID: (
                'Response code of downloading the new version is 200.'
            ),
            self.DOWNLOAD_NEW_VER_RES_CODE_FAIL_MESS_ID: (
                'Response code of downloading the new version is {}.'
            ),
            self.DOWNLOAD_NEW_VER_SUCC_MESS_ID: (
                'New version of application is downloaded.'
            ),
            self.DOWNLOAD_NEW_VER_FAIL_MESS_ID: (
                'New version of application is not downloaded.'
            ),
            self.CREATE_LOADER_MESS_ID: (
                'Creating application loader window...'
            ),
            self.DESTROY_LOADER_MESS_ID: (
                'Destroying application loader window...'
            ),
            self.CREATE_ROOT_MESS_ID: (
                'Creating application root window...'    
            ),
            self.DESTROY_ROOT_MESS_ID: (
                'Destroying application root window...'
            ),
            self.LOAD_S_DATA_MESS_ID: (
                'Loading the service data from "{}" directory...'
            ),
            self.CHECK_S_DATA_EXISTS_MESS_ID: (
                'Checking if the service data file exists...'
            ),
            self.NO_S_DATA_AND_CREATE_MESS_ID: (
                'No service data in the "{}" directory. Application will create the new one.'
            ),
            self.SAVE_S_DATA_MESS_ID: (
                'Saving the service data in "{}" directory...'
            ),
            self.SAVE_S_DATA_SUCC_MESS_ID: (
                'The service data was saved in "{}" directory.'
            ),
            self.SAVE_S_DATA_FAIL_MESS_ID: (
                'The service data was not saved in "{}" directory.\n{}'
            ),
            self.CHECK_S_DATA_VALID_MESS_ID: (
                'Checking if the service data is valid...'
            ),
            self.S_DATA_VALID_MESS_ID: (
                'The service data is valid.'
            ),
            self.S_DATA_INVALID_AND_CREATE_MESS_ID: (
                'The service data is invalid. Application will create the new one.'
            ),
            self.CHECK_SERV_NAME_MESS_ID: (
                'Checking server network name...'
            ),
            self.GOT_SERV_NAME_MESS_ID: (
                'Application got server network name: "{}".'
            ),
            self.NO_SERV_NAME_MESS_ID: (
                'Application could not get server network name.'
            ),
            self.LOAD_S_DATA_SUCC_MESS_ID: (
                'The service data was loaded from "{}" directory.'
            ),
            self.CREATE_LOADER_SUCC_MESS_ID: (
                'The application loader window is created.'
            ),
            self.DESTROY_LOADER_SUCC_MESS_ID: (
                'The application loader window is destroyed.'
            ),
            self.CREATE_ROOT_SUCC_MESS_ID: (
                'The application root window is created.'
            ),
            self.DESTROY_ROOT_SUCC_MESS_ID: (
                'The application root window is destroyed.'
            ),
            self.LOAD_A_DATA_FROM_SERV_MESS_ID: (
                'Loading the application data from "{}" directory...'
            ),
            self.LOAD_A_DATA_LOCAL_MESS_ID: (
                'Loading the application data from "{}" directory...'
            ),
            self.LOAD_A_DATA_FROM_SERV_SUCC_MESS_ID: (
                'The application data was loaded from "{}" directory.'
            ),
            self.LOAD_A_DATA_FROM_SERV_FAIL_MESS_ID: (
                'The application data was not loaded from "{}" directory.\n{}'
            ),
            self.LOAD_A_DATA_TRY_LOCAL_MESS_ID: (
                'The application will try to load the application data locally.'
            ),
            self.LOAD_A_DATA_LOCAL_SUCC_MESS_ID: (
                'The application data was loaded from "{}" directory.'
            ),
            self.LOAD_A_DATA_LOCAL_FAIL_MESS_ID: (
                'The application data was not loaded from "{}" directory.\n{}'
            ),
            self.SAVE_A_DATA_MESS_ID: (
                'Saving the application data into "{}" directory...'
            ),
            self.SAVE_A_DATA_SUCC_MESS_ID: (
                'The application data saved into "{}" directory.'
            ),
            self.SAVE_A_DATA_FAIL_MESS_ID: (
                'The application data was not saved into "{}" directory.\n{}'
            ),
            self.CHECK_A_DATA_UPDATED_MESS_ID: (
                'Checking if the application data was modified...'
            ),
            self.A_DATA_UPDATABLE_MESS_ID: (
                'The application data was modified.'
            ),
            self.A_DATA_NOT_UPDATABLE_MESS_ID: (
                'The application data was not modified'
            ),
            self.CHECK_A_DATA_UPDATED_FAIL_MESS_ID: (
                'The application cannot check if the application data was modified.\n{}'
            ),
            self.UPDATE_A_DATA_MESS_ID: (
                'Updating the application data'
            ),
            self.RESTART_APP_MESS_ID: (
                'Application is restarting...'
            ),
            self.IMPORT_CREDS_FROM_A_DATA_MESS_ID: (
                'Importing network credentials from the application data to the service data...'
            ),
            self.VALID_A_DATA_MESS_ID: (
                'Validating incoming application data...'
            ),
            self.VALID_A_DATA_FAIL_MESS_ID: (
                'Application could not validate the application data.\n{}'
            ),
            self.VALID_A_DATA_SUCC_MESS_ID: (
                'Application validated the application data.'
            ),
            self.VALID_A_DATA_DEFAULT_MESS_ID: (
                'Application found invalid values that can be replaced by default ones.'
            ),
            self.SHOW_ROOT_PREPARE_MESS_ID: (
                'Preparing the root window...'
            ),
            self.SHOW_ROOT_MESS_ID: (
                'Application prepared the root window. Displaying...'
            ),
            self.SHOW_MENU_MESS_ID: (
                'Preparing menu for displaying...'
            ),
            self.SHOW_MENU_SUCC_MESS_ID: (
                'Application menu is ready.'
            ),
            self.OPEN_DIALOG_LOAD_A_DATA_MESS_ID: (
                'Opening file dialog window to import the application data...'
            ),
            self.SHOW_INFO_DIALOG_MESS_ID: (
                'Application showed an information dialog window with message: "{}"'
            ),
            self.SHOW_ERR_DIALOG_MESS_ID: (
                'Application showed an error dialog window with message: "{}"'
            ),
            self.GOT_A_DATA_FILEDIR_MESS_ID: (
                'Application got directory of the application data: "{}"'
            ),
            self.EDIT_S_DATA_MESS_ID: (
                'The service data parameter "{}" changed its value to: "{}"'
            ),
            self.OPEN_CREDS_MODAL_MESS_ID: (
                'Opening network credentials modal window...'
            ),
            self.CLOSE_CREDS_MODAL_MESS_ID: (
                'Application closed network credentials modal window.'
            ),
            self.CLOSE_DIALOG_LOAD_A_DATA_MESS_ID: (
                'Application closed file dialog meant to import the application data.'
            ),
            self.OPEN_HELP_DIALOG_MESS_ID: (
                'Opening help dialog window with title name: "{}"...'
            ),
            self.CLOSE_HELP_DIALOG_MESS_ID: (
                'Application closed help dialog window.'
            ),
            self.PREPARE_ROOT_BG_MESS_ID: (
                'Preparing the root window background...'
            ),
            self.SET_CURS_VALS_MESS_ID: (
                'Setting the cursor values...'
            ),
            self.CONFIG_BUTTONS_MESS_ID: (
                'Configuring buttons...'
            ),
            self.CONFIG_BUTTONS_SUCC_MESS_ID: (
                'Application configured buttons.'
            ),
            self.NO_CONFIG_BUTTONS_MESS_ID: (
                'Application did not configured any buttons.'
            ),
            self.CONFIG_GROUPS_MESS_ID: (
                'Configuring groups...'
            ),
            self.CONFIG_GROUPS_SUCC_MESS_ID: (
                'Application configured groups.'
            ),
            self.SHOW_GROUPS_MESS_ID: (
                'Placing groups on the root window...'
            ),
            self.SHOW_GROUPS_SUCC_MESS_ID: (
                'Application placed all groups on the root window.'
            ),
            self.SHOW_NO_GROUPS_MESS_ID: (
                'Application did not placed any groups on the root window.'
            ),
            self.SHOW_BUTTONS_MESS_ID: (
                'Placing buttons on the root window...'
            ),
            self.SHOW_BUTTONS_SUCC_MESS_ID: (
                'Application placed all buttons on the root window.'
            ),
            self.PRESS_BUTTON_MESS_ID: (
                'Pressed button with name: "{}"'
            ),
            self.OPEN_DIR_MESS_ID: (
                'Opening directory: "{}"...'
            ),
            self.RUN_CMD_MESS_ID: (
                'Running command: "{}"...'
            ),
            self.RUN_CMD_SUCC_MESS_ID: (
                'Application successfully performed the command.'
            ),
            self.RUN_CMD_FAIL_MESS_ID: (
                'Application could not perform the command.'
            ),
            self.S_DATA_EXISTS_MESS_ID: (
                'The service data file exists.'
            ),
            self.CONFIG_LOADER_MESS_ID: (
                'Application configuring the loader window...'
            ),
            self.CONFIG_LOADER_SUCC_MESS_ID: (
                'Application configured the loader window.'
            ),
            self.CONFIG_ROOT_MESS_ID: (
                'Application configuring the root window...'
            ),
            self.CONFIG_ROOT_WIDTH_ERR_MESS_ID: (
                'Invalid value for the root window width {}.'
            ),
            self.CONFIG_ROOT_SUCC_MESS_ID: (
                'Application configured the root window.'
            ),
            self.APP_CLOSED_MESS_ID: (
                'Application with session name "{}" is closed.'
            ),
        }
        
    def log(self, level, message_id, vars=None):
        """Logs about an app event.
        
        Gets the logging instance according to a log level 
        and creates a log message.

        Args:
            level (int): The log level.
            message_id (int): The identifier of a log message.
            vars (tuple, optional): Optional values for composing the log message. Defaults to None.
        """
        
        log_functions = {
            self.INFO: logging.info,
            self.WARN: logging.warning,
            self.ERR: logging.error,
        }
        
        log_functions.get(level, None)(self._get_message_by_id(message_id, vars))
        
    def clear_logs(self):
        with open(self.__file_dir, 'w', encoding='utf-8') as f:
            f.write('')
        
    def _get_message_by_id(self, id, vars=None):
        """Compose a log message by the identifier.
        
        If an identifier is worng or optional variables are not match 
        to this type of message, returns the certain message.

        Args:
            id (int): The identifier of a log message.
            vars (tuple, optional): Optional values for composing the log message. Defaults to None.

        Returns:
            str: The log message.
        """
        
        invalid_message = f'Invalid args for message id {id}. Args: {vars}.'
        unknown_message = f'Unknown message id {id}.'
        
        message = self.message_map.get(id, unknown_message)
        
        if message != unknown_message:
            try:
                return message if not vars else message.format(*vars)
            
            except IndexError:
                return invalid_message
            
        return unknown_message