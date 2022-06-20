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

class LocalRdpWindow:
    def __init__(self, vmname, ip):
        self.language_sys = locale.getdefaultlocale()
        translate.install()

        self.builder = Gtk.Builder()
        self.ip = ip
        self.vmname = vmname
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")
        self.script_path = "ubconnect "
        self.second_win = self.builder.get_object("rdp1")
        self.builder.connect_signals(EventHandler(self))
        self.store1 = Gtk.ListStore(int, str)
        self.second_win.show()
        self.initiation_ui()

        self.update_translation()

    def initiation_ui(self):
        self.ip_entry = self.builder.get_object("local_rdp_entry_ip")
        if self.ip is not None:
            self.ip_entry.set_text(f"{self.ip}")
        self.ip_entry.connect("changed", self.ok_ip)
        self.port_entry = self.builder.get_object("local_rdp_entry_port")
        self.port_entry.connect("changed", self.ok_ip)
        self.login = self.builder.get_object("local_rdp_entry_login")
        self.password = self.builder.get_object("local_rdp_entry_password")
        self.password.set_visibility(False)
        self.domain = self.builder.get_object("local_rdp_entry_domain")
        self.certignore = self.builder.get_object("local_rdp_cb_ignore")
        self.connect_name = self.vmname
        self.display_default = self.builder.get_object("local_rdp_rb_default")
        self.display_full = self.builder.get_object("local_rdp_rb_client")
        self.display_custom = self.builder.get_object("local_rdp_rb_manual")
        self.display_custom_width = self.builder.get_object("local_rdp_entry_width")
        self.display_custom_width.connect("changed", self.ok_ip)
        self.display_custom_height = self.builder.get_object("local_rdp_entry_height")
        self.display_custom_height.connect("changed", self.ok_ip)
        self.xfreerdp = self.builder.get_object("local_rdp_rb_xfree")
        self.xfreerdp.connect("toggled", self.change_color)

        self.rdesktop = self.builder.get_object("local_rdp_rb_rdesktop")
        self.rdesktop.connect("toggled", self.change_color)

        self.defaultrdp = self.builder.get_object("local_rdp_rb_desktop")

        self.appstart = self.builder.get_object("local_rdp_rb_nondesktop")
        self.appstart_path = self.builder.get_object("local_rdp_entry_app")

        self.display_color = self.builder.get_object("local_rdp_cmb_color")
        self.display_color.connect("changed", self.selected_color_changed)

        cell1 = Gtk.CellRendererText()
        self.color = 2
        self.store1.append([1, "High color 15 bit"])
        self.store1.append([2, "High color 16 bit"])
        self.store1.append([3, "High color 24 bit"])
        self.store1.append([4, "RemoteFX"])
        self.store1.append([5, "GFX progressive"])
        self.store1.append([6, "GFX AVC420 32 bit"])
        self.store1.append([7, "GFX H264"])
        self.display_color.set_model(self.store1)
        self.display_color.set_active(1)
        self.display_color.pack_start(cell1, True)
        self.display_color.add_attribute(cell1, "text", 1)

        self.browse_button = self.builder.get_object("local_rdp_btn_browse")
        self.folder_home = self.builder.get_object("local_rdp_cb_sharedfolder")
        self.folder_custom = self.builder.get_object("local_rdp_cb_connect_folder")
        self.folder_custom_path = self.builder.get_object("local_rdp_entry_path")
        self.printer_default = self.builder.get_object("local_rdp_cb_printer")
        self.printer_all = self.builder.get_object("local_rdp_cb_printer_reset")
        self.printer_custom = self.builder.get_object("local_rdp_cb_printer_connect")
        self.printer_custom_name = self.builder.get_object("local_rdp_cmb_printers")
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

        self.audio = self.builder.get_object("local_rdp_cb_audio")
        self.title = self.builder.get_object("local_rdp_cb_title")
        self.title_text = self.builder.get_object("local_rdp_entry_title")
        self.icon = self.builder.get_object("local_rdp_cb_icon")
        self.icon_path = self.builder.get_object("local_rdp_entry_icon")

        self.xfreerdp.set_active(True)
        self.defaultrdp.set_active(True)
        self.crdesktop = self.builder.get_object("local_rdp_btn_createconn")
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
            print("sdsd")
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
            self.connect_client = "xfreerdp"
            if self.xfreerdp.get_active():
                self.connect_client = "xfreerdp"
            else:
                self.connect_client = "rdesktop"

            if self.appstart.get_active():
                connectionstring = connectionstring + f"--appstart \"{self.appstart_path.get_text()}\""

            desktop = subprocess.getoutput("xdg-user-dir DESKTOP")
            if exists(f"{desktop}/{filename}.desktop"):
                msgTitle = i18n("Confirm action")
                msgText = i18n("The file already exists. Enter yes to overwrite the file:")
                yes = subprocess.getoutput(f"zenity --entry --title \"{msgTitle}\" --icon-name=\"info\" --text \"{msgText}\"")
                subprocess.getoutput(f"echo {yes} | {connectionstring} --{self.connect_client}")
            else:
                subprocess.getoutput(f"{connectionstring} --{self.connect_client}")

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
            msgTitle = i18n("Error")
            msgText = i18n("You must enter the connection address!")
            subprocess.getoutput(f"zenity --error --title \"{msgTitle}\" --text \"{msgText}\"")

    def change_color(self, widget):
        self.store1.clear()
        self.display_color.clear()
        if self.xfreerdp.get_active():
            cell1 = Gtk.CellRendererText()
            self.color = 2
            self.store1.append([1, "High color 15 bit"])
            self.store1.append([2, "High color 16 bit"])
            self.store1.append([3, "High color 24 bit"])
            self.store1.append([4, "RemoteFX"])
            self.store1.append([5, "GFX progressive"])
            self.store1.append([6, "GFX AVC420 32 bit"])
            self.store1.append([7, "GFX H264"])
            self.display_color.set_model(self.store1)
            self.display_color.set_active(1)
            self.display_color.pack_start(cell1, True)
            self.display_color.add_attribute(cell1, "text", 1)
        else:
            cell1 = Gtk.CellRendererText()
            self.color = 2
            self.store1.append([1, "High color 15 bit"])
            self.store1.append([2, "High color 16 bit"])
            self.store1.append([3, "High color 24 bit"])
            self.store1.append([4, "High color 32 bit"])
            self.display_color.set_model(self.store1)
            self.display_color.set_active(1)
            self.display_color.pack_start(cell1, True)
            self.display_color.add_attribute(cell1, "text", 1)

    def ok_ip(self, widget):
        entry = widget.get_text()
        if entry != "":
            temp = entry[-1]
            if not temp.isdigit() and temp != ".":
                widget.set_text(entry[0:-1])

    def check_property(self):
        return self.ip_entry.get_text() != ""

    def update_translation(self):
        self.builder.get_object("lblHostrdp1").set_label(i18n("Host"))
        self.builder.get_object("lblLoginrdp1").set_label(i18n("Login:"))
        self.builder.get_object("lblPasswordrdp1").set_label(i18n("Password:"))
        self.builder.get_object("lblDomenrdp1").set_label(i18n("Domain:"))
        self.builder.get_object("lblPortrdp1").set_label(i18n("Port:"))
        self.builder.get_object("lblIgnoreCertrdp1").set_label(i18n("Ignore certificate"))
        self.builder.get_object("lblConnClientrdp1").set_label(i18n("Connection client"))
        self.builder.get_object("lblXfreerdprdp1").set_label(i18n("xfreerdp (Windows 7 and newer)"))
        self.builder.get_object("lblScreenSettingsrdp1").set_label(i18n("Screen settings"))
        self.builder.get_object("lblDefaultSizerdp1").set_label(i18n("Original size"))
        self.builder.get_object("lblClientSizerdp1").set_label(i18n("Client resolution"))
        self.builder.get_object("lblCustomSizerdp1").set_label(i18n("Manually:"))
        self.builder.get_object("lblNardp1").set_label(i18n("by"))
        self.builder.get_object("lblPalleterdp1").set_label(i18n("Palette:"))
        self.builder.get_object("lblSharedCatalogrdp1").set_label(i18n("Shared catalog"))
        self.builder.get_object("lblAutoForwHomerdp1").set_label(i18n("Auto forwarding\nhome directory of host in VM"))
        self.builder.get_object("lblConnCatalogrdp1").set_label(i18n("Catalog connection"))
        self.builder.get_object("lblPrinterrdp1").set_label(i18n("Printer"))
        self.builder.get_object("lblAutoForwDefaultPrinterrdp1").set_label(i18n("Automatic forwarding\ndefault printer host in VM"))
        self.builder.get_object("lblAutoForwAllPrintersrdp1").set_label(i18n("Automatic forwarding\nall host printers in VM"))
        self.builder.get_object("lblConnPrinterrdp1").set_label(i18n("Printer connection"))
        self.builder.get_object("lblSoundMicrordp1").set_label(i18n("Sound and microphone"))
        self.builder.get_object("lblSoundMicroForwrdp1").set_label(i18n("Sound and microphone forwarding"))
        self.builder.get_object("lblRemoteConnection").set_label(i18n("Remote connection mode"))
        self.builder.get_object("lblWithEnvrdp1").set_label(i18n("With desktop environment"))
        self.builder.get_object("lblWithoutEnvrdp1").set_label(i18n("No desktop environment. Launch application:"))
        self.builder.get_object("lblWindowAppearancerdp1").set_label(i18n("Connection window appearance"))
        self.builder.get_object("lblWindowTitlerdp1").set_label(i18n("Window title"))
        self.builder.get_object("lblIconrdp1").set_label(i18n("Icon"))
        self.builder.get_object("lblCancelrdp1").set_label(i18n("Cancel"))
        self.builder.get_object("lblCreaterdp1").set_label(i18n("Create"))
        self.builder.get_object("rdp1").set_title(i18n("Create RDP connection shortcut"))

class EventHandler:

    def __init__(self, context):
        self.context = context

    def close_local_rdp(self, test):
        self.context.second_win.destroy()

    def local_rdp_btn_browse_clicked_cb(self, but):
        root = tkinter.Tk()
        root.withdraw()
        self.context.path = filedialog.askdirectory(parent=root, initialdir="/", title=i18n("Please select a directory"))
        self.context.folder_custom_path.set_text(self.context.path)

    def local_rdp_cb_connect_folder_clicked_cb(self, cb):
        isActive = self.context.folder_custom.get_active()
        self.context.browse_button.set_sensitive(isActive)
        self.context.folder_custom_path.set_sensitive(isActive)

    def cvm_btn_show_pass_clicked_cb(self, button):
        self.context.password.set_visibility(not self.context.password.get_visibility())

if __name__ == '__main__':
    main = LocalRdpWindow()
    Gtk.main()
