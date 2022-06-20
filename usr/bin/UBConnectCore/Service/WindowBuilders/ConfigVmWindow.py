import gettext
import locale
import subprocess
from os.path import exists

import gi
from UBConnectCore.Service.WindowBuilders.Conf.AddUsb import AddUsb
from UBConnectCore.Service.WindowBuilders.Conf.Dialogs import DialogSuccess
from UBConnectCore.Service.WindowBuilders.Conf.dialog_delete import DialogDelete

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

translate = gettext.translation("ubconnect", '/usr/share/locale', fallback=True)
i18n = translate.gettext

class UsbDevice:
    def __init__(self, index, active, filter_name, vendor_id, product_id, product_name):
        self.index = index
        self.active = active
        self.filter_name = filter_name
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.product_name = product_name


class ConfigVmWindow:
    def __init__(self, vm):
        self.language_sys = locale.getdefaultlocale()
        translate.install()

        self.vmthis = vm
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")
        self.login = self.builder.get_object("cvm_entry_login")
        self.password = self.builder.get_object("cvm_entry_password")
        self.cvm_entry_port = self.builder.get_object("cvm_entry_port")
        self.cvm_entry_port.connect("changed", self.ok_port)
        self.remote_access = self.builder.get_object("cvm_cb_remote_access")
        self.second_win = self.builder.get_object("configvm")
        self.usb_tv = self.builder.get_object("cvm_usb_tv")
        self.folders_tv = self.builder.get_object("cvm_tv_sharedfolders")
        self.cvm_btn_port = self.builder.get_object("cvm_btn_port")
        self.autorun_cmb = self.builder.get_object("cvm_cmb_run_type")
        self.autorun_check = self.builder.get_object("cvm_cb_autorun")
        self.auth_type_cmb = self.builder.get_object("auth_cmb")
        self.brige = self.builder.get_object("cvm_rb_bridge")
        self.nat = self.builder.get_object("cvm_rb_nat")

        self.Direct_TreeView_USB_List = Gtk.ListStore(bool, str, str, str, int)
        self.dd = self
        self.builder.connect_signals(EventHandler(self))
        self.tv_gener()
        self.usb_tv_gener()
        self.second_win.show()
        self.autorun_init()
        self.net_load()

        self.update_translation()

    def ok_port(self, widget):
        entry = widget.get_text()
        if entry != "":
            temp = entry[-1]
            if not temp.isdigit():
                widget.set_text(entry[0:-1])

    def net_load(self):
        if(subprocess.getstatusoutput(f"VBoxManage showvminfo \"{self.vmthis}\" | grep \"Bridged Interface\"")[0] == 0):
            self.brige.set_active(True)
        else:
            self.nat.set_active(True)

        if(subprocess.getoutput(f"VBoxManage showvminfo \"{self.vmthis}\" | grep \"Authentication type:\"").__contains__("null")):
            self.auth_cmb.set_active_id("0")
        else:
            self.auth_cmb.set_active_id("1")

    def autorun_init(self):
        self.autorun_check.set_active(False)
        store = Gtk.ListStore(int, str)
        cell = Gtk.CellRendererText()
        store.append([0, i18n("After system start")])
        store.append([1, i18n("After user login")])
        self.autorun_cmb.set_model(store)
        self.autorun_cmb.set_active(0)
        self.autorun_cmb.pack_start(cell, True)
        self.autorun_cmb.add_attribute(cell, "text", 1)
        username = subprocess.getoutput("whoami")
        home = subprocess.getoutput("echo $HOME")
        temp = subprocess.getoutput(f"ls {home}/.config/systemd/user/default.target.wants/")
        check_autorun = f"ubconnect@{self.vmthis}" in temp.replace("\\x20", " ")
        if check_autorun:
            self.autorun_cmb.set_active(0)
        if not check_autorun:
            self.autorun_cmb.set_active(1)
            check_autorun = exists(f"{home}/.config/autostart/ubconnect_{self.vmthis}.desktop")

        self.autorun_check.set_active(check_autorun)
        # temp = subprocess.getoutput(
        #     f"ls $HOME/.config/systemd/user/default.target.wants/ | grep ubconnect@{self.vmthis}.service")
        # print(temp)
        # if len(temp) != 0 and temp.find("такого файла или каталога") == -1:
        #     self.autorun_check.set_active(True)
        #     self.autorun_cmb.set_active(0)
        # home = subprocess.getoutput("echo $HOME")
        # if exists(f"{home}/.config/autostart/ubconnect_{self.vmthis}.desktop"):
        #     self.autorun_check.set_active(True)
        #     self.autorun_cmb.set_active(1)

        self.auth_cmb = self.builder.get_object("auth_cmb")
        self.auth_cmb.append("0", i18n("Without authorization"))
        self.auth_cmb.append("1", i18n("External"))
        self.auth_cmb.set_active_id("0")

    def fill_tv_usb(self):
        i = 0
        while i < len(self.vmthis.usb_device_filters.device_filters):
            self.list_usb.append([self.vmthis.usb_device_filters.device_filters[i].active,
                                  self.vmthis.usb_device_filters.device_filters[i].name])
            i += 1

    def usb_tv_gener(self):
        self.list_usb = Gtk.ListStore(bool, str)
        text_renderer = Gtk.CellRendererText()
        bool_renderer = Gtk.CellRendererToggle()

        ccol1 = Gtk.TreeViewColumn(title=i18n("Active"), cell_renderer=bool_renderer, active=0)
        ccol2 = Gtk.TreeViewColumn(title=i18n("Device"), cell_renderer=text_renderer, text=1)

        self.usb_tv.append_column(ccol1)
        self.usb_tv.append_column(ccol2)
        self.usb_tv.set_model(self.list_usb)

        self.fill_tv_usb()

    def fill_tv_folders(self):
        i = 0
        while i < len(self.vmthis.shared_folders):
            self.list_fold.append([self.vmthis.shared_folders[i].name, self.vmthis.shared_folders[i].host_path,
                                   self.vmthis.shared_folders[i].writable, self.vmthis.shared_folders[i].auto_mount,
                                   self.vmthis.shared_folders[i].auto_mount_point])
            i += 1

    def tv_gener(self):
        self.list_fold = Gtk.ListStore(str, str, 'gboolean', 'gboolean', str)
        text_renderer = Gtk.CellRendererText()
        bool_renderer = Gtk.CellRendererToggle()

        self.col1 = Gtk.TreeViewColumn(title=i18n("Name"), cell_renderer=text_renderer, text=0)
        self.col2 = Gtk.TreeViewColumn(title=i18n("Path"), cell_renderer=text_renderer, text=1)
        self.col3 = Gtk.TreeViewColumn(title=i18n("Access"), cell_renderer=bool_renderer, active=2)
        self.col4 = Gtk.TreeViewColumn(title=i18n("Automount"), cell_renderer=bool_renderer, active=3)
        self.col5 = Gtk.TreeViewColumn(title=i18n("Mount point"), cell_renderer=text_renderer, text=4)

        self.folders_tv.append_column(self.col1)
        self.folders_tv.append_column(self.col2)
        self.folders_tv.append_column(self.col3)
        self.folders_tv.append_column(self.col4)
        self.folders_tv.append_column(self.col5)
        self.folders_tv.set_model(self.list_fold)

        self.fill_tv_folders()

        print("len", len(self.vmthis.usb_device_filters.device_filters))

    def update_translation(self):
        self.builder.get_object("lblAutostartSettingsConfigVM").set_label(i18n("VM autorun settings"))
        self.builder.get_object("lblAutostartconfigvm").set_label(i18n("Autorun"))
        self.builder.get_object("lblAutostartTypeConfigVM").set_label(i18n("Autorun type:"))
        self.builder.get_object("lblConnServerSettingsConfigVM").set_label(i18n("Set property connection"))
        self.builder.get_object("lblPortConfigVM").set_label(i18n("Port:"))
        self.builder.get_object("lblTimeoutConfigVM").set_label(i18n("Timeout:"))
        self.builder.get_object("lblMultiuserAccessconfigvm").set_label(i18n("Multi-User Remote Access"))
        self.builder.get_object("lblAuthConfigVM").set_label(i18n("Authorization:"))
        self.builder.get_object("lblLoginConfigVM").set_label(i18n("Login:"))
        self.builder.get_object("lblPasswordConfigVM").set_label(i18n("Password:"))
        self.builder.get_object("lblConnTypeSettingsConfigVM").set_label(i18n("Setting the network connection type"))
        self.builder.get_object("lblMostconfigvm").set_label(i18n("Bridge"))
        self.builder.get_object("lblUsbDevicesConfigVM").set_label(i18n("USB-devices"))
        self.builder.get_object("lblSharedCatalogsConfigVM").set_label(i18n("Shared catalogs"))
        self.builder.get_object("lblPortsForwardingconfigvm").set_label(i18n("Port forwarding"))
        self.builder.get_object("lblCancelconfigvm").set_label(i18n("Cancel"))
        self.builder.get_object("lblSaveSettconfigvm").set_label(i18n("Save settings"))
        self.builder.get_object("configvm").set_title(i18n("Virtual machine settings (VirtualBox)"))

