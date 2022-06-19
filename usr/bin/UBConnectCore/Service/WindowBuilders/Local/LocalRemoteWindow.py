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

class LocalRemoteWindow:
    def __init__(self, vmname, ip):
        self.language_sys = locale.getdefaultlocale()
        translate.install()

        self.builder = Gtk.Builder()
        self.vmname = vmname
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")
        self.second_win = self.builder.get_object("remote")
        self.builder.connect_signals(EventHandler(self))
        self.ip = ip
        self.script_path = "ubconnect "
        self.second_win.show()
        self.initiation_ui()

        self.update_translation()

    def initiation_ui(self):
        self.ip_entry = self.builder.get_object("local_ra_entry_ip")
        if self.ip is not None:
            self.ip_entry.set_text(f"{self.ip}")
        self.ip_entry.connect("changed", self.ok_ip)
        self.port_entry = self.builder.get_object("local_ra_entry_port")
        self.port_entry.connect("changed", self.ok_ip)
        self.login = self.builder.get_object("local_ra_entry_login")
        self.password = self.builder.get_object("local_ra_entry_password")
        self.domain = self.builder.get_object("local_ra_entry_domain")
        self.certignore = self.builder.get_object("local_ra_cb_ignore")
        self.connect_name = self.builder.get_object("local_ra_entry_conn_name")

        self.xfreerdp = self.builder.get_object("local_ra_rb_xfree")

        self.rdesktop = self.builder.get_object("local_ra_rb_rdesktopseam")

        self.appstart_path = self.builder.get_object("local_ra_entry_app")

        self.browse_button = self.builder.get_object("local_ra_btn_browse")
        self.folder_home = self.builder.get_object("local_ra_cb_sharedfolder")
        self.folder_custom = self.builder.get_object("local_ra_cb_connect_folder")
        self.folder_custom_path = self.builder.get_object("local_ra_entry_path")
        self.printer_default = self.builder.get_object("local_ra_cb_printer")
        self.printer_all = self.builder.get_object("local_ra_cb_printer_reset")
        self.printer_custom = self.builder.get_object("local_ra_cb_printer_connect")
        self.printer_custom_name = self.builder.get_object("local_ra_cmb_printers")
        self.printer_custom_name.connect("changed", self.selected_printer_changed)

        self.browse_button = self.builder.get_object("local_ra_btn_browse")

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
        self.audio = self.builder.get_object("local_ra_cb_audio")
        self.xfreerdp.set_active(True)
        self.crdesktop = self.builder.get_object("local_ra_btn_create")
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
            connectionstring = f"{self.script_path}"
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

            connectionstring = connectionstring + f"--name \"{self.vmname}\" "
            filename = f"{self.vmname}"

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
            if exists(f"{desktop}/{filename}.desktop"):
                msgTitle = i18n("Confirm action")
                msgText = i18n("The file already exists. Enter yes to overwrite the file:")
                yes = subprocess.getoutput(f"zenity --entry --title \"{msgTitle}\" --icon-name=\"info\" --text \"{msgText}\"")
                subprocess.getoutput(f"echo {yes} | {connectionstring} --{self.connect_client} --remoteapp")
                self.second_win.destroy()
            else:
                subprocess.getoutput(f"{connectionstring} --{self.connect_client} --remoteapp")
                self.second_win.destroy()
        else:
            msgTitle = i18n("Error")
            msgText = i18n("You must enter the connection address!")
            subprocess.getoutput(f"zenity --error --title \"{msgTitle}\" --text \"{msgText}\"")

    def ok_ip(self, widget):
        entry = widget.get_text()
        if entry != "":
            temp = entry[-1]
            if not temp.isdigit() and temp != ".":
                widget.set_text(entry[0:-1])

    def check_property(self):
        return self.ip_entry.get_text() != ""

    def update_translation(self):
        self.builder.get_object("lblHostRemote").set_label(i18n("Host"))
        self.builder.get_object("lblLoginRemote").set_label(i18n("Login:"))
        self.builder.get_object("lblPasswordRemote").set_label(i18n("Password:"))
        self.builder.get_object("lblDomenRemote").set_label(i18n("Domain:"))
        self.builder.get_object("lblPortRemote").set_label(i18n("Port:"))
        self.builder.get_object("lblIgnoreCertRemote").set_label(i18n("Ignore certificate"))
        self.builder.get_object("lblClientRemote").set_label(i18n("Connection client"))
        self.builder.get_object("lblXfreerdpRemote").set_label(i18n("xfreerdp (Windows 7 and newer)"))
        self.builder.get_object("lblAppStartRemote").set_label(i18n("Application launch"))
        self.builder.get_object("lblAppRemote").set_label(i18n("App:"))
        self.builder.get_object("lblSharedCatalogRemote").set_label(i18n("Shared catalog"))
        self.builder.get_object("lblAutoForwardingHomeRemote").set_label(i18n("Auto forwarding\nhome directory of host in VM"))
        self.builder.get_object("lblCatalogConnectionRemote").set_label(i18n("Catalog connection"))
        self.builder.get_object("lblPrinterRemote").set_label(i18n("Printer"))
        self.builder.get_object("lblAutoForwardingPrinterRemote").set_label(i18n("Automatic forwarding\ndefault printer host in VM"))
        self.builder.get_object("lblAutoForwardingAllPrintersRemote").set_label(i18n("Automatic forwarding\nall host printers in VM"))
        self.builder.get_object("lblPrinterConnectionRemote").set_label(i18n("Printer connection"))
        self.builder.get_object("lblSoundMicroRemote").set_label(i18n("Sound and microphone"))
        self.builder.get_object("lblSoundMicroForwardingRemote").set_label(i18n("Sound and microphone forwarding"))
        self.builder.get_object("lblCancelRemote").set_label(i18n("Cancel"))
        self.builder.get_object("lblCreateRemote").set_label(i18n("Create"))
        self.builder.get_object("remote").set_title(i18n("Create RemoteApp connection shortcut"))


class EventHandler:

    def __init__(self, context):
        self.context = context

    def close_local_remote(self, test):
        self.context.second_win.destroy()

 # NEW (Короче, такое же должно быть во всехподключениях)
    def local_ra_btn_browse_clicked_cb(self, but):
        root = tkinter.Tk()
        root.withdraw()
        self.context.path = filedialog.askdirectory(parent=root, initialdir="/", title=i18n("Please select a directory"))
        self.context.folder_custom_path.set_text(self.context.path)

    def local_ra_cb_connect_folder_activate_cb(self, cb):
        isActive = self.context.folder_custom.get_active()
        self.context.browse_button.set_sensitive(isActive)
        self.context.folder_custom_path.set_sensitive(isActive)

if __name__ == '__main__':
    main = LocalRemoteWindow()
    Gtk.main()
