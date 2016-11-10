#!bin/sh

die() {
    echo "ERROR: $1. Aborting!"
    exit 1
}

#if [ "$(id -u)" -ne 0 ] ; then
#    echo "You must run this script as root. Sorry!"
#    exit 1
#fi

APPLET_FILE_DEST="/usr/local/bin/proxy-applet"
TMP_FILE="proxy-applet.desktop"

#copying applet program
sudo cp applet.py $APPLET_FILE_DEST || die "could not copy applet to bin"
sudo chmod a+x $APPLET_FILE_DEST

#copying icon
sudo cp proxy-applet.svg /usr/share/icons/proxy-applet.svg || die "could not copy image"

cat > $TMP_FILE <<EOT
[Desktop Entry]
Type=Application
Exec=/usr/local/bin/proxy-applet
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[en_IN]=proxy-applet
Name=proxy-applet
Comment[en_IN]=change proxy from the top menu
Comment=change proxy from the top menu

EOT

mkdir -p ~/.config/autostart || die " could not create autostart directory"

cp $TMP_FILE ~/.config/autostart/proxy-applet.desktop || die "could not copy applet init file to autostart"
rm $TMP_FILE 

nohup proxy-applet &> /dev/null &
echo "success"

exit 0