class EventHandler:

    def __init__(self, context):
        self.context = context
        self.vm = self.context.vmthis
        self.auth_type_cmb = self.context.autorun_cmb
        self.auth_type = "0"

    def save_vrde_settings(self):

        login = self.context.login.get_text()
        password = self.context.password.get_text()
        port = self.context.cvm_entry_port.get_text()
        if f"{self.vm}" not in subprocess.getoutput(f"VBoxManage list runningvms"):
            subprocess.getoutput(f"VBoxManage modifyvm \"{self.vm}\" --vrdeport {port}")
            if self.auth_type == "0":
                subprocess.getoutput(f"VBoxManage modifyvm \"{self.vm}\" --vrdeauthtype null")
            else:
                subprocess.getoutput(f"VBoxManage setproperty vrdeauthlibrary \"VBoxAuthSimple\"")
                subprocess.getoutput(f"VBoxManage modifyvm \"{self.vm}\" --vrdeauthtype external")
                passhash = subprocess.getoutput(f"VBoxManage internalcommands passwordhash \"{password}\"")
                subprocess.getoutput(
                    f"VBoxManage setextradata \"{self.vm}\" \"VBoxAuthSimple/users/{login}\" \"{passhash}\"")
        else:
            dialog = Gtk.MessageDialog(
                transient_for=self.context.second_win,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=i18n("Error"),
            )
            dialog.format_secondary_text(i18n("To save changes, you must turn off the virtual machine"))
            dialog.run()
            dialog.destroy()



    def autorun_change(self):
        if self.context.autorun_check.get_active():
            iter = self.context.autorun_cmb.get_active_iter()
            if iter is not None:
                model = self.context.autorun_cmb.get_model()
                row_id, color = model[iter][:2]
                autorun_type = row_id
                username = subprocess.getoutput("whoami")
                if autorun_type == 0:
                    subprocess.getoutput(f"/usr/bin/UBConnectCore/scripts/autorun.sh --vmname \"{self.vm}\" --delete")
                    temp = subprocess.getoutput(
                        f"/usr/bin/UBConnectCore/scripts/autorun.sh --vmname \"{self.vm}\" --onsystem --user \"{username}\"")
                    print(temp)
                if autorun_type == 1:
                    subprocess.getoutput(f"/usr/bin/UBConnectCore/scripts/autorun.sh --vmname \"{self.vm}\" --delete")
                    subprocess.getoutput(
                        f"/usr/bin/UBConnectCore/scripts/autorun.sh --vmname \"{self.vm}\" --onlogin --user \"{username}\"")
        else:
            subprocess.getoutput(f"/usr/bin/UBConnectCore/scripts/autorun.sh --vmname \"{self.vm}\" --delete")

    def get_iter_last(self, mdl):
        itr = mdl.get_iter_first()
        last = None
        while itr:
            last = itr
            itr = mdl.iter_next(itr)
        return last

    def close_cfg_vm(self, test):
        self.context.second_win.destroy()

    def cvm_btn_add_sharedfolder_clicked_cb(self, widget):
        from UBConnectCore.Service.WindowBuilders.Conf.AddFolder import AddFolder
        # self.cont = self.context
        # self.conf = AddFolder(self.cont)
        AddFolder(self)

    def on_selection_changed_fold(self, widget):
        model, iter = widget.get_selected()
        self.fold_name = model.get_value(iter, 0)
        self.fold_path = model.get_value(iter, 1)
        self.fold_access = model.get_value(iter, 2)
        self.fold_auto_mount = model.get_value(iter, 3)
        self.fold_auto_mount_point = model.get_value(iter, 4)

    def cvm_btn_delete_sharedfolder_clicked_cb(self, widget):
        self.context.list_fold.clear()
        subprocess.getoutput('VBoxManage sharedfolder remove "' + str(self.vm) + '" --name "' + self.fold_name + '"')
        self.context.fill_tv_folders()

    def cvm_btn_config_sharedfolder_clicked_cb(self, widget):
        from UBConnectCore.Service.WindowBuilders.Conf.ChangeFolder import ChangeFolder
        # cont = self.context
        # conf = ChangeFolder(cont)
        ChangeFolder(self)

    def cvm_btn_add_usb_clicked_cb(self, widget):
        dialog = AddUsb()
        try:
            lastid = int(subprocess.getoutput(f"VBoxManage showvminfo \"{self.context.vmthis}\" | grep Index | awk -F ':                       ' '{{print $2}}'").split("\n")[-1]) + 1
        except:
            lastid = 0

        if dialog.response_type == Gtk.ResponseType.OK:
            for el in dialog.get_result():
                #print("" + self.Select_USB)
                print(dialog.get_result())
                last_iter = self.get_iter_last(self.context.Direct_TreeView_USB_List)
                id = lastid if last_iter is None else self.context.Direct_TreeView_USB_List[last_iter][4] + 1

                subprocess.getoutput(
                    f"VBoxManage usbfilter add {id} --target \"{str(self.context.vmthis)}\" --name '{el[1]}' --action hold --vendorid {el[3]} --productid {el[2]}")

                self.context.Direct_TreeView_USB_List.append([el[0], el[1], el[2], el[3], id])

            dialog = Gtk.MessageDialog(
                transient_for=self.context.second_win,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=i18n("Success!"),
            )
            dialog.format_secondary_text(i18n("USB device added successfully"))

            self.context.list_usb.clear()
            self.context.fill_tv_usb()
        return

    def on_selection_changet_fold(self, select):

        self.model, self.treeiter = select.get_selected()
        if self.treeiter is not None:
            rownumobj = self.model.get_path(self.treeiter)
            self.row = int(rownumobj.to_string())

        self.usb_name = self.vm.usb_device_filters.device_filters[self.row].name
        self.usb_vend = self.vm.usb_device_filters.device_filters[self.row].vendor_id
        self.usb_prod_id = self.vm.usb_device_filters.device_filters[self.row].product_id
        self.usb_active = self.vm.usb_device_filters.device_filters[self.row].active
        print(self.usb_name)
        print(self.usb_vend)
        print(self.usb_prod_id)
        # if(self.row - 1 >= 0):
        #     self.usb_name_up = self.vm.usb_device_filters.device_filters[self.row-1].name
        #     self.usb_vend_up = self.vm.usb_device_filters.device_filters[self.row-1].vendor_id
        #     self.usb_prod_id_up = self.vm.usb_device_filters.device_filters[self.row-1].product_id
        #     self.usb_active_up = self.vm.usb_device_filters.device_filters[self.row-1].active
        # if(self.row + 1 <= len(self.context.list_usb)):
        #     self.usb_name_down = self.vm.usb_device_filters.device_filters[self.row+1].name
        #     self.usb_vend_down = self.vm.usb_device_filters.device_filters[self.row+1].vendor_id
        #     self.usb_prod_id_down = self.vm.usb_device_filters.device_filters[self.row+1].product_id
        #     self.usb_active_down = self.vm.usb_device_filters.device_filters[self.row+1].active




    def cvm_btn_delete_usb_clicked_cb(self, widget):
        vm = str(self.context.vmthis)
        print(vm)

        if self.treeiter is not None:
            dialog = DialogDelete(self.context.second_win, self.model[self.treeiter][1])
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                self.context.list_usb.remove(self.treeiter)
                subprocess.getoutput(f"VBoxManage usbfilter remove {self.row} --target \"{vm}\"")
                dialog.destroy()

            if response == Gtk.ResponseType.CANCEL:
                dialog.destroy()

        self.context.list_usb.clear()
        self.context.fill_tv_usb()

    def cvm_btn_move_cursor_up_clicked_cb(self, widget):
        vm = str(self.context.vmthis)
        flag = self.row - 1
        print(vm)
        print(self.usb_name)
        print(self.usb_vend)
        print(self.usb_prod_id)
        if flag >= 0:
            if self.treeiter is not None:
                temp1 = subprocess.getoutput(f"VBoxManage usbfilter remove {self.row} --target \"{vm}\"")
                temp2 = subprocess.getoutput(
                    f"VBoxManage usbfilter add {flag} --target \"{str(self.context.vmthis)}\" --name '{self.usb_name}'"
                    f" --action hold --vendorid {self.usb_vend} --productid {self.usb_prod_id}")


        self.context.list_usb.clear()
        self.context.fill_tv_usb()

    def cvm_btn_move_cursor_down_clicked_cb(self, widget):
        vm = str(self.context.vmthis)
        flag = self.row + 1
        print(vm)

        if flag < len(self.context.vmthis.usb_device_filters.device_filters):
            if self.treeiter is not None:
                subprocess.getoutput(f"VBoxManage usbfilter remove {self.row} --target \"{vm}\"")
                subprocess.getoutput(
                    f"VBoxManage usbfilter add {flag} --target \"{str(self.context.vmthis)}\" --name '{self.usb_name}'"
                    f" --action hold --vendorid {self.usb_vend} --productid {self.usb_prod_id}")

        self.context.list_usb.clear()
        self.context.fill_tv_usb()


    def cvm_btn_rec_clicked_cb(self, widget):
        # try:
        last_iter = self.get_iter_last(self.context.Direct_TreeView_USB_List)
        id = 0 if last_iter is None else self.context.Direct_TreeView_USB_List[last_iter][4] + 1
        newFilterName = i18n("New filter")
        subprocess.getoutput(
            f"VBoxManage usbfilter add {id} --target {str(self.context.vmthis)} --name '{newFilterName} {id}'  --action hold")
        self.context.Direct_TreeView_USB_List.append([True, f'{newFilterName} {id}', '', '', id])
        dialog = Gtk.MessageDialog(
            transient_for=self.context.second_win,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=i18n("Success!"),
        )
        dialog.format_secondary_text(i18n("USB device added successfully"))
        dialog.run()
        dialog.destroy()
        # except:
        self.context.list_usb.clear()
        self.context.fill_tv_usb()
        return

    def cvm_btn_port_clicked_cb(self, btn):
        from UBConnectCore.Service.WindowBuilders.Conf.PortsWindow import PortsWindow
        PortsWindow(self)

    @staticmethod
    def usb_empty_filter(index, name_vm):
        newFilterName = i18n("New filter")
        subprocess.getoutput(
            f"VBoxManage usbfilter add {index} --target {name_vm} --name '{newFilterName} {index}'  --action hold")

    def cvm_btn_save_config_clicked_cb(self, widget):
        if(self.auth_type != "0"):
            if(self.context.login.get_text() and self.context.password.get_text()):
                self.save_vrde_settings()
            else:
                dialog = Gtk.MessageDialog(
                    transient_for=self.context.second_win,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text=i18n("Error"),
                )
                dialog.format_secondary_text(i18n("Enter login and password!"))
                dialog.run()
                dialog.destroy()
                return

        if self.context.remote_access.get_active() is True:
            subprocess.getoutput(f"VBoxManage modifyvm \"{self.vm}\" --vrdemulticon on")
        else:
            subprocess.getoutput(f"VBoxManage modifyvm \"{self.vm}\" --vrdemulticon off")

        if (self.context.nat.get_active):
            subprocess.getoutput(f"VBoxManage modifyvm \"{self.vm}\" --nic1 nat")
        else:
            subprocess.getoutput(f"VBoxManage modifyvm \"{self.vm}\" --nic1 bridged")

        self.autorun_change()

        DialogSuccess("Settings saved").show()

    def on_cvm_rb_nat_toggled(self, radio):
        self.context.cvm_btn_port.set_sensitive(radio.get_active())

    def cvm_cb_autorun_toggled_cb(self, checkbox):
        self.context.autorun_cmb.set_sensitive(checkbox.get_active())

    def cvm_cmb_auth_changed_cb(self, combobox):
        self.context.login.set_sensitive(combobox.get_active_id() == "1")
        self.context.password.set_sensitive(combobox.get_active_id() == "1")
        self.auth_type = combobox.get_active_id()

    def cvm_btn_show_pass_clicked_cb(self, button):
        self.context.password.set_visibility(not self.context.password.get_visibility())


if __name__ == '__main__':
    main = ConfigVmWindow()
    Gtk.main()
