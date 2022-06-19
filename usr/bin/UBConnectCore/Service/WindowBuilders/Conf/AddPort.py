import gettext
import locale

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

translate = gettext.translation("ubconnect", '/usr/share/locale', fallback=True)
i18n = translate.gettext

class AddPort:
    def __init__(self, conf):
        self.language_sys = locale.getdefaultlocale()
        translate.install()

        self.vm = conf.vmthis
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")
        self.builder.connect_signals(EventHandler(self))
        self.add_port_win = self.builder.get_object("add_port_dialog")
        self.name = self.builder.get_object("port_entry_name")
        self.protocol = self.builder.get_object("port_cmb_protocol")
        self.host_ip = self.builder.get_object("port_entry_host_address")
        self.host_port = self.builder.get_object("port_entry_host_port")
        self.guest_ip = self.builder.get_object("port_entry_guest_address")
        self.guest_port = self.builder.get_object("port_entry_guest_port")
        print(self.vm)
        self.add_port_win.show()

        self.update_translation()

    def update_translation(self):
        self.builder.get_object("lblNameAddPort").set_label(i18n("Name"))
        self.builder.get_object("lblProtocolAddPort").set_label(i18n("Protocol"))
        self.builder.get_object("lblHostAddressAddPort").set_label(i18n("Host address"))
        self.builder.get_object("lblHostPortAddPort").set_label(i18n("Host port"))
        self.builder.get_object("lblGuestAddressAddPort").set_label(i18n("Guest address"))
        self.builder.get_object("lblGuestPortAddPort").set_label(i18n("Guest port"))
        self.builder.get_object("lblCanceladd_port_dialog").set_label(i18n("Cancel"))
        self.builder.get_object("lblApplyadd_port_dialog").set_label(i18n("Apply"))
        self.builder.get_object("add_port_dialog").set_title(i18n("Add rule"))


class EventHandler:

    def __init__(self, context):
        self.context = context

    def add_port_add_btn_clicked_cb(self, btn):
        # ConfigureRules().create_rule(Rule()
        self.get_data()
        print(self.Name)
        # print(self.Potocol)
        print(self.Host_ip)
        print(self.Host_port)
        print(self.Guest_ip)
        print(self.Guest_port)

    def add_port_close_btn_clicked_cb(self, btn):
        self.context.add_port_win.destroy()

    def get_data(self):
        self.Name = self.context.name.get_text()
        self.Potocol = self.context.protocol.get_value()
        self.Host_ip = self.context.host_ip.get_text()
        self.Host_port = self.context.host_port.get_text()
        self.Guest_ip = self.context.guest_ip.get_text()
        self.Guest_port = self.context.guest_port.get_text()


if __name__ == '__main__':
    main = AddPort()
    Gtk.main()
