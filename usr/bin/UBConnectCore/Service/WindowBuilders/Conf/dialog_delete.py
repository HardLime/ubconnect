import gettext
import locale

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

translate = gettext.translation("ubconnect", '/usr/share/locale', fallback=True)
i18n = translate.gettext

class DialogDelete(Gtk.Dialog):
    def __init__(self, parent, device):
        self.language_sys = locale.getdefaultlocale()
        translate.install()

        super().__init__(title=i18n("Deleting"), transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        translatedText = i18n("Are you sure you want to remove the device:")
        label = Gtk.Label(label=f"{translatedText} {device}?")

        box = self.get_content_area()
        box.add(label)
        self.show_all()
