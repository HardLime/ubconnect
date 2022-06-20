import gettext
import locale

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

translate = gettext.translation("ubconnect", '/usr/share/locale', fallback=True)
i18n = translate.gettext

class DialogSuccess:
    def __init__(self, message):
        self.language_sys = locale.getdefaultlocale()
        translate.install()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")
        self.second_win = self.builder.get_object("sucess")
        self.builder.connect_signals(self)
        self.builder.get_object("message").set_text(i18n(f"{message}"))

    def show(self):
        self.second_win.run()

    def click(self, widget):
        self.second_win.destroy()