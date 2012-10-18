
import Globals
import os.path
from Products.ZenModel.ZenPack import ZenPackBase
import logging
import subprocess

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())
    
log = logging.getLogger('.'.join(['zen', __name__]))

DEVICE_CLASS = "/Websites"

class ZenPack(ZenPackBase):
    def install(self, app):
        """
        Extend the install method, so we can verify twill
        """
        try:
            import twill
        except ImportError:
            msg = ("This ZenPack requires the twill module. It is currently" +
                   " not installed. Attempting to install it now.")
            log.info(msg)
            try:
                subprocess.check_call(["easy_install", "twill"])
            except subprocess.CalledProcessError as ex:
                msg = "Failed to install twill: {0}".format(ex.returncode)
                log.error(msg)
                msg = ("You have to install twill before installing this "
                       "ZenPack . Please run `easy_install twill` and then " +
                       "try again")
                log.critical(msg)
                exit(1)
            
        #We need to ensure the device class of /Websites exists
        #It might already, so do this nicely, not blindly
        if DEVICE_CLASS not in app.dmd.Devices.getOrganizerNames():
            log.info("Creating new device class: {0}".format(DEVICE_CLASS))
            org = app.dmd.Devices.createOrganizer(DEVICE_CLASS)
        ZenPackBase.install(self, app)
