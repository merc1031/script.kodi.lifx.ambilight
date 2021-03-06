import os
import traceback

import xbmc
import xbmcaddon

__addon__ = xbmcaddon.Addon()
__addondir__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__cwd__ = __addon__.getAddonInfo('path')
__resource__ = xbmc.translatePath(os.path.join(__cwd__, 'resources', 'lib')).decode('utf-8')

sys.path.append(__resource__)

from settings import Settings

from service_entry import Service
from tools import xbmclog
from ga_client import GoogleAnalytics

DELAY = int(Settings.getSetting('startup_delay') or 0)

if __name__ == "__main__":
    xbmclog("======== STARTED ========")

    try:
        service = Service()
        abort = False
        if DELAY and xbmc.Monitor().waitForAbort(DELAY):
            raise RuntimeError("Abort event while waiting to start Emby for kodi")
            abort = True
        # Start the service
        if abort == False:
            service.service_entry_point()

    except Exception as error:
        if not (hasattr(error, 'quiet') and error.quiet):
            ga = GoogleAnalytics()
            errStrings = ga.formatException()
            ga.sendExceptionData(errStrings[0])
            ga.sendEventData("Crash", errStrings[0], errStrings[1])

        # Display the *original* exception
        traceback.print_exc()

        xbmclog("Forcing shutdown")
        service.shutdown()

    xbmclog("======== STOPPED ========")
