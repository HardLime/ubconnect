import subprocess
#
# import private as private
# import self as self


class VirtualMachine:
    def __init__(self, vm_name, vm_hash):
        self.vm_name = vm_name
        self.vm_hash = vm_hash

    def getname(self):
        return self.vm_name

    def gethash(self):
        return self.vm_hash + ""


class SharedFolder:
    def __init__(self, folder_name, folder_path, folder_access, folder_automount, folder_mount_point):
        self.folder_name = folder_name
        self.folder_path = folder_path
        self.folder_access = folder_access
        self.folder_automount = folder_automount
        if folder_mount_point == "":
            self.folder_mount_point = "Auto"
        else:
            self.folder_mount_point = folder_mount_point

    def get_folder_access(self):
        if self.folder_access == "RO":
            return "--readonly "
        else:
            return ""

    def get_folder_automount(self):
        if self.folder_automount:
            return "--automount "
        else:
            return ""

    def get_folder_mount_point(self):
        if self.folder_mount_point == "Auto":
            return ""
        else:
            return f" --auto-mount-point={self.folder_mount_point}"


class SharedFolders:
    def __init__(self, name):
        self.folder_names = subprocess.getoutput(
            f"v=$(VBoxManage showvminfo {name} |grep \"Host path:\");awk -F \"\'|\'\" \'{{print $2}}\' <<< $v;").split("\n")
        self.folder_patches = subprocess.getoutput(
            f"v=$(VBoxManage showvminfo {name} |grep \"Host path:\");awk -F \"\'|\'\" \'{{print $4}}\' <<< $v;").split("\n")
        self.folder_points = subprocess.getoutput(
            f"v=$(VBoxManage showvminfo {name} |grep \"Host path:\");awk -F \"\'|\'\" \'{{print $6}}\' <<< $v;").split("\n")
        self.folder_configs = subprocess.getoutput(
            f"v=$(VBoxManage showvminfo {name} |grep \"Host path:\");awk -F \"\'|\'\" \'{{print $5}}\' <<< $v;").split("\n")
        self.shared_folders_list = list()
        self.shared_folders_fill()

    def shared_folders_fill(self):
        for i in range(len(self.folder_names)):
            temp_readonly = "RW"
            temp_automount = False
            if "readonly" in self.folder_configs[i]:
                temp_readonly = "RO"
            if "auto-mount" in self.folder_configs[i]:
                temp_automount = True
            temp = SharedFolder(self.folder_names[i], self.folder_patches[i], temp_readonly, temp_automount,
                                self.folder_points[i])
            self.shared_folders_list.append(temp)


