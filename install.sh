#!bin/sh

die() {
    echo "ERROR: $1. Aborting!"
    exit 1
}

if [ "$(id -u)" -ne 0 ] ; then
    echo "You must run this script as root. Sorry!"
    exit 
fi

APPLET_FILE_DEST="/usr/local/bin/proxy-applet"  
INIT_FILE="/etc/init.d/proxy-applet"
TMP_FILE="temp"

#copying applet program
cp applet.py $APPLET_FILE_DEST || die "could not copy applet to bin"
chmod a+x $APPLET_FILE_DEST

#copying icon
cp proxy-applet.svg /usr/share/icons/proxy-applet.svg || die "could not copy image"

cat > TMP_FILE <<EOT
#!/bin/sh
$APPLET_FILE_DEST 

EOT

cp $TMP_FILE $INIT_FILE && \
   chmod +x $INT_FILE || die "could not copy applet init file to $INIT_FILE"
rm $TMP_FILE 

update-rc.d proxy-applet defaults || die "could not start the services contact the author"


exit 0
