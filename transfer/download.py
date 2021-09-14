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
from pathlib import Path

from logger import logger
from transfer import https


def master(path):
    logger.info("start downloading master files")
    path = Path(path)

    year = datetime.date.today().year

    successful = 0
    error = 0

    # download past data in case it is missing
    for i in range(1979, year):
        file = f"master{i % 100:02d}.txt"
        dest = (path / file)
        if not dest.is_file():
            if https.https_download(f"https://cddis.nasa.gov/archive/vlbi/ivscontrol/{file}", dest):
                error += 1
            else:
                successful += 1
    for i in range(1992, year):
        file = f"master{i % 100:02d}-int.txt"
        dest = (path / file)
        if not dest.is_file():
            if https.https_download(f"https://cddis.nasa.gov/archive/vlbi/ivscontrol/{file}", dest):
                error += 1
            else:
                successful += 1
    for i in [2013, *range(2015, 2020)]:
        file = f"master{i % 100:02d}-vgos.txt"
        dest = (path / file)
        if not dest.is_file():
            if https.https_download(f"https://cddis.nasa.gov/archive/vlbi/ivscontrol/{file}", dest):
                error += 1
            else:
                successful += 1

    # always download data from this year
    file = f"master{year % 100}.txt"
    dest = (path / file)
    if https.https_download(f"https://cddis.nasa.gov/archive/vlbi/ivscontrol/{file}", dest):
        error += 1
    else:
        successful += 1

    file = f"master{year % 100}-int.txt"
    dest = (path / file)
    if https.https_download(f"https://cddis.nasa.gov/archive/vlbi/ivscontrol/{file}", dest):
        error += 1
    else:
        successful += 1

    logger.info(f"successfully downloaded {successful} files, {error} errors")
