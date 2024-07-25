from tkinter import Tk, Toplevel, Canvas, Frame


def center(object, width, height):
    screen_width = object.winfo_screenwidth()
    screen_height = object.winfo_screenheight()
        
    x = (screen_width - width) / 2
    y = (screen_height - height) / 2
        
    object.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

class ExpandedTk(Tk):    
    def configure(self, **kwargs):        
        self.resizable(False, False)
        self.title(kwargs['title'])
        
        if kwargs.get('toolwindow'):
            self.attributes('-toolwindow', True)
            
        window_width = kwargs['width']
        window_height = kwargs['height']
        
        is_loader = kwargs.get('is_loader')
        
        if is_loader is not True:
            self.iconbitmap(kwargs['icon_file_path'])
          
            widgets_height = 0
        
            if kwargs.get('groups_pos'):
                window_height = int(kwargs['groups_pos'][-1][1] + kwargs['groups_pos'][-1][-1])
                widgets_height = window_height
                
                if window_height > 515:
                    window_height = 515
                
            kwargs['canvas'].configure(height=widgets_height)
            kwargs['frame'].configure(height=widgets_height)
        
        center(self, window_width, window_height)
        
    def on_close(self, logs_perf=None, data_perf=None, disabled_btn=False):
        if disabled_btn is False:
            logs_perf.log(logs_perf.INFO, logs_perf.DESTROY_ROOT_MESS_ID)
            
            self.destroy()
            
            logs_perf.log(logs_perf.INFO, logs_perf.DESTROY_ROOT_SUCC_MESS_ID)
            
            data_perf.delete_files((data_perf.service_file_dir, data_perf.data_file_dir))
            logs_perf.clear_logs()

class ExpandedTopLevel(Toplevel):
    def configure(self, **kwargs):
        self.resizable(False, False)
        self.title(kwargs['title'])
                
        if kwargs.get('toolwindow'):
            self.attributes('-toolwindow', True)
                
        center(self, kwargs['width'], kwargs['height'])

    def on_close(self, canvas, logs_perf):
        self.destroy()
        canvas.bind_scrolling()
        
        logs_perf.log(logs_perf.INFO, logs_perf.CLOSE_HELP_DIALOG_MESS_ID)

class ExpandedCanvas(Canvas):
    def configure(self, **kwargs):
        self.config(height=kwargs['height'])
          
    def bind_scrolling(self):
        self.bind_all('<MouseWheel>', lambda e: self._on_mousewheel(e))
        
    def unbind_scrolling(self):
        self.unbind_all('<MouseWheel>')
        
    def _on_mousewheel(self, event):
        self.yview_scroll(-1*(event.delta // 120), 'units')
        
class ExpandedFrame(Frame):
    def configure(self, **kwargs):
        self.config(height=kwargs['height'])