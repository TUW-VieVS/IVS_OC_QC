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
import argparse
import configparser

import transfer.download as download
from logger.logger import initialize_logging


def start_download():
    path = settings["data"].get("master", "data/MASTER")
    download.master(path)


if __name__ == "__main__":
    doc = "=== IVS Operation Center Quality Control === \n" \
          "Some scripts to automatically download and evaluate IVS observing programs."

    parser = argparse.ArgumentParser(description=doc)
    parser.add_argument("-i", "--ini", help="path to .ini file", default="settings.ini")
    parser.add_argument("-nd", "--no_download", action="store_true", help="do not download new data")
    args = parser.parse_args()

    settings = configparser.ConfigParser()
    settings.read(args.ini)

    initialize_logging()

    start_download()
