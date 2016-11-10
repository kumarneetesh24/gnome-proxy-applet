#!/usr/bin/env python
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
img_path = "/usr/share/icons/proxy-applet.svg"

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID,img_path,appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def checkProxy(): 
   data = os.popen("gsettings get "+mode).read()
   if(data == "'none'\n"):
       return True
   else:
       return False 


def build_menu():
    menu = gtk.Menu()
    
    item_toggle = gtk.MenuItem('toggle')
    item_toggle.connect('activate',toggle)
    menu.append(item_toggle)
    
    # Separator
    smi = gtk.SeparatorMenuItem()
    smi.show()
    menu.append(smi)
    
    #group for radio icon
    grp = []
    #radio icon
    item_none = gtk.RadioMenuItem.new_with_label(grp, 'none')
    grp = item_none.get_group()
    item_none.set_active(checkProxy() == True)
    item_none.connect('toggled',prnone)
    menu.append(item_none)

    #radio icon 
    item_manual = gtk.RadioMenuItem.new_with_label(grp,'manual')
    grp = item_manual.get_group()
    item_manual.set_active(checkProxy() == False)
    item_manual.connect('toggled',manual)
    menu.append(item_manual)
    
    # Separator
    smi = gtk.SeparatorMenuItem()
    smi.show()
    menu.append(smi)
    
    item_quit = gtk.MenuItem('quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    
    menu.show_all()
    return menu

def prnone(source):
    os.popen("gsettings set "+mode+" none")

def manual(source):
    os.popen("gsettings set "+mode+" manual")


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
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
