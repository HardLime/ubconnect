#!/usr/bin/env python
import gettext
import locale

import gi

from UBConnectCore.Service import VM

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

translate = gettext.translation("ubconnect", '/usr/share/locale', fallback=True)
i18n = translate.gettext

class AddUsb:
    def __init__(self):
        self.language_sys = locale.getdefaultlocale()
        translate.install()

        self.builder = Gtk.Builder()
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")
        self.update_translation()
        self.dialog_add_usb: Gtk.Dialog = self.builder.get_object("dialog_add_usb")

        self.listbox_usb: Gtk.TreeView = self.builder.get_object('list_usb')
        self.listbox_selection_usb: Gtk.TreeSelection = self.listbox_usb.get_selection()
        self.listbox_usb_list = Gtk.ListStore(bool, str, str, str)
        self.listbox_usb_generated()

        self.btn_dialog_add_usb_add: Gtk.Button = self.builder.get_object("btn_dialog_add_usb_add")
        self.btn_dialog_add_usb_add.connect("clicked", self.btn_dialog_add_usb_add_clicked)
        self.btn_dialog_add_usb_cancel: Gtk.Button = self.builder.get_object("btn_dialog_add_usb_cancel")
        self.btn_dialog_add_usb_cancel.connect("clicked", self.btn_dialog_add_usb_cancel_clicked)

        self.response_type = Gtk.ResponseType.CANCEL

        self.listbox_usb.show_all()
        self.dialog_add_usb.run()

    def listbox_usb_generated(self, *args):
        list_usb = VM.UsbDevices().get_usb_list()
        i = 0
        while i != len(list_usb):
            name = f'{list_usb[i].product_name} [{list_usb[i].vendor_id}]'
            activate = False
            vendor_id = list_usb[i].vendor_id
            product_id = list_usb[i].product_id

            self.listbox_usb_list.append([activate, name, product_id, vendor_id])
            i += 1

        bool_renderer = Gtk.CellRendererToggle()
        bool_renderer.connect("toggled", self.on_cell_toggled)
        text_renderer = Gtk.CellRendererText()

        active_column = Gtk.TreeViewColumn(title="", cell_renderer=bool_renderer, active=0)
        device_column = Gtk.TreeViewColumn(title="", cell_renderer=text_renderer, text=1)

        self.listbox_usb.append_column(active_column)
        self.listbox_usb.append_column(device_column)

        self.listbox_usb.set_model(self.listbox_usb_list)

    def on_cell_toggled(self, widget, path):
        self.listbox_usb_list[path][0] = not self.listbox_usb_list[path][0]

    def btn_dialog_add_usb_add_clicked(self, button):
        self.response_type = Gtk.ResponseType.OK
        self.dialog_add_usb.destroy()

    def btn_dialog_add_usb_cancel_clicked(self, button):
        self.response_type = Gtk.ResponseType.CANCEL
        self.dialog_add_usb.destroy()

    def get_result(self):
        result_list = Gtk.ListStore(bool, str, str, str)
        for el in self.listbox_usb_list:
            if el[0]:
                result_list.append([el[0], el[1], el[2], el[3]])
        return result_list

    def update_translation(self):
        self.builder.get_object("lblDevicesDialogAddUsb").set_label(i18n("Devices"))
        self.builder.get_object("lblCanceldialog_add_usb").set_label(i18n("Cancel"))
        self.builder.get_object("lblAdddialog_add_usb").set_label(i18n("Add"))
        self.builder.get_object("dialog_add_usb").set_title(i18n("Add USB-device"))
