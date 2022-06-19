#! /usr/bin/env bash

helptext="
\nПри настройки автозапуска \"после старта системы\", скрипт необходимо выполнить через sudo 
\nПри настройки автозапуска \"после авторизации пользователя\", sudo не использовать 
\n--vmname - имя виртуальной машины, указывать в ковычках
\n--onlogin - указать для запуска после авторизации пользователя в системе
\n--onsystem - указать для запуска после включения системы
\n--user - указать имя пользователя (для запуска после старта системы)
\n--delete - указать для удаления машины с автозапуска. Пример ./autostart.sh --vmname \"windows 7\" --delete
\n--help - вывод справки
\nПример использования: \n
 \* sudo ./autostart.sh --vmname \"windows 7\" --onsystem --user superadmin (при старте системы)\n
 \* ./autostart.sh --vmname \"windows 7\" --onlogin --user superadmin (после авторизации пользователя)\n"


while [ -n "$1" ]
do
    case "$1" in
        --onsystem) 
            type="onsystem"
             echo "onsystem";;
            
        --onlogin) 
            type="onlogin"
             echo "onlogin";;

        --vmname) 
            vmname="$2"
            echo "$vmname"
            shift;;

        --help)
            echo -en $helptext;;
        --user)
            username="$2"
            shift;;
        --delete)
            delete="True";;
        
        *) 
            echo "$1 неверный параметр "
            echo -en $helptext
            exit;;
    esac
    shift
done
deleteVM(){
    echo "$vmname"
    systemctl --machine="$username"@.host --user disable ubconnect@"$vmname".service
    rm "$HOME/.config/autostart/ubconnect_$vmname.desktop"
    systemctl --machine=superadmin@.host --user daemon-reload
    exit
}
if [ "$delete" == "True" ];
then
	deleteVM
fi

pathForTemplate="/usr/lib/systemd/user/ubconnect@.service"

initialTemplate(){
    systemctl --machine="$username"@.host --user daemon-reload
    systemctl --machine="$username"@.host --user enable --now ubconnect@"$vmname".service
}

regOnSystem(){
if [ -f "$pathForTemplate" ];
then
    initialTemplate
else
    echo "Юнит автозапуска не найден! Создаю новый юнит...\n"
   echo "Description=Virtual Box Guest %I
After=network.target vboxdrv.service virtualbox.service
Before=runlevel2.target shutdown.target
[Service]
Type=forking
Restart=no
TimeoutSec=5min
IgnoreSIGPIPE=no
KillMode=process
GuessMainPID=no
RemainAfterExit=yes
ExecStart=/usr/bin/VBoxManage startvm '%I' --type headless
ExecStop=/usr/bin/VBoxManage controlvm '%I' acpipowerbutton
[Install]
WantedBy=default.target" > "$pathForTemplate"
    initialTemplate
fi
}

regOnLogin(){
    username=$(whoami)
    if [ -d "$HOME/.config/autostart" ];
    then
    fullPath="$HOME/.config/autostart/ubconnect_$vmname.desktop"
    echo "$fullPath"
    echo "[Desktop Entry]
Encoding=UTF-8
Version=0.9.4
Type=Application
Name=$vmname
Comment=Автозапуск виртуальной машины $vmname
Exec=VBoxHeadless --startvm '$vmname'
OnlyShowIn=XFCE;
RunHook=0
StartupNotify=false
Terminal=false
Hidden=false" > "$fullPath"
chmod +x "$fullPath"
    else
        mkdir "$HOME/.config/autostart"
    fi
}

if [ "$type" == "onsystem" ];
then
    regOnSystem 
fi
if [ "$type" == "onlogin" ];
then
    regOnLogin 
fi