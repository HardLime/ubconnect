import os
import subprocess
from time import sleep

import gi
import virtualbox
# from gi.overrides.Gtk import Builder
# from vboxapi import VirtualBoxManager
from gi.repository.Gtk import Builder

from UBConnectCore.Service.WindowBuilders.Conf.SettingsModule import Settings
from UBConnectCore.Service.WindowBuilders.ConfigVmWindow import ConfigVmWindow
from UBConnectCore.Service.WindowBuilders.Local.LocalRdpWindow import LocalRdpWindow
from UBConnectCore.Service.WindowBuilders.Local.LocalRemoteWindow import LocalRemoteWindow
from UBConnectCore.Service.WindowBuilders.Local.LocalVrdpWindow import LocalVrdpWindow
from UBConnectCore.Service.WindowBuilders.Remoat.RemoatRdpWindow import RemoteRdpWindow
from UBConnectCore.Service.WindowBuilders.Remoat.RemoatVrdpWindow import RemoteVrdpWindow
from UBConnectCore.Service.WindowBuilders.Remoat.RemoteRemoteWindow import RemoteRemoteWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class EventHandler:

    def __init__(self, context):
        self.context = context
        self.selected_vm = None
        self.vm = virtualbox.VirtualBox()
        self.session = virtualbox.Session()
        self.machine = None

        self.vm_tv = self.context.local_vm_tv
        self.select_vm_ip = self.vm_tv.get_selection()
        self.select_vm_ip.connect("changed", self.on_selection_changed)
        self.rem_vm_tv = self.context.remote_vm_tv
        self.connect_select = None
        self.vm_ip = None

        self.btn_turn_on = context.builder.get_object("local_btn_turn_on")
        self.btn_turn_off = context.builder.get_object("local_btn_turn_off")
        self.btn_reboot = context.builder.get_object("local_btn_reboot")
        self.btn_save_state = context.builder.get_object("local_btn_save_state")
        self.btn_config = context.builder.get_object("local_btn_vbox_config")


        select = self.rem_vm_tv.get_selection()
        select.connect("changed", self.on_remote_selection_changed)

        self.list_store = None
        self.bc = BtnController(context=context)
        self.launch_timer = None
        self.power_off_timer = None

    def on_destroy(self, widget):
        Gtk.main_quit()

    def local_btn_fill_tv_clicked_cb(self, btn):
        self.context.list_store_local.clear()
        self.context.fill_tv_vms()

    def on_selection_changed(self, widget):
        model, treeiter = widget.get_selected()
        if treeiter is not None:
            data = model.get_value(treeiter, 0)
            self.btn_config.set_sensitive(True)
            ip = model.get_value(treeiter, 4)
            status = model.get_value(treeiter, 3)
            self.set_button_visible(status)
            self.vm_ip = ip
            self.machine = virtualbox.VirtualBox().machines[data - 1]
            temp = model[treeiter][0] - 1
            row_num = temp
            hashes = []
            for item in self.vm.machines:
                hashes.append(item.id_p)
            self.selected_vm = hashes[row_num]
            self.machine = self.vm.find_machine(self.selected_vm)

    def start_vm(self, widget):
        subprocess.getoutput(f"VBoxManage startvm {self.machine.id_p} --type headless")

    def turn_off_vm(self, widget):
        subprocess.getoutput(f"VBoxManage controlvm {self.machine.id_p} acpipowerbutton")

    def reboot_vm(self, widget):
        subprocess.getoutput(f"VBoxManage controlvm {self.machine.id_p} reset")

    def pause_vm(self, widget):
        os.system("VBoxManage controlvm " + self.machine.id_p + " savestate")

    def config_vbox_show(self, widget):
        Builder()

    def update_tv(self):
        self.context.list_store.clear()
        self.context.prep_data()
        self.context.local_vm_tv.set_model(self.context.list_store)

    def local_btn_vrdp_clicked_cb(self, widget):
        LocalVrdpWindow(self.machine, self.vm_ip)

    def local_btn_rdp_clicked_cb(self, widget):
        LocalRdpWindow(self.machine, self.vm_ip)

    def local_btn_remoteapp_clicked_cb(self, widget):
        LocalRemoteWindow(self.machine, self.vm_ip)

    def on_remote_selection_changed(self, widget):
        model, treeiter = widget.get_selected()
        if treeiter is not None:
            data = model.get_value(treeiter, 1)
            self.connect_select = data

    def update_remote(self, widget):
        self.context.list_store_remote.clear()
        self.context.start_update()

    def delete_connect(self, widget):
        Settings().deleteConnect(self.connect_select)
        self.connect_select = None
        self.context.list_store_remote.clear()
        self.context.start_update()

    def remote_btn_vrdp_clicked_cb(self, widget):
        RemoteVrdpWindow(self.connect_select, self.context)

    def remote_btn_rdp_clicked_cb(self, widget):
        RemoteRdpWindow(self.connect_select, self.context)

    def remote_btn_remoteapp_clicked_cb(self, widget):
        RemoteRemoteWindow(self.connect_select, self.context)

    def btn_vbox_config_clicked_cb(self, widget):
        vm = ConfigVmWindow(self.machine)
        ConfigVmWindow(vm)

    def set_button_visible(self, state):
        self.btn_turn_on.set_sensitive(not state)
        self.btn_turn_off.set_sensitive(state)
        self.btn_reboot.set_sensitive(state)
        self.btn_save_state.set_sensitive(state)


class BtnController:
    def __init__(self, context):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")
