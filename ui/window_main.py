import tkinter
import ui.config_windows.window_channel_config as channel
import ui.config_windows.window_radio_config as radio
import ui.config_windows.window_system_config as system


class WindowMain():

    def __init__(self, system):
        self.system = system
        self.root = tkinter.Tk()
        self.setup_icon()
        self.setup_menubar()

    def setup_icon(self):
        self.root.title("Digital Radio System Simulator")
        self.root.call('wm', 'iconphoto', self.root._w, tkinter.PhotoImage(file='ui/images/icon.gif'))

    def setup_menubar(self):
        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)
        self.menu_config = tkinter.Menu(self.menu)
        self.menu_config.add_command(label='System Configuration', command=self.open_system_config)
        self.menu_config.add_command(label='Radio Configuration', command=self.open_radio_config)
        self.menu_config.add_command(label='Channel Configuration', command=self.open_channel_config)
        self.menu_help = tkinter.Menu(self.menu)
        self.menu_help.add_command(label='About')
        self.menu.add_cascade(label='Configurations', menu=self.menu_config)
        self.menu.add_cascade(label='Help', menu=self.menu_help)

    def run(self):
        self.root.mainloop()

    def open_system_config(self):
        print('System Configuration opened')
        window_system_config = system.WindowSystemConfig()
        self.system.config = window_system_config.apply()

    def open_radio_config(self):
        print('Radio Configuration opened')
        window_radio_config = radio.WindowRadioConfig()
        radio_config = window_radio_config.apply()
        self.system.radios[radio_config.radio_index] = radio_config

    def open_channel_config(self):
        print('Channel Configuration opened')
        window_channel_config = channel.WindowChannelConfig()