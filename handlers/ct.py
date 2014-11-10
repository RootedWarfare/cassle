from handlers import handlers
from handlers import handler
from handlers.base import BaseHandler


@handler(handlers,handler=True)
class CT(BaseHandler):

    name = "ct"
    cert = True
    ocsp = True

    def __init__(self):
        self._process_ocsp = False
        self._lock = False

    def on_certificate(self,cert):
        sct = cert.get_ct_extension()
        if sct != None:
            print "\t[+] Certificate %s has SCT %s" % (cert.ca_name(), sct.encode('hex'))
        else:
            self._process_ocsp = True
            self._ca_name = cert.ca_name()
        self._lock = True

    def on_ocsp_response(self,ocsp):
        while self._lock == False:
            pass
        if self._process_ocsp == True:
            sct = ocsp.check_certificate_transparency()
            if sct != None:
                print "\t[+] Certificate %s has SCT %s" % (self._ca_name, sct.encode('hex'))
            else:
                print "\t[-] Certificate %s has not SCT" % self._ca_name

