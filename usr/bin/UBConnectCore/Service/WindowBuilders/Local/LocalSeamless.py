import gettext
import locale
import subprocess
import tkinter
from os.path import exists
from tkinter import filedialog

import gi

from UBConnectCore.Service.WindowBuilders.Conf.Dialogs import DialogSuccess

from UBConnectCore.Service.WindowBuilders.Conf.Dialogs import DialogError

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

translate = gettext.translation("ubconnect", '/usr/share/locale', fallback=True)
i18n = translate.gettext

class LocalSeamless:
    def __init__(self, vmname):
        self.language_sys = locale.getdefaultlocale()
        translate.install()
        self.builder = Gtk.Builder()
        self.vmname = ""+vmname.name
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")
        self.second_win = self.builder.get_object("vboxseamless")
        self.builder.connect_signals(EventHandler(self))
        self.script_path = "ubconnect "
        self.second_win.show()
        self.initiation_ui()

        self.update_translation()

    def initiation_ui(self):
        self.vmname_entry = self.builder.get_object("seamless_vmname")
        self.vmname_entry.set_text(self.vmname)
        self.login_entry = self.builder.get_object("seamless_login")
        self.password_entry = self.builder.get_object("seamless_password")
        self.password_entry.set_visibility(False)
        self.show_pass_btn = self.builder.get_object("pass_btn")
        self.app_check = self.builder.get_object("seamless_app_check")
        self.app_check.connect("toggled", self.app_path_check)
        self.app_path = self.builder.get_object("seamless_app_path")
        self.btn_cancel = self.builder.get_object("seamless_cancel")
        self.btn_create = self.builder.get_object("seamless_create")
        self.btn_create.connect("clicked", self.create_desktop)

    def app_path_check(self, sender):
        if(self.app_check.get_active()):
            self.login_entry.set_sensitive(True)
            self.password_entry.set_sensitive(True)
            self.app_path.set_sensitive(True)
        else:
            self.login_entry.set_sensitive(False)
            self.password_entry.set_sensitive(False)
            self.app_path.set_sensitive(False)


    def create_desktop(self, widget):
        if(self.app_check.get_active()):

            if(self.login_entry.get_text() and self.password_entry.get_text() and self.vmname_entry.get_text() and self.app_path.get_text()):
                subprocess.Popen([f"{self.script_path}", "--vboxseamless", f"--login {self.login_entry.get_text()}", f"--password {self.password_entry.get_text()}", f"--appstart {self.app_path.get_text()}", f"--name \"{self.vmname}_seamless\""])
                DialogSuccess("The shortcut is saved on the desktop!").show()
            else:
                DialogError("Fill in the required fields! \n(machine name, login, password, app path)").show()

        else:

            if (self.login_entry.get_text() and self.password_entry.get_text() and self.vmname_entry.get_text()):
                subprocess.Popen([f"{self.script_path}", "--vboxseamless", f"--login {self.login_entry.get_text()}", f"--password {self.password_entry.get_text()}", f"--appstart {self.app_path.get_text()}", f"--name \"{self.vmname}\""])
                DialogSuccess("The shortcut is saved on the desktop!").show()
                self.second_win.destroy()
            else:
                DialogError("Fill in the required fields! \n(machine name, login, password)").show()



    def update_translation(self):
        self.builder.get_object("seamless_label_host").set_label(i18n("Host"))
        self.builder.get_object("vmname_label").set_label(i18n("Machine Name:"))
        self.builder.get_object("lblLoginvrdp1").set_label(i18n("Login:"))
        self.builder.get_object("lblPasswordvrdp1").set_label(i18n("Password:"))
        self.builder.get_object("lblWindowTitlerdp3").set_label(i18n("Application launch"))
        self.builder.get_object("vboxseamless").set_title(i18n("Create seamless mode connection shortcut"))

class EventHandler:

    def __init__(self, context):
        self.context = context

    def close_local_vrdp(self, test):
        self.context.second_win.destroy()

    def cvm_btn_show_pass_clicked_cb(self, button):
        self.context.password_entry.set_visibility(not self.context.password_entry.get_visibility())

if __name__ == '__main__':
    main = LocalVrdpWindow()
    Gtk.main()
