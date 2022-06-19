import gettext
import locale
import subprocess
import tkinter
from os.path import exists
from tkinter import filedialog

import gi

from UBConnectCore.Service.WindowBuilders.Conf.SettingsModule import ConnectSettings, Settings

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

translate = gettext.translation("ubconnect", '/usr/share/locale', fallback=True)
i18n = translate.gettext

class RemoteRemoteWindow:
    def __init__(self, connect_select, context):
        self.language_sys = locale.getdefaultlocale()
        translate.install()

        self.script_path = "ubconnect "
        self.connect_select = connect_select
        self.contextMain = context
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")
        self.second_win = self.builder.get_object("remote2")
        self.builder.connect_signals(EventHandler(self))
        self.second_win.show()
        self.color = 2
        self.store1 = Gtk.ListStore(int, str)
        self.initiation_ui()
        self.initiation_settings()

        self.update_translation()

    def initiation_settings(self):
        if self.connect_select is not None:
            settings = Settings().getSettings(self.connect_select)
            # заполнение текстовых полей
            self.ip_entry.set_text(f"{settings.ip}")
            self.port_entry.set_text(f"{settings.port}")
            self.domain.set_text(f"{settings.domen}")
            self.connect_name.set_text(f"{settings.connectname}")

            # заполнение текстовых полей
            if settings.printerall == "True":
                self.printer_all.set_active(True)
            if settings.printerdefault == "True":
                self.printer_default.set_active(True)
            if settings.printercustom != "":
                self.printer_custom.set_active(True)

            if settings.catalogcustom != "":
                self.folder_custom.set_active(True)
                self.folder_custom_path.set_text(f"{settings.catalogcustom}")
            if settings.cataloghome == "True":
                self.folder_home.set_active(True)

            if settings.audio == "True":
                self.audio.set_active(True)
            if settings.connectclient == "xfreerdp":
                self.xfreerdp.set_active(True)
            else:
                self.rdesktop.set_active(True)
            if settings.connectstartapp != "":
                self.appstart_path.set_text(settings.connectstartapp)
            else:
                self.appstart_path.set_text("")

    def initiation_ui(self):
        self.ip_entry = self.builder.get_object("remote_ra_entry_ip")
        self.ip_entry.connect("changed", self.ok_ip)
        self.port_entry = self.builder.get_object("remote_ra_entry_port")
        self.port_entry.connect("changed", self.ok_ip)
        self.login = self.builder.get_object("remote_ra_entry_login")
        self.password = self.builder.get_object("remote_ra_entry_password")
        self.domain = self.builder.get_object("remote_ra_entry_domain")
        self.certignore = self.builder.get_object("remote_ra_cb_ignore")
        self.connect_name = self.builder.get_object("remote_ra_entry_conn_name")

        self.xfreerdp = self.builder.get_object("remote_ra_rb_xfree")

        self.rdesktop = self.builder.get_object("remote_ra_rb_rdesktopseam")

        self.appstart_path = self.builder.get_object("remote_ra_entry_app")

        self.browse_button = self.builder.get_object("remote_ra_btn_browse")
        self.folder_home = self.builder.get_object("remote_ra_cb_sharedfolder")
        self.folder_custom = self.builder.get_object("remote_ra_cb_connect_folder")
        self.folder_custom_path = self.builder.get_object("remote_ra_entry_path")
        self.printer_default = self.builder.get_object("remote_ra_cb_printer")
        self.printer_all = self.builder.get_object("remote_ra_cb_printer_reset")
        self.printer_custom = self.builder.get_object("remote_ra_cb_printer_connect")
        self.printer_custom_name = self.builder.get_object("remote_ra_cmb_printers")
        self.printer_custom_name.connect("changed", self.selected_printer_changed)

        store = Gtk.ListStore(int, str)
        cell = Gtk.CellRendererText()
        printers = subprocess.getoutput("lpstat -e").split("\n")
        i = 0
        for printer in printers:
            store.append([i, printer])
            i = i + 1
        self.printer_custom_name.set_model(store)
        self.printer_custom_name.set_active(0)
        self.printer_custom_name.pack_start(cell, True)
        self.printer_custom_name.add_attribute(cell, "text", 1)
        self.audio = self.builder.get_object("remote_ra_cb_audio")
        self.xfreerdp.set_active(True)
        self.crdesktop = self.builder.get_object("remote_ra_btn_create")
        self.crdesktop.connect("clicked", self.create_desktop)

    def selected_printer_changed(self, widget):
        iter = self.printer_custom_name.get_active_iter()
        if iter is not None:
            model = self.printer_custom_name.get_model()
            row_id, name = model[iter][:2]
            self.custom_printer = name
            print(name)
    def create_desktop(self, widget):
        if self.check_property() == True:
            connectionstring=f"{self.script_path}"
            if self.ip_entry.get_text() != "":
                connectionstring = connectionstring + f"--ip {self.ip_entry.get_text()} "

            if self.port_entry.get_text() != "":
                connectionstring = connectionstring + f"--port {self.port_entry.get_text()} "

            if self.login.get_text() != "":
                connectionstring = connectionstring + f"--login \"{self.login.get_text()}\" "

            if self.password.get_text() != "":
                connectionstring = connectionstring + f"--password {self.password.get_text()} "

            if self.domain.get_text() != "":
                connectionstring = connectionstring + f"--domain \"{self.domain.get_text()}\" "

            if self.connect_name.get_text() != "":
                connectionstring = connectionstring + f"--name \"{self.connect_name.get_text()}\" "

            if self.folder_custom.get_active():
                if self.folder_custom_path.get_text() != "":
                    connectionstring = connectionstring + f"--mountcatalog \"{self.folder_custom_path.get_text()}\" "

            if self.folder_home.get_active():
                connectionstring = connectionstring + f"--mounthome "

            if self.printer_default.get_active():
                connectionstring = connectionstring + f"--defaultprinter "

            if self.printer_all.get_active():
                connectionstring = connectionstring + f"--allprinters "

            if self.audio.get_active():
                connectionstring = connectionstring + f"--audio "

            if self.printer_custom.get_active():
                connectionstring = connectionstring + f"--printer \"{self.custom_printer}\" "

            self.connect_client = "xfreerdp"
            if self.xfreerdp.get_active():
                self.connect_client = "xfreerdp"
            else:
                self.connect_client = "rdesktop"

            if self.appstart_path.get_text() != "":
                connectionstring = connectionstring + f"--appstart \"{self.appstart_path.get_text()}\""

            desktop = subprocess.getoutput("xdg-user-dir DESKTOP")
            if exists(f"{desktop}/{self.connect_name.get_text()}.desktop"):
                msgTitle = i18n("Confirm action")
                msgText = i18n("The file already exists. Enter yes to overwrite the file:")
                yes = subprocess.getoutput(f"zenity --entry --title \"{msgTitle}\" --icon-name=\"info\" --text \"{msgText}\"")
                subprocess.getoutput(f"echo {yes} | {connectionstring} --{self.connect_client}")
            else:
                subprocess.getoutput(f"{connectionstring} --{self.connect_client} --remoteapp")
            self.get_new_settings()
            self.contextMain.list_store_remote.clear()
            self.contextMain.start_update()
            self.second_win.destroy()
        else:
            msgTitle = i18n("Error")
            msgText = i18n("You must enter the address and connection name!")
            subprocess.getoutput(f"zenity --error --title \"{msgTitle}\" --text \"{msgText}\"")

    def get_new_settings(self):
        newsettings = ConnectSettings()

        newsettings.vmname = "coming soon..."
        newsettings.ip = self.ip_entry.get_text()
        newsettings.port = self.port_entry.get_text()
        newsettings.icon = ""
        newsettings.display = ""
        newsettings.displaycolor = ""
        newsettings.domen = self.domain.get_text()
        newsettings.connectname = self.connect_name.get_text()
        newsettings.title = ""
        # настройка принтеров
        if self.printer_custom.get_active():
            newsettings.printercustom = self.custom_printer
        else:
            newsettings.printercustom = ""

        if self.printer_all.get_active():
            newsettings.printerall = "True"
        else:
            newsettings.printerall = "False"

        if self.printer_default.get_active():
            newsettings.printerdefault = "True"
        else:
            newsettings.printerdefault = "False"
        # настройка принтеров

        # настройка каталогов
        if self.folder_home.get_active():
            newsettings.cataloghome = "True"
        else:
            newsettings.cataloghome = "False"
        if self.folder_custom.get_active():
            newsettings.catalogcustom = f"{self.folder_custom_path.get_text()}"
        else:
            self.folder_custom_path.set_text("")
            newsettings.catalogcustom = ""
        # настройка каталогов
        if self.audio.get_active():
            newsettings.audio = "True"
        else:
            newsettings.audio = "False"

        if self.appstart_path.get_text() != "":
            newsettings.connectstartapp = f"{self.appstart_path.get_text()}"
        else:
            newsettings.connectstartapp = ""

        if self.xfreerdp.get_active():
            newsettings.connectclient = "xfreerdp"
        else:
            newsettings.connectclient = "rdesktop"

        newsettings.connecttype = "RA"
        Settings().writeSettings(newsettings)
        self.contextMain.list_store_remote.clear()
        self.contextMain.fill_tv_vms_remote()
        self.connect_select = None

    def ok_ip(self, widget):
        entry = widget.get_text()
        if entry != "":
            temp = entry[-1]
            if not temp.isdigit() and temp != ".":
                widget.set_text(entry[0:-1])

    def check_property(self):
        return self.ip_entry.get_text() != "" and self.connect_name.get_text() != ""

    def update_translation(self):
        self.builder.get_object("lblHostremote2").set_label(i18n("Host"))
        self.builder.get_object("lblLoginremote2").set_label(i18n("Login:"))
        self.builder.get_object("lblPasswordremote2").set_label(i18n("Password:"))
        self.builder.get_object("lblDomenremote2").set_label(i18n("Domain:"))
        self.builder.get_object("lblPortremote2").set_label(i18n("Port:"))
        self.builder.get_object("lblIgnoreCertremote2").set_label(i18n("Ignore certificate"))
        self.builder.get_object("lblAdditionalyremote2").set_label(i18n("Additionally"))
        self.builder.get_object("lblConnNameremote2").set_label(i18n("Connection name:"))
        self.builder.get_object("lblConnClientremote2").set_label(i18n("Connection client"))
        self.builder.get_object("lblXfreerdpremote2").set_label(i18n("xfreerdp (Windows 7 and newer)"))
        self.builder.get_object("lblAppStartremote2").set_label(i18n("Application launch"))
        self.builder.get_object("lblAppremote2").set_label(i18n("App:"))
        self.builder.get_object("lblSharedCatalogremote2").set_label(i18n("Shared catalog"))
        self.builder.get_object("lblAutoForwHomeremote2").set_label(i18n("Auto forwarding\nhome directory of host in VM"))
        self.builder.get_object("lblConnCatalogremote2").set_label(i18n("Catalog connection"))
        self.builder.get_object("lblPrinterremote2").set_label(i18n("Printer"))
        self.builder.get_object("lblAutoForwDefaultPrinterremote2").set_label(i18n("Automatic forwarding\ndefault printer host in VM"))
        self.builder.get_object("lblAutoForwAllPrintersremote2").set_label(i18n("Automatic forwarding\nall host printers in VM"))
        self.builder.get_object("lblConnPrinterremote2").set_label(i18n("Printer connection"))
        self.builder.get_object("lblSoundMicroremote2").set_label(i18n("Sound and microphone"))
        self.builder.get_object("lblForwSoundMicroremote2").set_label(i18n("Sound and microphone forwarding"))
        self.builder.get_object("lblCancelremote2").set_label(i18n("Cancel"))
        self.builder.get_object("lblCreateremote2").set_label(i18n("Create"))
        self.builder.get_object("remote2").set_title(i18n("Create RemoteApp connection shortcut"))

class EventHandler:

    def __init__(self, context):
        self.context = context

    def close_remote_remote(self, test):
        self.context.second_win.destroy()

    def remote_ra_btn_browse_clicked_cb(self, but):
        root = tkinter.Tk()
        root.withdraw()
        self.context.path = filedialog.askdirectory(parent=root, initialdir="/", title=i18n("Please select a directory"))
        self.context.folder_custom_path.set_text(self.context.path)

    def remote_ra_cb_connect_folder_clicked_cb(self, cb):
        isActive = self.context.folder_custom.get_active()
        self.context.browse_button.set_sensitive(isActive)
        self.context.folder_custom_path.set_sensitive(isActive)


if __name__ == '__main__':
    main = RemoteRemoteWindow()
    Gtk.main()
