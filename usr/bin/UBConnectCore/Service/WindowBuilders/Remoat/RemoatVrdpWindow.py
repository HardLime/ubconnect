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


class RemoteVrdpWindow:
    def __init__(self, connect_select, context):
        self.language_sys = locale.getdefaultlocale()
        translate.install()

        self.script_path = "ubconnect "
        self.connect_select = connect_select
        self.contextMain = context
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")
        self.second_win = self.builder.get_object("vrdp2")
        self.builder.connect_signals(EventHandler(self))
        self.second_win.show()
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

            if settings.display != "":
                if settings.display == "default":
                    self.display_default.set_active(True)
                elif settings.display == "client":
                    self.display_full.set_active(True)
                else:
                    self.display_custom.set_active(True)
                    temp = settings.display.split("x")
                    self.display_custom_width.set_text(temp[0])
                    self.display_custom_height.set_text(temp[1])

            if settings.catalogcustom != "":
                self.folder_custom.set_active(True)
                self.folder_custom_path.set_text(f"{settings.catalogcustom}")
            if settings.cataloghome == "True":
                self.folder_home.set_active(True)

            if settings.title != "":
                self.title.set_active(True)
                self.title_text.set_text(f"{settings.title}")
            if settings.icon != "":
                self.icon.set_active(True)
                self.icon_path.set_text(f"{settings.icon}")
            if settings.audio == "True":
                self.audio.set_active(True)

    def initiation_ui(self):
        self.ip_entry = self.builder.get_object("remote_vrdp_entry_ip")
        self.ip_entry.connect("changed", self.ok_ip)
        self.port_entry = self.builder.get_object("remote_vrdp_entry_port")
        self.port_entry.connect("changed", self.ok_ip)
        self.login = self.builder.get_object("remote_vrdp_entry_login")
        self.password = self.builder.get_object("remote_vrdp_entry_password")
        self.domain = self.builder.get_object("remote_vrdp_entry_domain")
        self.certignore = self.builder.get_object("remote_vrdp_cb_ignore")
        self.connect_name = self.builder.get_object("remote_vrdp_entry_conn_name")
        self.display_default = self.builder.get_object("remote_vrdp_rb_default_size")
        self.display_full = self.builder.get_object("remote_vrdp_rb_client_size")
        self.display_custom = self.builder.get_object("remote_vrdp_rb_manual")
        self.display_custom_width = self.builder.get_object("remote_vrdp_entry_width")
        self.display_custom_width.connect("changed", self.ok_ip)
        self.display_custom_height = self.builder.get_object("remote_vrdp_entry_height")
        self.display_custom_height.connect("changed", self.ok_ip)
        self.display_color = self.builder.get_object("remote_vrdp_cmb_color")
        self.display_color.connect("changed", self.selected_color_changed)
        self.browse_button = self.builder.get_object("remote_vrdp_btn_browse")
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

        self.folder_home = self.builder.get_object("remote_vrdp_cb_sharedfolder")
        self.folder_custom = self.builder.get_object("remote_vrdp_cb_connect_folder")
        self.folder_custom_path = self.builder.get_object("remote_vrdp_entry_path")
        self.printer_default = self.builder.get_object("remote_vrdp_cb_printer")
        self.printer_all = self.builder.get_object("remote_vrdp_cb_printer_reset")
        self.printer_custom = self.builder.get_object("remote_vrdp_cb_printer_connect")
        self.printer_custom_name = self.builder.get_object("remote_vrdp_cmb_printers")
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

        self.audio = self.builder.get_object("remote_vrdp_cb_audio")
        self.title = self.builder.get_object("remote_vrdp_cb_title")
        self.title_text = self.builder.get_object("remote_vrdp_entry_title")
        self.icon = self.builder.get_object("remote_vrdp_cb_icon")
        self.icon_path = self.builder.get_object("remote_vrdp_entry_icon")

        self.crdesktop = self.builder.get_object("remote_vrdp_btn_create")
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

            if self.connect_name.get_text() != "":
                connectionstring = connectionstring + f"--name \"{self.connect_name.get_text()}\" "

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
            if exists(f"{desktop}/{self.connect_name.get_text()}.desktop"):
                msgTitle = i18n("Confirm action")
                msgText = i18n("The file already exists. Enter yes to overwrite the file:")
                yes = subprocess.getoutput(f"zenity --entry --title \"{msgTitle}\"--icon-name=\"info\" --text \"{msgText}\"")
                subprocess.getoutput(f"echo {yes} | {connectionstring} --rdesktop-vrdp")
            else:
                subprocess.getoutput(f"{connectionstring} --rdesktop-vrdp")

            self.get_new_settings()
            self.contextMain.list_store_remote.clear()
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
            self.contextMain.start_update()
            self.second_win.destroy()
        else:
            msgTitle = i18n("Error")
            msgText = i18n("You must enter the address and connection name!")
            subprocess.getoutput(f"zenity --error --title \"{msgTitle}\" --text \"{msgText}\"")

    def get_new_settings(self):
        newsettings = ConnectSettings()
        newsettings.title = self.title_text.get_text()
        newsettings.icon = self.icon_path.get_text()
        newsettings.connectclient = "rdesktop-vrdp"
        newsettings.vmname = "coming soon..."
        newsettings.ip = self.ip_entry.get_text()
        newsettings.port = self.port_entry.get_text()
        newsettings.domen = self.domain.get_text()
        newsettings.connectname = self.connect_name.get_text()
        newsettings.connectstartapp = ""
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
        # настройка разрешения

        if self.display_full.get_active():
            newsettings.display = "client"
        elif self.display_default.get_active():
            newsettings.display = "default"
        elif self.display_custom.get_active():
            newsettings.display = f"{self.display_custom_width.get_text()}x{self.display_custom_height.get_text()}"
        else:
            newsettings.display = ""
        # настройка разрешения
        # настройка каталогов
        if self.folder_home.get_active():
            newsettings.cataloghome = "True"
        else:
            newsettings.cataloghome = "False"
        if self.folder_custom.get_active():
            newsettings.catalogcustom = f"{self.folder_custom_path.get_text()}"
        else:
            newsettings.catalogcustom = ""
        # настройка каталогов
        if self.audio.get_active():
            newsettings.audio = "True"
        else:
            newsettings.audio = "False"
        newsettings.displaycolor = self.color
        newsettings.connecttype = "VRDP"
        Settings().writeSettings(newsettings)
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
        self.builder.get_object("lblHost").set_label(i18n("Host"))
        self.builder.get_object("lblLoginvrdp2").set_label(i18n("Login:"))
        self.builder.get_object("lblPasswordvrdp2").set_label(i18n("Password:"))
        self.builder.get_object("lblDomenvrdp2").set_label(i18n("Domain:"))
        self.builder.get_object("lblPortvrdp2").set_label(i18n("Port:"))
        self.builder.get_object("lblIgnoreCertvrdp2").set_label(i18n("Ignore certificate"))
        self.builder.get_object("lblAdditionalyvrdp2").set_label(i18n("Additionally"))
        self.builder.get_object("lblConnNamevrdp2").set_label(i18n("Connection name:"))
        self.builder.get_object("lblScreenSettingsvrdp2").set_label(i18n("Screen settings"))
        self.builder.get_object("lblDefaultResolutionvrdp2").set_label(i18n("Original size"))
        self.builder.get_object("lblClientResolutionvrdp2").set_label(i18n("Client resolution"))
        self.builder.get_object("lblCustomvrdp2").set_label(i18n("Manually:"))
        self.builder.get_object("lblNavrdp2").set_label(i18n("by"))
        self.builder.get_object("lblPalletevrdp2").set_label(i18n("Palette:"))
        self.builder.get_object("lblSharedCatalogvrdp2").set_label(i18n("Shared catalog"))
        self.builder.get_object("lblHomeCatalogForwardingvrdp2").set_label(i18n("Auto forwarding\nhome directory of host in VM"))
        self.builder.get_object("lblConnCatalogvrdp2").set_label(i18n("Catalog connection"))
        self.builder.get_object("lblPrintervrdp2").set_label(i18n("Printer"))
        self.builder.get_object("lblAutoForwardPrintervrdp2").set_label(i18n("Automatic forwarding\ndefault printer host in VM"))
        self.builder.get_object("lblAutoForwardingAllPrintesvrdp2").set_label(i18n("Automatic forwarding\nall host printers in VM"))
        self.builder.get_object("lblPrinterConnvrdp2").set_label(i18n("Printer connection"))
        self.builder.get_object("lblSoundMicrovrdp2").set_label(i18n("Sound and microphone"))
        self.builder.get_object("lbSoundMicroForwardingvrdp2").set_label(i18n("Sound and microphone forwarding"))
        self.builder.get_object("lblWindowAppearance").set_label(i18n("Connection window appearance"))
        self.builder.get_object("lblWindowTitlevrdp2").set_label(i18n("Window title"))
        self.builder.get_object("lblIconvrdp2").set_label(i18n("Icon"))
        self.builder.get_object("lblCancelvrdp2").set_label(i18n("Cancel"))
        self.builder.get_object("lblCreatevrdp2").set_label(i18n("Create"))
        self.builder.get_object("vrdp2").set_title(i18n("Create VRDP connection shortcut"))

class EventHandler:

    def __init__(self, context):
        self.context = context

    def close_remote_vrdp(self, test):
        self.context.second_win.destroy()

    def remote_vrdp_btn_browse_clicked_cb(self, but):
        root = tkinter.Tk()
        root.withdraw()
        self.context.path = filedialog.askdirectory(parent=root, initialdir="/", title=i18n("Please select a directory"))
        self.context.folder_custom_path.set_text(self.context.path)

    def remote_vrdp_cb_connect_folder_clicked_cb(self, cb):
        isActive = self.context.folder_custom.get_active()
        self.context.browse_button.set_sensitive(isActive)
        self.context.folder_custom_path.set_sensitive(isActive)
