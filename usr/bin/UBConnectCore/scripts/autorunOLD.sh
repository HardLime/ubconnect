#!/bin/bash
systemPath="/etc/systemd/system/"
systemCopyPath="/memory/data/from/0/ublinux-data/rootcopy/etc/systemd/system/multi-user.target.wants"
filePrefics="ubc_"
fileExeption=".service"
user=$(whoami)

while [ -n "$1" ]
do
    case "$1" in
        --onsystem) 
            type="onsystem"
             echo "sys"
             ;;
            

        --onlogin) 
            type="onlogin"
             echo "log";;

        --vmhash) 
            vmhash="$2"
            echo "$vmhash"
            shift;;
        
        *) 
            echo "$1 неверный параметр "
            echo -en $helptext
            exit;;
    esac
    shift
done

createFileInRootCopy(){
    echo "fgdgdgg"
    if [ ! -d "$systemCopyPath" ];
    then
        echo "Нет нужного каталога, создаю"
        if [ ! -d "/memory/data/from/0/ublinux-data/rootcopy/etc" ]; 
        then
            echo "Создаю rootcopy/etc"
            mkdir "/memory/data/from/0/ublinux-data/rootcopy/etc"
        fi
        if [ ! -d "/memory/data/from/0/ublinux-data/rootcopy/etc/systemd" ]; 
        then
            echo "Создаю rootcopy/etc/systemd"
            mkdir "/memory/data/from/0/ublinux-data/rootcopy/etc/systemd"
        fi
        if [ ! -d "/memory/data/from/0/ublinux-data/rootcopy/etc/systemd/system" ]; 
        then
            echo "Создаю rootcopy/etc/systemd/system"
            mkdir "/memory/data/from/0/ublinux-data/rootcopy/etc/systemd/system"
        fi
        if [ ! -d "/memory/data/from/0/ublinux-data/rootcopy/etc/systemd/system/multi-user.target.wants" ]; 
        then
            echo "Создаю rootcopy/etc/systemd/system"
            mkdir "/memory/data/from/0/ublinux-data/rootcopy/etc/systemd/system/multi-user.target.wants"
        fi
        pathForLink="multi-user.target.wants/"
        echo "Копирую файлы юнита"
        cp "$systemPath$filePrefics$vmhash$fileExeption" "/memory/data/from/0/ublinux-data/rootcopy/etc/systemd/system/$filePrefics$vmhash$fileExeption"
        ln -s "$systemPath$filePrefics$vmhash$fileExeption" "/memory/data/from/0/ublinux-data/rootcopy/etc/systemd/system/multi-user.target.wants/$filePrefics$vmhash$fileExeption"
        
    else
        pathForLink="multi-user.target.wants/"
        echo "Копирую файлы юнита"
        cp "$systemPath$filePrefics$vmhash$fileExeption" "/memory/data/from/0/ublinux-data/rootcopy/etc/systemd/system/$filePrefics$vmhash$fileExeption"
        ln -s "$systemPath$filePrefics$vmhash$fileExeption" "/memory/data/from/0/ublinux-data/rootcopy/etc/systemd/system/multi-user.target.wants/$filePrefics$vmhash$fileExeption"
    fi
    
}

regOnSystem(){
    fullPath="$systemPath$filePrefics$vmhash$fileExeption"
    echo "Description=Virtual Box Guest $vmhash
After=network.target vboxdrv.service
Before=runlevel2.target shutdown.target
[Service]
User=$user
Group=vboxusers
Type=forking
Restart=no
TimeoutSec=5min
IgnoreSIGPIPE=no
KillMode=process
GuessMainPID=no
RemainAfterExit=yes
ExecStart=/usr/bin/VBoxManage startvm $vmhash --type headless
ExecStop=/usr/bin/VBoxManage controlvm $vmhash acpipowerbutton
[Install]
WantedBy=multi-user.target" > "$fullPath"
    unitName="$filePrefics$vmhash$fileExeption"
    systemctl daemon-reload
    systemctl enable $unitName

    createFileInRootCopy

}


regOnLogin(){
    fullPath="$HOME/.config/autostart/$filePrefics$vmhash.desktop"
    echo "$fullPath"
    echo "[Desktop Entry]
Encoding=UTF-8
Version=0.9.4
Type=Application
Name=$filePrefics$vmhash
Comment=Автозапуск виртуальной машины $vmhash
Exec='VBoxHeadless --startvm $vmhash'
OnlyShowIn=XFCE;
RunHook=0
StartupNotify=false
Terminal=false
Hidden=false" > "$fullPath"
echo $(zenity --password --title "Авторизация") | sudo -S chmod +x "$fullPath"
}




if [ "$type" == "onsystem" ];
then
    regOnSystem "$vmhash"
fi
if [ "$type" == "onlogin" ];
then
    regOnLogin "$vmhash"
fi

