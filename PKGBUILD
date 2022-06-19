pkgname=ubconnect
pkgver=1.0
pkgrel=1
pkgdesc="Settings and creating shortcuts for remote desktop connection"
arch=('any')
url="https://github.com/HardLime/${pkgname}"
#url="https://github.com/HardLime/rabotaNEwork"
license=('GPL')
depends=(
    'pacman>5'
    'polkit'
    'python-bcrypt'
)

optdepends=(
    'alsa-utils: manipulate audio devices'
)
source=("$pkgname::git+${url}.git#branch=main")
sha256sums=('SKIP')

pkgver() {
    [[ -f "${srcdir}/${pkgname}/VERSION.md" ]] && printf "%s" "$(cat "${srcdir}/${pkgname}/VERSION.md" | grep VERSION | cut -d ' ' -f2)" || echo ${pkgver}
}

package() {
    install -dm755 "${pkgdir}/usr/bin"
    install -dm755 "${pkgdir}/usr/bin/UBConnectCore/scripts"
    install -dm755 "${pkgdir}/usr/bin/UBConnectCore/Service"
    install -dm755 "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders"
    install -dm755 "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Conf"
    install -dm755 "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Local"
    install -dm755 "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Remoat"
    install -dm755 "${pkgdir}/usr/share/${pkgname}/ui"
    install -dm755 "${pkgdir}/usr/share/applications"
    install -dm755 "${pkgdir}/usr/share/"${pkgname}"/images"
    install -dm755 "${pkgdir}/usr/lib/systemd/user"
    install -dm755 "${pkgdir}/memory/data/from/0/ublinux-data"
    install -dm755 "${pkgdir}/memory/data/from/0/ublinux-data/modules"
    install -dm755 "${pkgdir}/usr/share/locale"
    install -dm755 "${pkgdir}/usr/share/locale/ru"
    install -dm755 "${pkgdir}/usr/share/locale/ru/LC_MESSAGES"
    install -dm755 "${pkgdir}/usr/share/locale/en"
    install -dm755 "${pkgdir}/usr/share/locale/en/LC_MESSAGES"
    #install -dm755 "${pkgdir}/usr/share/polkit-1/actions"

    install -Dv "${srcdir}/${pkgname}"/usr/bin/ubconnect "${pkgdir}"/usr/bin
    install -Dv "${srcdir}/${pkgname}"/usr/bin/ubconnect.gtk "${pkgdir}"/usr/bin
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/scripts/* "${pkgdir}/usr/bin/UBConnectCore/scripts"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/VM.py "${pkgdir}/usr/bin/UBConnectCore/Service"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/ConfigVmWindow.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/MainWindowBuilder.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/MainWindowEventHandler.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/Conf/AddFolder.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Conf"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/Conf/AddPort.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Conf"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/Conf/AddUsb.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Conf"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/Conf/ChangeFolder.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Conf"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/Conf/dialog_delete.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Conf"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/Conf/PortsWindow.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Conf"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/Conf/SettingsModule.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Conf"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/Conf/VMPorts.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Conf"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/Local/LocalRdpWindow.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Local"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/Local/LocalRemoteWindow.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Local"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/Local/LocalVrdpWindow.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Local"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/Remoat/RemoatRdpWindow.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Remoat"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/Remoat/RemoatVrdpWindow.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Remoat"
    install -Dv "${srcdir}/${pkgname}"/usr/bin/UBConnectCore/Service/WindowBuilders/Remoat/RemoteRemoteWindow.py "${pkgdir}/usr/bin/UBConnectCore/Service/WindowBuilders/Remoat"
    install -Dv "${srcdir}/${pkgname}"/usr/share/applications/* "${pkgdir}/usr/share/applications"
    install -Dv "${srcdir}/${pkgname}"/usr/share/${pkgname}/ui/* "${pkgdir}/usr/share/${pkgname}/ui"
    install -Dv "${srcdir}/${pkgname}"/usr/share/${pkgname}/images/* "${pkgdir}/usr/share/${pkgname}/images"
    install -Dv "${srcdir}/${pkgname}"/usr/lib/systemd/user/* "${pkgdir}/usr/lib/systemd/user"
    install -Dv "${srcdir}/${pkgname}"/usr/share/locale/ru/LC_MESSAGES/ubconnect.mo "${pkgdir}/usr/share/locale/ru/LC_MESSAGES"
    install -Dv "${srcdir}/${pkgname}"/usr/share/locale/en/LC_MESSAGES/ubconnect.mo "${pkgdir}/usr/share/locale/en/LC_MESSAGES"

#     install -Dv "${srcdir}/${pkgname}"/usr/share/polkit-1/actions/* "${pkgdir}"/usr/share/polkit-1/actions
    install -Dvm774 --group=users "${srcdir}/${pkgname}"/memory/data/from/0/ublinux-data/* "${pkgdir}/memory/data/from/0/ublinux-data"
    install -Dvm774 --group=users "${srcdir}/${pkgname}"/memory/data/from/0/ublinux-data/modules/vboxapi.pfs "${pkgdir}/memory/data/from/0/ublinux-data/modules"
}