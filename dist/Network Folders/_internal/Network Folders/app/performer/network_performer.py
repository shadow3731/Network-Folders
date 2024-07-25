class CommandResult():
    def __init__(self, returncode):
        self.returncode = returncode

class NetworkPerformer():
    def __init__(self, logs_perf):
        self._win_cmds = {
            'win create map': 'net use "\\\\{id}" /user:"{user}" "{passw}"',
            'win delete map': 'net use "\\\\{id}" /delete /yes',
            'win open folder': 'explorer "{path}"',
            'win open file': '{file}',
        }
        self._non_win_cmds = {
            'nonwin open directory': 'echo "{passw}" | sudo -S open "{path}"',
        }
        
        self.logs_perf = logs_perf
            
    def execute(self, command_flag, **kwargs):
        timeout = kwargs.get('timeout', 0.0)
        
        if command_flag == 'win create map':
            command = self._win_cmds[command_flag].format(
                id=kwargs['identifier'],
                user=kwargs['username'],
                passw=kwargs['password'],
            )
            return self._run(
                command, 
                timeout=timeout, 
                hide_cmd=kwargs['hide_cmd'],
            )
        
        elif command_flag == 'win open file':
            command = self._win_cmds[command_flag].format(
                file=kwargs['file']
            )
            return self._run(
                command, 
                timeout=timeout,
                is_win_file=True,
            )
        
        elif command_flag == 'win open folder':
            command = self._win_cmds[command_flag].format(
                path=kwargs['path'],
                timeout=timeout,
            )
            return self._run(command, timeout=kwargs['timeout'])
        
        elif command_flag == 'win delete map':
            command = self._win_cmds[command_flag].format(
                id=kwargs['identifier']
            )
            return self._run(
                command, 
                timeout=timeout, 
                hide_cmd=kwargs['hide_cmd']
            )
            
        elif command_flag == 'nonwin open directory':
            command = self._non_win_cmds[command_flag].format(
                passw=kwargs['password'],
                path=kwargs['path'],
                timeout=timeout,
            )
            return self._run(command, timeout=kwargs['timeout'])
        
    def _run(self, command, **kwargs):
        if kwargs.get('is_win_file') and kwargs['is_win_file'] is True:   
            self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.RUN_CMD_MESS_ID, (command,))
            
            import os
                     
            if os.path.exists(command):                
                os.startfile(command)
                return CommandResult(0)
            
            else:
                result = self._run(command, timeout=kwargs['timeout'])
                
                if result.returncode == 0 or result.returncode == 1:
                    return CommandResult(0)
                
                return CommandResult(-1)
            
        else:
            self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.RUN_CMD_MESS_ID, (command,))
            
            import subprocess
            
            if kwargs.get('hide_cmd') and kwargs['hide_cmd'] is True:
                startup_info = subprocess.STARTUPINFO()
                startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startup_info.wShowWindow = subprocess.SW_HIDE
                
                return subprocess.run(
                    command,
                    stderr=subprocess.PIPE, 
                    stdout=subprocess.PIPE,
                    timeout=kwargs['timeout'],
                    startupinfo=startup_info,
                )
                
            else:
                return subprocess.run(
                    command,
                    stderr=subprocess.PIPE, 
                    stdout=subprocess.PIPE,
                    timeout=kwargs['timeout'],
                )
            
    def get_network_device_identifier(self, filepath):
        patterns = [r'\\\\([^\\]+)', r'//([^/]+)']
        
        for pattern in patterns:
            from re import match
            matches = match(pattern, filepath)
            
            if matches:
                return matches.group(1)
            
        return None
    
    def get_network_device_ip(self, identifier):
        from socket import gethostbyname
        return gethostbyname(identifier) if identifier else None