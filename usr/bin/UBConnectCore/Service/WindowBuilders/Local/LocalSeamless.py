import gettext
import locale
import subprocess
import tkinter
from os.path import exists
from tkinter import filedialog

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

translate = gettext.translation("ubconnect", '/usr/share/locale', fallback=True)
i18n = translate.gettext

class LocalSeamless:
    def __init__(self,vmname):
        self.language_sys = locale.getdefaultlocale()
        translate.install()
        self.builder = Gtk.Builder()
        self.vmname = vmname
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")
        self.second_win = self.builder.get_object("vboxseamless")
        self.sucess_win = self.builder.get_object("sucess")

        self.builder.connect_signals(EventHandler(self))
        self.script_path = "ubconnect "
        self.second_win.show()
        self.initiation_ui()

        self.update_translation()

    def initiation_ui(self):
        self.vmname_entry = self.builder.get_object("seamless_vmname")
        self.login_entry = self.builder.get_object("seamless_login")
        self.password_entry = self.builder.get_object("seamless_password")
        self.show_pass_btn = self.builder.get_object("pass_btn")
        self.app_check = self.builder.get_object("seamless_app_check")
        self.app_check.connect("checked", self.app_path_check)
        self.app_path = self.builder.get_object("seamless_app_path")
        self.btn_cancel = self.builder.get_object("seamless_cancel")
        self.btn_create = self.builder.get_object("seamless_create")
        self.btn_create.connect("toggled", self.create_desktop)

    def app_path_check(self):
        self.app_path.set_sensitive(self.app_check.get_active())


    def create_desktop(self, widget):
        if(self.app_check.get_active()):
            if(self.login_entry.get_text() and self.password_entry.get_text() and self.vmname_entry.get_text() and self.app_path.get_text()):
                subprocess.Popen([f"{self.script_path}", "--vboxseamless", f"--login {self.login_entry.get_text()}", f"--password {self.password_entry.get_text()}", f"--appstart {self.app_path.get_text()}", f"--name \"{self.vmname}_seamless\""])
                dialog = Gtk.MessageDialog(
                    transient_for=self.second_win,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text=i18n("Success"),
                )
                dialog.format_secondary_text(i18n("The shortcut is saved on the desktop!"))
                dialog.run()
                dialog.destroy()
                self.second_win.destroy()
            else:
                dialog = Gtk.MessageDialog(
                    transient_for=self.second_win,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text=i18n("Error"),
                )
                dialog.format_secondary_text(i18n("Fill in the required fields! \n(machine name, login, password, app path)"))
                dialog.run()
                dialog.destroy()  # необходим перевод
        else:
            if (self.login_entry.get_text() and self.password_entry.get_text() and self.vmname_entry.get_text()):
                subprocess.Popen([f"{self.script_path}", "--vboxseamless", f"--login {self.login_entry.get_text()}", f"--password {self.password_entry.get_text()}", f"--appstart {self.app_path.get_text()}", f"--name \"{self.vmname}\""])
                dialog = Gtk.MessageDialog(
                    transient_for=self.second_win,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text=i18n("Success"),
                )
                dialog.format_secondary_text(i18n("The shortcut is saved on the desktop!"))
                dialog.run()
                dialog.destroy()
                self.second_win.destroy()
            else:
                dialog = Gtk.MessageDialog(
                    transient_for=self.second_win,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text=i18n("Error"),
                )
                dialog.format_secondary_text(i18n("Fill in the required fields! \n(machine name, login, password)"))
                dialog.run()
                dialog.destroy()  # необходим перевод


    def update_translation(self):
        self.builder.get_object("seamless_label_host").set_label(i18n("Host"))
        self.builder.get_object("vmname_label").set_label(i18n("Machine Name:")) #добавить перевод
        self.builder.get_object("lblLoginvrdp1").set_label(i18n("Login:"))
        self.builder.get_object("lblPasswordvrdp1").set_label(i18n("Password:"))
        self.builder.get_object("lblWindowTitlerdp3").set_label(i18n("Application launch"))
        self.builder.get_object("vboxseamless").set_title(i18n("Create seamless mode connection shortcut")) #добавить перевод

class EventHandler:

    def __init__(self, context):
        self.context = context

    def close_local_vrdp(self, test):
        self.context.second_win.destroy()

if __name__ == '__main__':
    main = LocalVrdpWindow()
    Gtk.main()
