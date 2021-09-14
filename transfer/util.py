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

import datetime
import os

from logger import logger


def is_downlaod_necessary(destination, delta_t_hours=12):
    """
    if destination was last modified delta_t_hours or earlier no new download is necessary

    :param destination: target file
    :param delta_t_hours: minimum time since last modification to justify new download
    :return: True in case new download is necessary, otherwise False
    """
    if not destination.is_file():
        return True

    t_stamp = datetime.datetime.now()
    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(destination))
    dt_hours = (t_stamp - last_modified).total_seconds() / 3600
    if dt_hours < delta_t_hours:
        logger.debug(f"no download of {destination.name} necessary (last modified {dt_hours:.2f} hours ago)")
        return False
    else:
        return True
