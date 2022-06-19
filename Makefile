all: install

install:
	install -Dv usr/bin/* /usr/bin/
	install -Dv usr/share/applications/* /usr/share/applications/
	install -Dv usr/share/images/* /usr/share/images/

uninstall:
	rm -f "/usr/bin/ubconnect"
	rm -f "/usr/share/applications/ubconnect.desktop"
	rm -f "/usr/share/images/ubc_side_bar.png"
	rm -f "/usr/share/images/ubc_side_bar_dark.png"