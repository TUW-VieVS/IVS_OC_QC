# ##############################################################################
#  Copyright (c) 2021. Matthias Schartner                                      #
#                                                                              #
#  This program is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation, either version 3 of the License, or           #
#  (at your option) any later version.                                         #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.      #
# ##############################################################################

import requests

from logger import logger
from transfer.util import is_downlaod_necessary


def https_download(source, destination, force=True):
    """
    Download file via https.

    Only download if destination was last modified more than 12 hours ago - useful for debugging and testing to save
    time. Use force=True in case you want to ensure that you always download file

    :param source: web url to source file
    :param destination: destination
    :param force: force download even if destination file was recently modified
    :return: return True in case an error occurred, otherwise False
    """

    destination.parent.mkdir(parents=True, exist_ok=True)
    error_flag = False
    if force or is_downlaod_necessary(destination):
        try:
            r = requests.get(source, stream=True)
            if r.ok:
                with open(destination, 'wb') as f:
                    for ch in r.iter_content(chunk_size=1000):
                        f.write(ch)
                    logger.debug(f"updating {destination}")
            else:
                error_flag = True
                logger.error(f"error updating {destination}")
                if destination.is_file():
                    destination.unlink()
        except Exception as e:
            error_flag = True
            logger.error(f"error updating {destination} - {e}")
            if destination.is_file():
                destination.unlink()
    return error_flag


if __name__ == "__main__":
    pass
