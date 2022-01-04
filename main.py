import get_info
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

# initializes the GetHardwareInfo class for getting the hardware info
info = get_info.GetHardwareInfo()
# runs the functions that runs the commands and
# assings the required the variables to the output
info.get_mem_info()
info.get_cpu_info()
info.get_gpu_info()
info.get_motherboard_info()


class Main():
    """
    The main class that initializes the application
    """
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("main.ui")
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("app_window")

        # gets the objects needed from the ui file
        self.about = self.builder.get_object("about_dialog")
        self.mem_label = self.builder.get_object("mem_label")
        self.cpu_label = self.builder.get_object("cpu_label")
        self.gpu_label = self.builder.get_object("gpu_label")
        self.motherboard_label = self.builder.get_object("motherboard_label")

        # initializes the text variables for the labels
        label_mem_info = ""
        label_cpu_info = ""
        label_gpu_info = ""
        label_motherboard_info = ""

        for key in info.mem_info.keys():
            label_mem_info += f"<b>{key}</b>: {info.mem_info[key]}\n"

        for key in info.cpu_info.keys():
            label_cpu_info += f"<b>{key}</b>: {info.cpu_info[key]}\n"

        for key in info.gpu_info.keys():
            label_gpu_info += f"<b>{key}</b>: {info.gpu_info[key]}\n"

        for key in info.motherboard_info.keys():
            label_motherboard_info \
                += f"<b>{key}</b>: {info.motherboard_info[key]}\n"

        self.mem_label.set_markup(label_mem_info)
        self.cpu_label.set_markup(label_cpu_info)
        self.gpu_label.set_markup(label_gpu_info)
        self.motherboard_label.set_markup(label_motherboard_info)

        self.window.show_all()
        self.window.connect("destroy", Gtk.main_quit)

    def open_about(self, *args) -> None:
        """
        Shows the about dialog and
        connects the delete-event signal to close the dialog
        """
        self.about.connect("delete-event", self.close_about)
        self.about.run()

    def close_about(self, *args):
        """ Hides the about dialog """
        self.about.hide()


if __name__ == "__main__":
    Main()
    Gtk.main()
