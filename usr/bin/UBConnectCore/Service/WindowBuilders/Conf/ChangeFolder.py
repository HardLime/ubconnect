import gettext
import locale
import subprocess
import tkinter
from tkinter import filedialog

import gi
import subprocess

import virtualbox as virtualbox

from UBConnectCore.Service.WindowBuilders.ConfigVmWindow import ConfigVmWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

translate = gettext.translation("ubconnect", '/usr/share/locale', fallback=True)
i18n = translate.gettext

class ChangeFolder:
    def __init__(self, conf):
        self.language_sys = locale.getdefaultlocale()
        translate.install()

        self.fold = conf
        self.vm = conf.vm
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/usr/share/ubconnect/ui/ubconnect.glade")
        self.Add_fold_win = self.builder.get_object("addfolder")
        self.builder.connect_signals(EventHandler(self))
        self.Path = self.builder.get_object("addfolder_entry_path")
        self.Folder = self.builder.get_object("addfolder_entry_folder")
        self.Writable = self.builder.get_object("addfolder_cb_ro")
        self.Automount = self.builder.get_object("addfolder_cb_automount")
        self.Mount_point = self.builder.get_object("addfolder_entry_mount_point")
        # print("sss", self.vmthis)
        print('sss', self.fold.context.vmthis)
        self.changefolder_fill_form(self)
        self.Add_fold_win.show()

        self.update_translation()

    def changefolder_fill_form(self, cont):
        self.Folder.set_text(self.fold.fold_name)
        self.Path.set_text(self.fold.fold_path)
        self.Writable.set_active(self.fold.fold_access)
        self.Automount.set_active(self.fold.fold_auto_mount)
        self.Mount_point.set_text(self.fold.fold_auto_mount_point)

        self.fold_to_del = self.fold.fold_name

    def update_translation(self):
        self.builder.get_object("lblPathAddFolder").set_label(i18n("Path:"))
        self.builder.get_object("lblFolderNameAddFolder").set_label(i18n("Folder name:"))
        self.builder.get_object("lblReadonlyaddfolder").set_label(i18n("Read Only"))
        self.builder.get_object("lblAutoMountaddfolder").set_label(i18n("Automount"))
        self.builder.get_object("lblMountPointAddFolder").set_label(i18n("Mount point:"))
        self.builder.get_object("lblCanceladdfolder").set_label(i18n("Cancel"))
        self.builder.get_object("lblAddaddfolder").set_label(i18n("Save"))
        self.builder.get_object("addfolder").set_title(i18n("Edit shared folder settings"))


class EventHandler:

    def __init__(self, context):
        self.context = context

    def addfolder_btn_cancel_clicked_cb(self, widget):
        self.context.Add_fold_win.destroy()

    def addfolder_btn_show_clicked_cb(self, test):
        self.context.changefolder_fill_form(self.context.fold.fold_name)
        root = tkinter.Tk()
        root.withdraw()
        self.context.path = filedialog.askdirectory(parent=root, initialdir="/", title=i18n("Please select a directory"))
        self.context.Path.set_text(self.context.path)
        self.context.folder = self.context.path.split('/')
        self.context.Folder.set_text(self.context.folder[len(self.context.folder) - 1])

    def addfolder_btn_add_clicked_cb(self, test):
        self.VM = self.context.vm


        subprocess.getoutput('VBoxManage sharedfolder remove "' + str(self.VM) + '" --name "' + self.context.fold_to_del + '"')
        print('VBoxManage sharedfolder remove "' + str(self.VM) + '" --name "' + self.context.fold_to_del + '"')

        self.RO = ""
        self.AM = ""
        self.AMP = ""

        self.path = self.context.Path.get_text()
        self.name = self.context.Folder.get_text()
        self.writable = self.context.Writable.get_active()
        self.automount = self.context.Automount.get_active()
        self.automount_p = self.context.Mount_point.get_text()

        if self.writable is False:
            self.RO = ' --readonly'
        if self.automount is True:
            self.AM = ' --automount'
        if self.automount_p is not "":
            self.AMP = ' --auto-mount-point="' + self.automount_p + '"'

        subprocess.getoutput('VBoxManage sharedfolder add "' + str(self.VM) + '" --name "' + self.name +
                             '" --hostpath "' + self.path + '"' + self.RO + self.AM + self.AMP)# + ' --transient')

        print('VBoxManage sharedfolder add "' + str(self.VM) + '" --name "' + self.name + '" --hostpath "' +
              self.path+'"' + self.RO + self.AM, self.AMP)

        print(self.path)
        print(self.name)
        print(self.writable)
        print(self.automount)
        print(self.automount_p)

        self.context.fold.context.list_fold.clear()
        self.context.Add_fold_win.destroy()
        self.context.fold.context.fill_tv_folders()


if __name__ == '__main__':
    main = ChangeFolder()
    Gtk.main()