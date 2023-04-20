import detect


# Load the correct library methods for detecting whether the user is using
# A dark or light theme.
if detect.windows:
    from darkdetect._windows_detect import isDark
elif detect.mac:
    from darkdetect._mac_detect import isDark
else:
    from darkdetect._linux_detect import isDark



class Theme:


    def __init__(self, *args, **kwargs) -> None:
        self.__dark = isDark()
        self.cursor = 'pointinghand' if detect.mac else '@Windows_Hand.cur'
        self.set_theme_colours()


    def change_theme(self) -> None:
        """ Change the theme to the opposite of what it was. """
        self.__dark = not self.__dark
        self.set_theme_colours()
        return


    def dark_theme_colours(self) -> None:
        """ Set the colours to the dark theme colours. """
        self.background = "black"
        self.foreground = "white"
        self.border = "white"
        return


    def get_dark(self) -> bool:
        return self.__dark


    def light_theme_colours(self) -> None:
        """ Set the colours to the light theme colours. """
        self.background = "white"
        self.foreground = "black"
        self.border = "black"
        return

    
    def set_theme_colours(self) -> None:
        """ Set the colours for the specific theme. """
        if self.__dark:
            self.dark_theme_colours()
        else:
            self.light_theme_colours()
        return