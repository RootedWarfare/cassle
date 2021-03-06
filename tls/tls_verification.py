

# Copyright (C) 2014       Alvaro Felipe Melchor (alvaro.felipe91@gmail.com)


# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tls.cert import X509Chain
from handlers import handlers
from tls.ocsp import Ocsp
import logging
from conf import debug_logger
# from multiprocessing import Process

logger = logging.getLogger(__name__)


class TLSVerificationDispatch:
    def __init__(self, data):
        self.certs = None
        self.status_request = None
        if 'cert' in data:
            self.certs = data['cert']
        if 'status_request' in data:
            self.status_request = data['status_request']
        self.dispatch_certificate()
        # self.dispatch_status_request()

    def dispatch_certificate(self):
        # Do everything related with certificate
        if self.certs is not None:
            # verify certificate
            try:
                chain = X509Chain(self.certs)
            except Exception:
                return
            if chain.length_chain() == 1:
                try:
                    debug_logger.debug(
                        '[-] Chain incomplete from %s' % chain.ca_name()
                        )
                    logger.info(
                        "The chain is incomplete %s"
                        % chain.subject_common_name()
                        )
                except Exception:
                    debug_logger.debug('[-] Chain incomplete')
                    logger.info('[-] Chain incomplete')
            else:
                # TODO ask ocsp status when is only necessary
                ocsp = Ocsp(chain)
                debug_logger.debug('[+] Verifying certificate')
                for cls in handlers.store:
                    handlers.store[cls](chain, ocsp)

        else:
            pass

    def dispatch_status_request(self):
        if self.dispatch_status_request is not None:
            # verify connection through ocsp_stapling
            # In the future only add here all the code needed
            pass
        else:
            pass


