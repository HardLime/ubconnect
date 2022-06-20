��          $      ,      8   S  A              helptext All values are specified with a space. Put paths and file names in quotes "path"
Parameters marked (boolean) are specified without values. (or not specified)

Connection options:
--ip - server address of type х.х.х.х
--port - server port
--domain - server domain
--login - guest OS username
--password - guest OS user password
--clientdisplay - run in full screen mode. (boolean)
--geometry - set the screen resolution manually. Example: --geometry 1920x1280
--color - set palette. Example --color 2
    Valid palette values:
    For xfreerdp
    1) high color 15 bit
    2) high color 16 bit
    3) true color 24 bit
    4) RemoteFX
    5) GFX progressive
    6) GFX AVC420 32bit
    7) GFX H264
    For rdesktop и vrdp
    1) high color 15 bit
    2) high color 16 bit
    3) true color 24 bit
    4) true color 32 bit
--mounthome - mount home directory (boolean)
--mountcatalog - mounting directory. Example --mountcatalog "/home/superadmin/Downloads"
--defaultprinter - forwarding the default printer. (boolean)
--allprinters - forwarding all printers registered in the system (boolean)
--printer - forwarding printer. Example --printer "My printer name"
--audio - forwarding sound and microphone. (boolean)
--certignore - ignoring certificate (boolean)

Selecting a connection mode:
--appstart - launch without desktop environment. Example --appstart "path/to/application" Do not specify option for mode with desktop environment
--remoteapp - run app in remoteapp mode (boolean)

Setting up a connection shortcut:
--windowtitle - set window title. Example --windowtitle "new window title"
--icon - specify the full path to the icon
--filepath - specify the save path. Example --filepath "/home/superadmin/Documents"
--name - name of desktop-file. Example --name "Virtual machine connection 1"

Selecting a connection client:
--xfreerdp - use Freerdp syntax (boolean)
--rdesktop - use rdesktop syntax (boolean)
--vrdp - use rdesktop-vrdp syntax (boolean)

Examples:
Connecting RDP:
* ubconnect --ip 192.168.1.1 --port 3389 --clientdisplay --name "Windows" --mounthome --printer "My printer" --xfreerdp
* ubconnect --login user --password 123 --ip 192.168.1.1 --name "Windows" --icon "ub_icon" --geometry 1920x1280 --printer "name" --color 1 --xfreerdp
* ubconnect --ip 192.168.1.1 --port 3389 --name "Windows XP" --mounthome --printer "My printer" --geometry 1920x1280 --rdesktop

Connecting RDP without desktop environment:
* ubconnect --login user --password 123 --ip 192.168.1.1 --port 3389 --name "Launch notepad" --appstart "notepad.exe" --xfreerdp (for Windows 7 and newer)
* ubconnect --login user --password 123 --ip 192.168.1.1 --port 3389 --name "Launch notepad" --appstart "notepad.exe" --rdesktop (for Windows XP)

Connecting VRDP:
* ubconnect --ip 192.168.1.1 --port 3389 --name "VrdpConnect" --mounthome --printer "My printer" --vrdp

Connecting RemoteApp:
* ubconnect --login user --password 123 --ip 192.168.1.1 --port 3389 --name "Notepad" --appstart "notepad.exe" --remoteapp --xfreerdp (for Windows 7 and newer)
* ubconnect --login user --password 123 --ip 192.168.1.1 --port 3389 --name "Notepad" --appstart "notepad.exe" --remoteapp --rdesktop (for Windows XP)
Connecting VBoxSeamless:
* ubconnect --vboxseamless --vmname "Windows 7" --name "Seamless mode"
* ubconnect --vboxseamless --vmname "Windows 7" --name "Start notepad" --appstart "notepad.exe" --login user --password 123  