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

from ftplib import all_errors as ftp_errors

from logger import logger
from transfer.util import is_downlaod_necessary


def ftp_download(ftp, source, destination, force=True):
    """
    Download file from ftp server.

    Only download if destination was last modified more than 12 hours ago - useful for debugging and testing to save
    time. Use force=True in case you want to ensure that you always download file

    :param ftp: FTP server
    :param source: source file
    :param destination: destination
    :param force: force download even if destination file was recently modified
    :return: return True in case an error occurred, otherwise False
    """

    destination.parent.mkdir(parents=True, exist_ok=True)
    error_flag = False
    if force or is_downlaod_necessary(destination):
        try:
            msg = ftp.retrbinary("RETR " + source, open(destination, 'wb').write)
            logger.debug(f"updating {destination} ({ftp.host})... {msg}")
        except ftp_errors as err:
            error_flag = True
            logger.error(f"error downloading ftp file {source} {err}")
            if destination.is_file():
                try:
                    destination.unlink()
                except PermissionError as e:
                    logger.error(f"error deleting {destination} - {e}")
    return error_flag


if __name__ == "__main__":
    pass
