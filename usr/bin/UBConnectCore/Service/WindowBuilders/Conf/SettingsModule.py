import gettext
import locale
from os.path import exists

translate = gettext.translation("ubconnect", '/usr/share/locale', fallback=True)
i18n = translate.gettext

settingsPath = f"/memory/data/from/0/ublinux-data/ubconnect.ini"

class ConnectSettings:
    connectname: str
    vmname: str
    ip: str
    port: str
    domen: str
    display: str
    displaycolor: str
    cataloghome: str
    catalogcustom: str
    printerdefault: str
    printerall: str
    printercustom: str
    audio: str
    title: str
    icon: str
    connectclient: str
    connecttype: str
    connectstartapp: str


class forList:
    connectname: str
    vmname: str
    ip: str


class Settings:
    def writeSettings(self, connectsettings):
        findSector = open(f"{settingsPath}", "r")
        findS = findSector.read()
        find = f"[CONNECT_{connectsettings.connectname}]"
        if findS.find(find) != -1:
            findSector.close()
            settingsFile = open(f"{settingsPath}", "r+")
            temp = settingsFile.read()
            settingsFile.close()

            tag1 = temp.find(f"[CONNECT_{connectsettings.connectname}]")
            tag2 = temp.find(f"[/CONNECT_{connectsettings.connectname}]") + len(
                f"[/CONNECT_{connectsettings.connectname}]")
            temp1 = temp[tag1: tag2]
            arg = temp1.split("\n")

            arg[0] = f"[CONNECT_{connectsettings.connectname}]"
            arg[1] = f"NAME={connectsettings.vmname}"
            arg[2] = f"IP={connectsettings.ip}"
            arg[3] = f"PORT={connectsettings.port}"
            arg[4] = f"DOMEN={connectsettings.domen}"
            arg[5] = f"PASSWORD=null"
            arg[len(arg) - 1] = f"[/CONNECT_{connectsettings.connectname}]"
            okStr = temp.replace(temp1, self.getWrittingSettings(connectsettings, arg))
            settingsFile = open(f"{settingsPath}", "w")
            settingsFile.write(okStr)

            settingsFile.close()

        else:
            settingsFile = open(f"{settingsPath}", "a")
            strSettings = f"""[CONNECT_{connectsettings.connectname}]
NAME={connectsettings.vmname}
IP={connectsettings.ip}
PORT={connectsettings.port}
DOMEN={connectsettings.domen}
PASSWORD=null
{self.getSettingsConType(connectsettings)}
[/CONNECT_{connectsettings.connectname}]\n"""
            settingsFile.write(strSettings)
            settingsFile.close()

    def getConnectList(self):
        settingsFile = open(f"{settingsPath}", "r+")
        temp = settingsFile.read()
        settingsFile.close()
        arg = temp.split("\n")
        list = []
        i = 0
        for item in arg:

            if item.startswith("[CONNECT_"):
                temp = forList()
                temp.connectname = arg[i][9:-1]
                temp.vmname = arg[i + 1][5:]
                temp.ip = arg[i + 2][3:]
                list.append(temp)

            i += 1
        return list

    def deleteConnect(self, connectname):
        settingsFile = open(f"{settingsPath}", "r+")
        temp = settingsFile.read()
        settingsFile.close()
        tag1 = temp.find(f"[CONNECT_{connectname}]")
        tag2 = temp.find(f"[/CONNECT_{connectname}]\n") + len(
            f"[/CONNECT_{connectname}]\n")
        temp1 = temp[tag1: tag2]
        okStr = temp.replace(temp1, "")
        settingsFile = open(f"{settingsPath}", "w")
        settingsFile.write(okStr)
        settingsFile.close()

    def getSettings(self, connectname):
        settingsFile = open(f"{settingsPath}", "r+")
        temp = settingsFile.read()
        settingsFile.close()

        tag1 = temp.find(f"[CONNECT_{connectname}]")
        tag2 = temp.find(f"[/CONNECT_{connectname}]") + len(
            f"[/CONNECT_{connectname}]")
        temp1 = temp[tag1: tag2]
        if temp1 != "" and temp1 != " ":
            arg = temp1.split("\n")
            connect = ConnectSettings()
            connect.connectname = connectname
            connect.vmname = arg[1][arg[1].find("NAME=")+5:]
            connect.ip = arg[2][arg[2].find("IP=")+3:]
            connect.port = arg[3][arg[3].find("PORT=")+5:]
            connect.domen = arg[4][arg[4].find("DOMEN=")+6:]
            connect.password = arg[5][arg[5].find("PASSWORD=")+9:]
            connect.display = arg[7][arg[7].find("    DISPLAY=")+12:]
            connect.displaycolor = arg[8][arg[8].find("    COLOR=")+10:]
            connect.cataloghome = arg[9][arg[9].find("    CATALOGHOME=")+16:]
            connect.catalogcustom = arg[10][arg[10].find("    CATALOG=")+12:]
            connect.printerdefault = arg[11][arg[11].find("    PRINTERDEFAULT=")+19:]
            connect.printerall = arg[12][arg[12].find("    PRINTERALL=")+15:]
            connect.printercustom = arg[13][arg[13].find("    PRINTERCUSTOM=")+18:]
            connect.audio = arg[14][arg[14].find("    AUDIO=")+10:]
            connect.title = arg[15][arg[15].find("    TITLE=")+10:]
            connect.icon = arg[16][arg[16].find("    ICON=")+9:]
            connect.connectclient = arg[17][arg[17].find("    CONNECTCLIENT=")+18:]
            connect.connectstartapp = arg[18][arg[18].find("    APPSTART=")+13:]
            return connect
        else:
            return False

    def getWrittingSettings(self, connectsettings, arg):
        if connectsettings.connecttype == "VRDP":
            arg[7] = f"    DISPLAY={connectsettings.display}"
            arg[8] = f"    COLOR={connectsettings.displaycolor}"
            arg[9] = f"    CATALOGHOME={connectsettings.cataloghome}"
            arg[10] = f"    CATALOG={connectsettings.catalogcustom}"
            arg[11] = f"    PRINTERDEFAULT={connectsettings.printerdefault}"
            arg[12] = f"    PRINTERALL={connectsettings.printerall}"
            arg[13] = f"    PRINTERCUSTOM={connectsettings.printercustom}"
            arg[14] = f"    AUDIO={connectsettings.audio}"
            arg[15] = f"    TITLE={connectsettings.title}"
            arg[16] = f"    ICON={connectsettings.icon}"
            arg[17] = f"    CONNECTCLIENT={connectsettings.connectclient}"
            arg[18] = f"    APPSTART={connectsettings.connectstartapp}"
            return "\n".join(arg)
        elif connectsettings.connecttype == "RDP":
            arg[7] = f"    DISPLAY={connectsettings.display}"
            arg[8] = f"    COLOR={connectsettings.displaycolor}"
            arg[9] = f"    CATALOGHOME={connectsettings.cataloghome}"
            arg[10] = f"    CATALOG={connectsettings.catalogcustom}"
            arg[11] = f"    PRINTERDEFAULT={connectsettings.printerdefault}"
            arg[12] = f"    PRINTERALL={connectsettings.printerall}"
            arg[13] = f"    PRINTERCUSTOM={connectsettings.printercustom}"
            arg[14] = f"    AUDIO={connectsettings.audio}"
            arg[15] = f"    TITLE={connectsettings.title}"
            arg[16] = f"    ICON={connectsettings.icon}"
            arg[17] = f"    CONNECTCLIENT={connectsettings.connectclient}"
            arg[18] = f"    APPSTART={connectsettings.connectstartapp}"
            return "\n".join(arg)
        elif connectsettings.connecttype == "RA":
            arg[7] = f"    DISPLAY={connectsettings.display}"
            arg[8] = f"    COLOR={connectsettings.displaycolor}"
            arg[9] = f"    CATALOGHOME={connectsettings.cataloghome}"
            arg[10] = f"    CATALOG={connectsettings.catalogcustom}"
            arg[11] = f"    PRINTERDEFAULT={connectsettings.printerdefault}"
            arg[12] = f"    PRINTERALL={connectsettings.printerall}"
            arg[13] = f"    PRINTERCUSTOM={connectsettings.printercustom}"
            arg[14] = f"    AUDIO={connectsettings.audio}"
            arg[15] = f"    TITLE={connectsettings.title}"
            arg[16] = f"    ICON={connectsettings.icon}"
            arg[17] = f"    CONNECTCLIENT={connectsettings.connectclient}"
            arg[18] = f"    APPSTART={connectsettings.connectstartapp}"
            return "\n".join(arg)
        else:
            self.language_sys = locale.getdefaultlocale()
            translate.install()
            print("Error " + connectsettings.connecttype + " " + i18n("is incorrect"))

    def getSettingsConType(self, connectsettings):
        if connectsettings.connecttype == "VRDP":
            strReturn = f"""<TYPE_CONNECT=VRDP>
    DISPLAY={connectsettings.display}
    COLOR={connectsettings.displaycolor}
    CATALOGHOME={connectsettings.cataloghome}
    CATALOG={connectsettings.catalogcustom}
    PRINTERDEFAULT={connectsettings.printerdefault}
    PRINTERALL={connectsettings.printerall}
    PRINTERCUSTOM={connectsettings.printercustom}
    AUDIO={connectsettings.audio}
    TITLE={connectsettings.title}
    ICON={connectsettings.icon}
    CONNECTCLIENT={connectsettings.connectclient}
    APPSTART={connectsettings.connectstartapp}
</TYPE_CONNECT=VRDP>"""
            return strReturn
        elif connectsettings.connecttype == "RDP":
            strReturn = f"""<TYPE_CONNECT=RDP>
    DISPLAY={connectsettings.display}
    COLOR={connectsettings.displaycolor}
    CATALOGHOME={connectsettings.cataloghome}
    CATALOG={connectsettings.catalogcustom}
    PRINTERDEFAULT={connectsettings.printerdefault}
    PRINTERALL={connectsettings.printerall}
    PRINTERCUSTOM={connectsettings.printercustom}
    AUDIO={connectsettings.audio}
    TITLE={connectsettings.title}
    ICON={connectsettings.icon}
    CONNECTCLIENT={connectsettings.connectclient}
    APPSTART={connectsettings.connectstartapp}
</TYPE_CONNECT=RDP>"""
            return strReturn
        elif connectsettings.connecttype == "RA":
            strReturn = f"""<TYPE_CONNECT=RA>
    DISPLAY={connectsettings.display}
    COLOR={connectsettings.displaycolor}
    CATALOGHOME={connectsettings.cataloghome}
    CATALOG={connectsettings.catalogcustom}
    PRINTERDEFAULT={connectsettings.printerdefault}
    PRINTERALL={connectsettings.printerall}
    PRINTERCUSTOM={connectsettings.printercustom}
    AUDIO={connectsettings.audio}
    TITLE={connectsettings.title}
    ICON={connectsettings.icon}
    CONNECTCLIENT={connectsettings.connectclient}
    APPSTART={connectsettings.connectstartapp}
</TYPE_CONNECT=RA>"""
            return strReturn

