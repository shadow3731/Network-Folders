import tkinter as tk

from app.performer.expanded_tkinter import ExpandedTk, ExpandedCanvas, ExpandedFrame


class WindowFactory():
    def __init__(self, logs_perf=None):
        self.logs_perf = logs_perf
        
    def create_and_preapare_loader(self):
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.CREATE_LOADER_MESS_ID)       
        
        loading_window = ExpandedTk()
        
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.CREATE_LOADER_SUCC_MESS_ID)
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.CONFIG_LOADER_MESS_ID)
        
        loading_window.protocol(
            'WM_DELETE_WINDOW', 
            lambda: loading_window.on_close(self.logs_perf, True)
        )
        loading_window.configure(
            is_loader=True,
            width=200, 
            height=30, 
            title='Network Folders', 
            toolwindow=True
        )
        
        loading_label = tk.Label(loading_window, text='Запуск...', font=('Arial', 14))
        loading_label.pack()
        
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.CONFIG_LOADER_SUCC_MESS_ID)
        
        loading_window.update()
        
        return loading_window
    
    def create_main(self):
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.CREATE_ROOT_MESS_ID)
        
        main_window = ExpandedTk()
        
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.CREATE_ROOT_SUCC_MESS_ID)
        
        main_window.withdraw()
        
        return main_window
    
    def prepare_main(self, main_window, app_data, data_perf):
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.CONFIG_ROOT_MESS_ID)
        
        main_window.protocol(
            'WM_DELETE_WINDOW', 
            lambda: main_window.on_close(self.logs_perf)
        )

        canvas = ExpandedCanvas(main_window)
        canvas.place(x=0, y=-5, relheight=1, relwidth=1)
        canvas.bind_scrolling()
            
        from app.performer.menu_performer import MenuPerformer
        mp = MenuPerformer(canvas, data_perf, self.logs_perf)
        mp.show_menu(main_window)
        
        frame = ExpandedFrame(
            canvas,
            width=canvas.winfo_screenwidth(),
            height=canvas.winfo_screenheight(),
        )
        
        from app.util.cursor import Cursor
        cursor = Cursor()
        cursor.save_default_values(
            init_x=app_data['window']['padding'],
            init_y=app_data['window']['padding'],
            width=app_data['window']['button_width'],
            height=app_data['window']['button_height'],
            padding=app_data['window']['padding'],
            right_padding=app_data['window']['r_padding'],
            scr_width=app_data['window']['width'],
        )
        
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.SET_CURS_VALS_MESS_ID)
        
        cursor.load_deafault_values()
        
        from app.performer.buttons_performer import ButtonsPerformer
        buttons_perf = ButtonsPerformer(data_perf, self.logs_perf)
        buttons_pos = buttons_perf.configure_buttons(app_data, cursor)
        
        groups_pos = None
        
        if buttons_pos and len(buttons_pos) > 0:
            self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.SET_CURS_VALS_MESS_ID)
            
            cursor.load_deafault_values()
            
            from app.performer.groups_performer import GroupsPerformer
            groups_perf = GroupsPerformer(self.logs_perf)
            groups_pos = groups_perf.configure_groups(buttons_pos, cursor)
            
            groups_perf.show_groups(app_data, groups_pos, frame)
            buttons_perf.show_buttons(app_data, buttons_pos, frame, main_window)
            
        main_window.configure(
            width=app_data['window']['width'],
            height=0,
            title=app_data['app_name'],
            icon_file_path=data_perf.get_full_path(data_perf.icon_file_dir),
            groups_pos=groups_pos,
            canvas=canvas,
            frame=frame,
        )
        
        frame.update_idletasks()
        
        canvas.config(scrollregion=(0, 0, frame.winfo_reqwidth(), frame.winfo_reqheight()))
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)
        
        scrollbar = tk.Scrollbar(
            main_window,
            width=cursor.right_padding + 2,
            command=canvas.yview,
        )
        scrollbar.place(relx=1, rely=0, relheight=1, anchor=tk.NE)
        
        canvas.config(yscrollcommand=scrollbar.set)
        
        main_window.deiconify()
        
        self.logs_perf.log(self.logs_perf.INFO, self.logs_perf.CONFIG_ROOT_SUCC_MESS_ID)