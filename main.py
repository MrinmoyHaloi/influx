"""A application for Linux that displays hardware information."""
import get_info
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


class Main:
    """The main class that initializes the application."""

    def __init__(self):
        """Init function."""
        self.builder = Gtk.Builder()
        self.builder.add_from_file("main.ui")
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("app_window")

        # gets the objects needed from the ui file
        self.about = self.builder.get_object("about_dialog")
        self.preferences = self.builder.get_object("preferences_dialog")
        self.mem_label = self.builder.get_object("mem_label")
        self.cpu_label = self.builder.get_object("cpu_label")
        self.gpu_label = self.builder.get_object("gpu_label")
        self.motherboard_label = self.builder.get_object("motherboard_label")

        # initializes the text variables for the labels
        self.label_mem_info = ""
        self.label_cpu_info = ""
        self.label_gpu_info = ""
        self.label_motherboard_info = ""

        self.window.show_all()
        self.window.connect("destroy", Gtk.main_quit)

        # initializes the GetHardwareInfo class for getting the hardware info
        self.info = get_info.GetHardwareInfo()

        self.info.get_cpu_info()

        for key in self.info.cpu_info.keys():
            self.label_cpu_info += f"<b>{key}</b>: {self.info.cpu_info[key]}\n"

        self.cpu_label.set_markup(self.label_cpu_info)

    def open_about(self, *args) -> None:
        """Show the about dialog and connect the delete-event signal to close\
        the dialog."""
        self.about.connect("delete-event", self.close_about)
        self.about.run()
        
    def close_about(self, *args) -> None:
        """Hide the about dialog."""
        self.about.hide()

    def open_preferences(self, *args) -> None:
        """Show the preferences dialog and connect the delete-event signal to close\
        the dialog."""
        self.preferences.connect("delete-event", self.close_preferences)
        self.preferences.run()
        
    def close_preferences(self, *args) -> None:
        """Hide the preferences dialog."""
        self.preferences.hide()
    
    def set_info(self, notebook, page, page_num: int):
        """Run the commands needed and set the info on the respective label."""
        if page_num == 0:
            pass
        elif page_num == 1:
            if self.label_mem_info != "":
                pass
            else:
                self.info.get_mem_info()
                for key in self.info.mem_info.keys():
                    self.label_mem_info \
                        += f"<b>{key}</b>: {self.info.mem_info[key]}\n"
                self.mem_label.set_markup(self.label_mem_info)
        elif page_num == 2:
            if self.label_gpu_info != "":
                pass
            else:
                self.info.get_gpu_info()
                for key in self.info.gpu_info.keys():
                    self.label_gpu_info \
                        += f"<b>{key}</b>: {self.info.gpu_info[key]}\n"
                self.gpu_label.set_markup(self.label_gpu_info)
        elif page_num == 3:
            if self.label_motherboard_info != "":
                pass
            else:
                self.info.get_motherboard_info()
                for key in self.info.motherboard_info.keys():
                    self.label_motherboard_info \
                        += f"<b>{key}</b>: {self.info.motherboard_info[key]}\n"
                self.motherboard_label.set_markup(self.label_motherboard_info)


if __name__ == "__main__":
    # runs the application
    Main()
    Gtk.main()
