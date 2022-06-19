import gettext
import locale
import subprocess
import tkinter
from tkinter import filedialog

import gi
import subprocess

import virtualbox as virtualbox

from UBConnectCore.Service.WindowBuilders.Conf.AddPort import AddPort
from UBConnectCore.Service.WindowBuilders.Conf.VMPorts import ConfigureRules
from UBConnectCore.Service.WindowBuilders.ConfigVmWindow import ConfigVmWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

translate = gettext.translation("ubconnect", '/usr/share/locale', fallback=True)
i18n = translate.gettext

class PortsWindow:
    def __init__(self, conf):
        self.language_sys = locale.getdefaultlocale()
        translate.install()

        self.fold = conf
        self.vmthis = conf.vm
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")
        self.Ports_win = self.builder.get_object("portswin")
        self.ports_tv = self.builder.get_object("ports_tv")
        self.builder.connect_signals(EventHandler(self))
        self.Ports_win.show()
        # print(ConfigureRules.get_rule_list(self.vmthis))
        self.test = ConfigureRules().get_rule_list(self.vmthis)
        self.ports_gener()

        self.update_translation()

    def ports_gener(self):
        self.list_fold = Gtk.ListStore(str, str, str, str, str, str)
        text_renderer = Gtk.CellRendererText()

        self.col1 = Gtk.TreeViewColumn(title=i18n("Name"), cell_renderer=text_renderer, text=0)
        self.col2 = Gtk.TreeViewColumn(title=i18n("Protocol"), cell_renderer=text_renderer, text=1)
        self.col3 = Gtk.TreeViewColumn(title=i18n("Host address"), cell_renderer=text_renderer, text=2)
        self.col4 = Gtk.TreeViewColumn(title=i18n("Host port"), cell_renderer=text_renderer, text=3)
        self.col5 = Gtk.TreeViewColumn(title=i18n("Guest address"), cell_renderer=text_renderer, text=4)
        self.col6 = Gtk.TreeViewColumn(title=i18n("Guest port"), cell_renderer=text_renderer, text=5)

        self.ports_tv.append_column(self.col1)
        self.ports_tv.append_column(self.col2)
        self.ports_tv.append_column(self.col3)
        self.ports_tv.append_column(self.col4)
        self.ports_tv.append_column(self.col5)
        self.ports_tv.append_column(self.col6)
        self.ports_tv.set_model(self.list_fold)

        self.fill_ports()

    def fill_ports(self):
        print("AAA", len(ConfigureRules().get_rule_list(self.vmthis)))
        i = 0
        while i < len(ConfigureRules().get_rule_list(self.vmthis)):
            self.list_fold.append([self.test[i].name, self.test[i].type,
                                   self.test[i].host_ip, self.test[i].host_port,
                                   self.test[i].guest_ip, self.test[i].guest_port])
            i += 1

    def update_translation(self):
        self.builder.get_object("lblCancelportswin").set_label(i18n("Cancel"))
        self.builder.get_object("lblSaveportswin").set_label(i18n("Save"))


class EventHandler:

    def __init__(self, context):
        self.context = context

    def btn_add_port_activate_cb(self, btn):
        AddPort(self.context)

    def change_ports_save_activate_cb(self, btn):
        self.context.Ports_win.destroy()

    def change_ports_close_clicked_cb(self, btn):
        self.context.Ports_win.destroy()

    def btn_delete_port_activate_cb(self, btn):
        ConfigureRules().delete_rule(rule_name=self.f, vm_name=self.context.vmthis)
        self.context.list_fold.clear()
        self.context.fill_ports()

    def ports_tv_change(self, select):
        self.model, self.treeiter = select.get_selected()
        if self.treeiter is not None:
            rownumobj = self.model.get_path(self.treeiter)
            self.row = int(rownumobj.to_string())

        self.f = self.context.test[self.row].name


if __name__ == '__main__':
    main = PortsWindow()
    Gtk.main()
