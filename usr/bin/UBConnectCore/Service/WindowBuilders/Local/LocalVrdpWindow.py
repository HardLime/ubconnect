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

class LocalVrdpWindow:
    def __init__(self,vmname, ip):
        self.language_sys = locale.getdefaultlocale()
        translate.install()

        self.builder = Gtk.Builder()
        self.vmname = vmname
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")
        self.second_win = self.builder.get_object("vrdp1")
        self.ip = ip
        self.builder.connect_signals(EventHandler(self))
        self.script_path = "ubconnect "
        self.second_win.show()
        self.initiation_ui()

        self.update_translation()

    def initiation_ui(self):
        self.ip_entry = self.builder.get_object("local_vrdp_entry_ip")
        if self.ip is not None:
            self.ip_entry.set_text(f"{self.ip}")
        self.ip_entry.connect("changed", self.ok_ip)
        self.port_entry = self.builder.get_object("local_vrdp_entry_port")
        self.port_entry.connect("changed", self.ok_ip)
        self.login = self.builder.get_object("local_vrdp_entry_login")
        self.password = self.builder.get_object("local_vrdp_entry_password")
        self.domain = self.builder.get_object("local_vrdp_entry_domain")
        self.certignore = self.builder.get_object("local_vrdp_cb_ignore")
        self.connect_name = self.builder.get_object("local_vrdp_entry_conn_name")
        self.display_default = self.builder.get_object("local_vrdp_rb_default_size")
        self.display_full = self.builder.get_object("local_vrdp_rb_client_size")
        self.display_custom = self.builder.get_object("local_vrdp_rb_manual")
        self.display_custom_width = self.builder.get_object("local_vrdp_entry_width")
        self.display_custom_width.connect("changed", self.ok_ip)
        self.display_custom_height = self.builder.get_object("local_vrdp_entry_height")
        self.display_custom_height.connect("changed", self.ok_ip)
        self.display_color = self.builder.get_object("local_vrdp_cmb_color")
        self.display_color.connect("changed", self.selected_color_changed)

        self.browse_button = self.builder.get_object("local_vrdp_btn_browse")

        store1 = Gtk.ListStore(int, str)
        cell1 = Gtk.CellRendererText()
        self.color = 2

        store1.append([1, "High color 15 bit"])
        store1.append([2, "High color 16 bit"])
        store1.append([3, "High color 24 bit"])
        store1.append([4, "High color 32 bit"])

        self.display_color.set_model(store1)
        self.display_color.set_active(1)
        self.display_color.pack_start(cell1, True)
        self.display_color.add_attribute(cell1, "text", 1)

        self.folder_home = self.builder.get_object("local_vrdp_cb_sharedfolder")
        self.folder_custom = self.builder.get_object("local_vrdp_cb_connect_folder")
        self.folder_custom_path = self.builder.get_object("local_vrdp_entry_path")
        self.printer_default = self.builder.get_object("local_vrdp_cb_printer")
        self.printer_all = self.builder.get_object("local_vrdp_cb_printer_reset")
        self.printer_custom = self.builder.get_object("local_vrdp_cb_printer_connect")
        self.printer_custom_name = self.builder.get_object("local_vrdp_cmb_printers")
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

        self.audio = self.builder.get_object("local_vrdp_cb_audio")
        self.title = self.builder.get_object("local_vrdp_cb_title")
        self.title_text = self.builder.get_object("local_vrdp_entry_title")
        self.icon = self.builder.get_object("local_vrdp_cb_icon")
        self.icon_path = self.builder.get_object("local_vrdp_entry_icon")

        self.crdesktop = self.builder.get_object("local_vrdp_btn_createconn")
        self.crdesktop.connect("clicked", self.create_desktop)

    def selected_printer_changed(self, widget):
        iter = self.printer_custom_name.get_active_iter()
        if iter is not None:
            model = self.printer_custom_name.get_model()
            row_id, name = model[iter][:2]
            self.custom_printer = name
            print(name)

    def selected_color_changed(self, widget):
        iter = self.display_color.get_active_iter()
        if iter is not None:
            model = self.display_color.get_model()
            row_id, color = model[iter][:2]
            self.color = row_id
            print(self.color)

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

            connectionstring = connectionstring + f"--name \"{self.vmname}\" "
            filename = f"{self.vmname}"

            if self.title.get_active():
                connectionstring = connectionstring + f"--windowtitle \"{self.title_text.get_text()}\" "

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

            if self.icon.get_active():
                if self.icon_path.get_text() != "":
                    connectionstring = connectionstring + f"--icon \"{self.icon_path.get_text()}\" "

            if self.display_default.get_active():
                pass

            if self.display_full.get_active():
                connectionstring = connectionstring + f"--clientdisplay "

            if self.display_custom.get_active():
                connectionstring = connectionstring + f"--geometry {self.display_custom_width.get_text()}x{self.display_custom_height.get_text()} "

            desktop = subprocess.getoutput("xdg-user-dir DESKTOP")
            if exists(f"{desktop}/{filename}.desktop"):
                print("нашел")
                msgTitle = i18n("Confirm action")
                msgText = i18n("The file already exists. Enter yes to overwrite the file:")
                yes = subprocess.getoutput(f"zenity --entry --title \"{msgTitle}\"--icon-name=\"info\" --text \"{msgText}\"")
                subprocess.getoutput(f"echo {yes} | {connectionstring} --rdesktop-vrdp")
                self.second_win.destroy()
            else:
                subprocess.getoutput(f"{connectionstring} --rdesktop-vrdp")
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
        self.builder.get_object("lblHostvrdp1").set_label(i18n("Host"))
        self.builder.get_object("lblDomenvrdp1").set_label(i18n("Domain:"))
        self.builder.get_object("lblPortvrdp1").set_label(i18n("Port:"))
        self.builder.get_object("lblLoginvrdp1").set_label(i18n("Login:"))
        self.builder.get_object("lblPasswordvrdp1").set_label(i18n("Password:"))
        self.builder.get_object("lblScreenSettingsvrdp1").set_label(i18n("Screen settings"))
        self.builder.get_object("lblDefaultSizevrdp1").set_label(i18n("Original size"))
        self.builder.get_object("lblClientSizevrdp1").set_label(i18n("Client resolution"))
        self.builder.get_object("lblCustomSizevrdp1").set_label(i18n("Manually:"))
        self.builder.get_object("lblNavrdp1").set_label(i18n("by"))
        self.builder.get_object("lblPalletevrdp1").set_label(i18n("Palette:"))
        self.builder.get_object("lblSharedCatalogvrdp1").set_label(i18n("Shared catalog"))
        self.builder.get_object("lblAutoHomeForwvrdp1").set_label(i18n("Auto forwarding\nhome directory of host in VM"))
        self.builder.get_object("lblConnCatalogvrdp1").set_label(i18n("Catalog connection"))
        self.builder.get_object("lblPrintervrdp1").set_label(i18n("Printer"))
        self.builder.get_object("lblAutoForwDefaultPrintervrdp1").set_label(i18n("Automatic forwarding\ndefault printer host in VM"))
        self.builder.get_object("lblAutoForwAllPrintersvrdp1").set_label(i18n("Automatic forwarding\nall host printers in VM"))
        self.builder.get_object("lblPrinterConnvrdp1").set_label(i18n("Printer connection"))
        self.builder.get_object("lblSoundMicrovrdp1").set_label(i18n("Sound and microphone"))
        self.builder.get_object("lblAutoForwSoundMicrovrdp1").set_label(i18n("Sound and microphone forwarding"))
        self.builder.get_object("lblWindowAppearancevrdp1").set_label(i18n("Connection window appearance"))
        self.builder.get_object("lblWindowTitlevrdp1").set_label(i18n("Window title"))
        self.builder.get_object("lblWindowIconvrdp1").set_label(i18n("Icon"))
        self.builder.get_object("lblCancelvrdp1").set_label(i18n("Cancel"))
        self.builder.get_object("lblCreatevrdp1").set_label(i18n("Create"))
        self.builder.get_object("vrdp1").set_title(i18n("Create VRDP connection shortcut"))

