import gettext
import locale
import os
import subprocess
import threading

import tkinter
from os.path import exists
from time import sleep

import virtualbox
import gi
from UBConnectCore.Service.WindowBuilders.Conf.SettingsModule import Settings, ConnectSettings
from UBConnectCore.Service.WindowBuilders.MainWindowEventHandler import EventHandler
from gi.repository.GLib import Thread



gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

translate = gettext.translation("ubconnect", '/usr/share/locale', fallback=True)
i18n = translate.gettext


class MainWindowBuilder:
    def __init__(self):
        self.language_sys = locale.getdefaultlocale()
        translate.install()

        self.builder = Gtk.Builder()
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")

        self.local_vm_tv = self.builder.get_object("local_tv_vms")
        self.remote_vm_tv = self.builder.get_object("remote_tv_vms")
        self.select = self.local_vm_tv.get_selection()
        self.select_local_index = 0

        self.list_store_remote = Gtk.ListStore(int, str, bool, str)
        self.list_store_local = Gtk.ListStore(int, str, bool, bool, str)

        self.gener()
        self.gener_local()

        self.builder.connect_signals(EventHandler(self))
        self.main_window = self.builder.get_object("main")
        self.main_window.show()
        self.select_local = 1
        self.fill_tv_vms()
        self.wait_window = self.builder.get_object("wait_window")

        self.lblLocalConnmain = self.builder.get_object("lblLocalConnmain")
        self.lblRemoteConnmain = self.builder.get_object("lblRemoteConnmain")
        self.lblVMContolLocalmain = self.builder.get_object("lblVMContolLocalmain")
        self.lblEnableLocalVMmain = self.builder.get_object("lblEnableLocalVMmain")
        self.lblDisableLocalVMmain = self.builder.get_object("lblDisableLocalVMmain")
        self.lblRestartLocalVMmain = self.builder.get_object("lblRestartLocalVMmain")
        self.lblSaveStateLocalVMmain = self.builder.get_object("lblSaveStateLocalVMmain")
        self.lblSettVBoxLocalVMmain = self.builder.get_object("lblSettVBoxLocalVMmain")
        self.lblCreateConnShortcutmain = self.builder.get_object("lblCreateConnShortcutmain")
        self.lblUpdateLocalListmain = self.builder.get_object("lblUpdateLocalListmain")
        self.lblVMControlRemotemain = self.builder.get_object("lblVMControlRemotemain")
        self.lblEnableRemoteVMmain = self.builder.get_object("lblEnableRemoteVMmain")
        self.lblDisableRemoteVMmain = self.builder.get_object("lblDisableRemoteVMmain")
        self.lblRestartRemoteVMmain = self.builder.get_object("lblRestartRemoteVMmain")
        self.lblSaveStateRemoteVMmain = self.builder.get_object("lblSaveStateRemoteVMmain")
        self.lblDeleteRemoteVMmain = self.builder.get_object("lblDeleteRemoteVMmain")
        self.lblCreateEditShortcutRemotemain = self.builder.get_object("lblCreateEditShortcutRemotemain")
        self.lblUpdateRemoteListmain = self.builder.get_object("lblUpdateRemoteListmain")
        self.waitText = self.builder.get_object("waitText")

        self.pid = None
        self.update_translations()
        self.start_update()

    def check_status(self, ip):
        return subprocess.getoutput(f"ping -c 1 {ip} -w 1 1>/dev/null; [ $? == \"0\" ] && echo \"work\"")

    def start_update(self):
        self.main_window.set_sensitive(False)

        self.pid = subprocess.Popen(["zenity", "--progress", "--pulsate", "--no-cancel"]).pid

        thread = threading.Thread(target=self.fill_tv_vms_remote, daemon=True)
        thread.start()

        thread.join()




    def fill_tv_vms_remote(self):
        vms_setting_list = Settings().getConnectList()

        i = 0
        for vm in vms_setting_list:
            print(self.check_status(vm.ip))
            if self.check_status(vm.ip) == "work":
                self.list_store_remote.append([i + 1, vm.connectname, True, vm.ip])
            else:
                self.list_store_remote.append([i + 1, vm.connectname, False, vm.ip])
            i = i + 1

        subprocess.getoutput(f"kill {self.pid}")
        self.main_window.set_sensitive(True)


    def gener(self):
        text_renderer = Gtk.CellRendererText()
        text_renderer.set_fixed_height_from_font(1)
        bool_renderer = Gtk.CellRendererToggle()
        bool_renderer.set_fixed_size(20, 20)
        text_renderer_for_number = Gtk.CellRendererText()
        text_renderer_for_number.set_alignment(xalign=0.5, yalign=0.5)

        col1 = Gtk.TreeViewColumn(title="№, п/п", cell_renderer=text_renderer_for_number, text=0)
        col2 = Gtk.TreeViewColumn(title=i18n("Name"), cell_renderer=text_renderer, text=1)
        col3 = Gtk.TreeViewColumn(title=i18n("Status"), cell_renderer=bool_renderer, active=2)
        col4 = Gtk.TreeViewColumn(title=i18n("IP-address"), cell_renderer=text_renderer, text=3)

        col1.set_max_width(60)

        self.remote_vm_tv.append_column(col1)
        self.remote_vm_tv.append_column(col2)
        self.remote_vm_tv.append_column(col3)
        self.remote_vm_tv.append_column(col4)

        self.remote_vm_tv.set_model(self.list_store_remote)

    def gener_local(self):
        text_renderer = Gtk.CellRendererText()
        text_renderer.set_fixed_height_from_font(1)
        text_renderer_for_number = Gtk.CellRendererText()
        text_renderer_for_number.set_alignment(xalign=0.5, yalign=0.5)
        bool_renderer = Gtk.CellRendererToggle()
        bool_renderer.set_fixed_size(20, 20)

        col1 = Gtk.TreeViewColumn(title="№, п/п", cell_renderer=text_renderer_for_number, text=0)
        col2 = Gtk.TreeViewColumn(title=i18n("Virtual machine"), cell_renderer=text_renderer, text=1)
        col3 = Gtk.TreeViewColumn(title=i18n("Autorun"), cell_renderer=bool_renderer, active=2)
        col4 = Gtk.TreeViewColumn(title=i18n("Status"), cell_renderer=bool_renderer, active=3)
        col5 = Gtk.TreeViewColumn(title=i18n("IP-address"), cell_renderer=text_renderer, text=4)

        col1.set_max_width(60)

        self.local_vm_tv.append_column(col1)
        self.local_vm_tv.append_column(col2)
        self.local_vm_tv.append_column(col3)
        self.local_vm_tv.append_column(col4)
        self.local_vm_tv.append_column(col5)

        self.local_vm_tv.set_model(self.list_store_local)

    def fill_tv_vms(self):
        i = 0
        if subprocess.getoutput("VBoxManage list vms"):
            machines = subprocess.getoutput("v=$(VBoxManage list vms);awk -F\'\"\' \'{print $2}\' <<< $v").split("\n")
            running_machines = subprocess.getoutput(
                "v=$(VBoxManage list runningvms);awk -F\'\"\' \'{print $2}\' <<< $v").split("\n")
            while i < len(machines):
                check_autorun = False
                state = False
                state = machines[i] in running_machines
                home = subprocess.getoutput("echo $HOME")
                temp = subprocess.getoutput(f"ls {home}/.config/systemd/user/default.target.wants/")
                check_autorun = f"ubconnect@{machines[i]}" in temp.replace("\\x20", " ")
                if not check_autorun:
                    check_autorun = exists(f"{home}/.config/autostart/ubconnect_{machines[i]}.desktop")

                ip = subprocess.getoutput(
                    f"v=$(VBoxManage guestproperty enumerate \"{machines[i]}\" | grep IP); awk -F ': |,' '{{print $4}}' <<< $v")

                self.list_store_local.append([i + 1, machines[i], check_autorun, state, ip])
                i += 1

    def update_translations(self):
        self.lblLocalConnmain.set_label(i18n("Local connection"))
        self.lblRemoteConnmain.set_label(i18n("Remote connection"))
        self.lblVMContolLocalmain.set_label(i18n("VM Control"))
        self.lblEnableLocalVMmain.set_label(i18n("Enable"))
        self.lblDisableLocalVMmain.set_label(i18n("Shutdown"))
        self.lblRestartLocalVMmain.set_label(i18n("Restart"))
        self.lblSaveStateLocalVMmain.set_label(i18n("Save state"))
        self.lblSettVBoxLocalVMmain.set_label(i18n("VirtualBox settings"))
        self.lblCreateConnShortcutmain.set_label(i18n("Create connection shortcut"))
        self.lblUpdateLocalListmain.set_label(i18n("Update list"))
        self.lblVMControlRemotemain.set_label(i18n("VM Control"))
        self.lblEnableRemoteVMmain.set_label(i18n("Enable"))
        self.lblDisableRemoteVMmain.set_label(i18n("Shutdown"))
        self.lblRestartRemoteVMmain.set_label(i18n("Restart"))
        self.lblSaveStateRemoteVMmain.set_label(i18n("Save state"))
        self.lblDeleteRemoteVMmain.set_label(i18n("Delete entry"))
        self.lblCreateEditShortcutRemotemain.set_label(i18n("Create/edit\nconnection shortcut"))
        self.lblUpdateRemoteListmain.set_label(i18n("Update list"))
        self.waitText.set_label(i18n("Updating the list of connections..."))