class VirtualMachines:
    def __init__(self):
        self.vm_name_list = subprocess.getoutput(
            "v=$(VBoxManage list vms); awk -F \'\"|\" {|}\' \'{print $2}\' <<< $v").split("\n")
        self.vm_hash_list = subprocess.getoutput(
            "v=$(VBoxManage list vms); awk -F \'\"|\" {|}\' \'{print $3}\' <<< $v").split("\n")
        self.vm_list = list()
        self.vm_fill()

    def vm_fill(self):
        for i in range(len(self.vm_name_list)):
            temp = VirtualMachine(self.vm_name_list[i], self.vm_hash_list[i])
            self.vm_list.append(temp)

    def get_name(self, vm_id):
        temp = self.vm_list[vm_id]
        return temp.getname()

    def get_hash(self, vm_id):
        temp = self.vm_list[vm_id]
        return temp.gethash()

    def add_usb(self, filter_id, vm, action, usb):
        if vm is not None:
            subprocess.getoutput(
                "VBoxManage usbfilter add " + filter_id + " --target " + vm.gethash() + " --action " + action + " --vendorid " + usb.vendor_id + " --productid " + usb.product_id)
        else:
            subprocess.getoutput(
                "VBoxManage usbfilter add " + filter_id + " --action " + action + " --vendorid " + usb.vendor_id + " --productid " + usb.product_id)

    def remove_usb(self, filter_id, vm):
        if vm is not None:
            subprocess.getoutput("VBoxManage usbfilter remove " + filter_id + " --target " + vm.gethash())
        else:
            subprocess.getoutput("VBoxManage usbfilter remove " + filter_id)

    def add_shared_folder(self, shared_folder, vm):
        subprocess.getoutput(
            f"VBoxManage sharedfolder add {vm.gethash()} --name {shared_folder.folder_name} --hostpath {shared_folder.folder_path} {shared_folder.get_folder_access()} {shared_folder.get_folder_automount()} {shared_folder.get_folder_mount_point()}")

    def set_multicon(self, vm, typecon):
        if typecon:
            subprocess.getoutput(f"VBoxManage modifyvm {vm.gethash()} --vrdemulticon on")
        else:
            subprocess.getoutput(f"VBoxManage modifyvm {vm.gethash()} --vrdemulticon off")

    def set_shared_buffer(self, vm, type_shared):
        if type_shared == "disabled":
            subprocess.getoutput(f"VBoxManage modifyvm {vm.gethash()} --clipboard-mode {type_shared}")
        if type_shared == "hosttoguest":
            subprocess.getoutput(f"VBoxManage modifyvm {vm.gethash()} --clipboard-mode {type_shared}")
        if type_shared == "guesttohost":
            subprocess.getoutput(f"VBoxManage modifyvm {vm.gethash()} --clipboard-mode {type_shared}")
        if type_shared == "bidirectional":
            subprocess.getoutput(f"VBoxManage modifyvm {vm.gethash()} --clipboard-mode {type_shared}")


class DirectConnection:

    def __init__(self, login, password, ip, port, timeout, usb, printer):
        self.login = login
        self.password = password
        self.ip = ip
        self.port = port
        self.timeout = timeout

        if usb:
            self.usb = "-r usb"
        else:
            self.usb = ""

        if printer is not None:
            self.printer = "-r printer:" + printer
        else:
            self.printer = ""

    def create_desktop(self, name, path):
        subprocess.getoutput(
            f"echo \"[Desktop Entry]\nType=Application\nCategories=System;Utility;\nExec=rdesktop-vrdp -u \'{self.login}\' -p \'{self.password}\' {self.ip}:{self.port} {self.usb} {self.printer}\n"
            f"Terminal=true\nStartupNotify=true\nName={name}\nName[ru]={name}\n"
            "Comment=Start virtual machine\nComment[ru]=Запуск виртуальной машины\nNoDisplay=false\n"
            f"Hidden=false \" > /home/superadmin/'Рабочий стол'/{name}.desktop; PASSWD=$(zenity --password --title=\"Введите пароль\"); echo $PASSWD | sudo -S chmod +x '{path}'{name}.desktop")


class UsbDevice:
    def __init__(self, vendor_id, product_id, product_name):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.product_name = product_name


class UsbDevices:
    def __init__(self):
        self.usb_vendorId_list = subprocess.getoutput(
            "v=$(VBoxManage list usbhost | grep VendorId: );b=$(awk -F \'(\' \'{print $2}\' <<< $v);awk -F \')\' \'{"
            "print $1}\' <<<$b").split(
            "\n")
        self.usb_productId_list = subprocess.getoutput(
            "v=$(VBoxManage list usbhost | grep ProductId: );b=$(awk -F \'(\' \'{print $2}\' <<< $v);awk -F \')\' \'{"
            "print $1}\' <<<$b").split(
            "\n")
        self.usb_productName_list = subprocess.getoutput(
            "v=$(VBoxManage list usbhost | grep Product: );awk -F \':            \' \'{print $2}\' <<< $v").split("\n")
        self.usb_list = list()
        self.usb_device_fill()

    def usb_device_fill(self):
        for i in range(len(self.usb_productId_list)):
            temp = UsbDevice(self.usb_vendorId_list[i], self.usb_productId_list[i], self.usb_productName_list[i])
            self.usb_list.append(temp)

    def get_usb_list(self):
        return self.usb_list

    def get_usb(self, usb_id):
        return self.usb_list[usb_id]

