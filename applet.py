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
host="org.gnome.system.proxy.http host"
port="org.gnome.system.proxy.http port"

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID,os.path.abspath('sample_icon.svg'),appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_toggle = gtk.MenuItem('toggle')
    item_toggle.connect('activate',toggle)
    menu.append(item_toggle)
    item_quit = gtk.MenuItem('quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def toggle(source):
    data = os.popen("gsettings get "+mode).read()
    if(data == "'none'\n"):
        os.popen("gsettings set "+mode+" manual").read()
        host_data = os.popen("gsettings get "+host).read()
        port_data = os.popen("gsettings get "+port).read()
        notify_for_manual(host_data,port_data)
    else:
        os.popen("gsettings set "+mode+" none").read()
        notify.Notification.new("Proxy: none",None).show()
    

def notify_for_manual(host_data,port_data):
    data = host_data+":"+port_data 
    notify.Notification.new("Proxy "+data,None).show()

def quit(source):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    main()
