import os
import signal
import gi
gi.require_version('Gtk','3.0')
gi.require_version('AppIndicator3','0.1')
gi.require_version('Notify','0.7')


from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

APPINDICATOR_ID = 'network-proxy-toggle'
mode = "org.gnome.system.proxy mode"
host = "org.gnome.system.proxy.http host"
port = "org.gnome.proxy.http port"

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID,os.path.abspath('sample_icon.svg'),appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_quit = gtk.MenuItem('quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

#def toggle():
#    os.popen("gsettings get"+mode).read()

def quit(source):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    main()