class EventHandler:

    def __init__(self, context):
        self.context = context

    def close_local_vrdp(self, test):
        self.context.second_win.destroy()
    # NEW (Короче, такое же должно быть во всехподключениях)
    def local_vrdp_btn_browse_clicked_cb(self, but):
        root = tkinter.Tk()
        root.withdraw()
        self.context.path = filedialog.askdirectory(parent=root, initialdir="/", title=i18n("Please select a directory"))
        self.context.folder_custom_path.set_text(self.context.path)

    def local_vrdp_cb_connect_folder_activate_cb(self, cb):
        isActive = self.context.folder_custom.get_active()
        self.context.browse_button.set_sensitive(isActive)
        self.context.folder_custom_path.set_sensitive(isActive)
    #

    # NEW (Короче, такое же должно быть во всехподключениях)
    def local_vrdp_btn_browse_clicked_cb(self, but):
        root = tkinter.Tk()
        root.withdraw()
        self.context.path = filedialog.askdirectory(parent=root, initialdir="/", title=i18n("Please select a directory"))
        self.context.folder_custom_path.set_text(self.context.path)

    def local_vrdp_cb_connect_folder_activate_cb(self, cb):
        isActive = self.context.folder_custom.get_active()
        self.context.browse_button.set_sensitive(isActive)
        self.context.folder_custom_path.set_sensitive(isActive)

        #
if __name__ == '__main__':
    main = LocalVrdpWindow()
    Gtk.main()