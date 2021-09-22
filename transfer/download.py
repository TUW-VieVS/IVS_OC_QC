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

import requests
from ftplib import FTP, FTP_TLS
from ftplib import all_errors as ftp_errors

from logger import logger
from transfer import https, ftp
from data.util import code2program


def master(path):
    logger.info("start downloading master files")
    path = Path(path)

    year = datetime.date.today().year
    try:
        ftp_server = FTP_TLS(host='gdc.cddis.eosdis.nasa.gov')
        ftp_server.login(user='anonymous', passwd='')
        ftp_server.prot_p()
        ftp_server.cwd('/vlbi/ivscontrol/')
    except ftp_errors as e:
        logger.error(f"error connecting to gdc.cddis.eosdis.nasa.gov: {e}")
        return

    successful, error, skipped = 0, 0, 0

    def download_(f, force=False):
        nonlocal successful, error, skipped
        dest = (path / f)
        if force or not dest.is_file():
            if ftp.ftp_download(ftp_server, f, dest):
                error += 1
            else:
                successful += 1
        else:
            skipped += 1

    # download past data in case it is missing
    for i in range(1979, year):
        file = f"master{i % 100:02d}.txt"
        download_(file)
    for i in range(1992, year):
        file = f"master{i % 100:02d}-int.txt"
        download_(file)
    for i in [2013, *range(2015, 2020)]:
        file = f"master{i % 100:02d}-vgos.txt"
        download_(file)

    # always download data from this year
    file = f"master{year % 100}.txt"
    download_(file, True)

    file = f"master{year % 100}-int.txt"
    download_(file, True)

    logger.info(f"successfully downloaded {successful} files, {error} errors, {skipped} skipped")


def download_cddis(path, year=None):
    logger.info("start downloading files from CDDIS")
    if year is None:
        year = datetime.date.today().year
        # download_cddis(path, year-1)
    path = Path(path)

    successful, error, skipped = 0, 0, 0

    def download_(f, dest, force=False):
        nonlocal successful, error, skipped
        if force or not dest.is_file():
            if ftp.ftp_download(ftp_server, f, dest):
                error += 1
            else:
                successful += 1
        else:
            skipped += 1

    try:
        # connect to FTP server
        ftp_server = FTP_TLS(host='gdc.cddis.eosdis.nasa.gov')
        ftp_server.login(user='anonymous', passwd='')
        ftp_server.prot_p()
        ftp_server.cwd(f'/vlbi/ivsdata/aux/{year}')

        # get a list of all files at FTP server
        ftp_dirs = ftp_server.nlst()
        for dir in ftp_dirs:
            ftp_server.cwd(f"/vlbi/ivsdata/aux/{year}/{dir}")
            ftp_files = ftp_server.nlst()

            for file in ftp_files:
                if file.endswith(".skd") or "spool" in file:
                    out = path / code2program(dir, year) / dir / file
                    download_(file, out)

        logger.info(f"successfully downloaded {successful} files, {error} errors, {skipped} skipped")

    except ftp_errors as e:
        logger.error(f"error connecting to gdc.cddis.eosdis.nasa.gov: {e}")


def download_bkg(path, year=None):
    logger.info("start downloading files from BKG")
    if year is None:
        year = datetime.date.today().year
        # download_bkg(path, year-1)
    path = Path(path)

    successful, error, skipped = 0, 0, 0

    def download_(f, dest, force=False):
        nonlocal successful, error, skipped
        if force or not dest.is_file():
            if ftp.ftp_download(ftp_server, f, dest):
                error += 1
            else:
                successful += 1
        else:
            skipped += 1

    try:
        # connect to FTP server
        ftp_server = FTP("ivs.bkg.bund.de")
        ftp_server.login()
        ftp_server.cwd(f"/pub/vlbi/ivsdata/aux/{year}/")

        # get a list of all files at FTP server
        ftp_dirs = ftp_server.nlst()
        for dir in ftp_dirs:
            ftp_server.cwd(f"/pub/vlbi/ivsdata/aux/{year}/{dir}")
            ftp_files = ftp_server.nlst()

            for file in ftp_files:
                if file.endswith(".skd") or "spool" in file:
                    out = path / code2program(dir, year) / dir / file
                    download_(file, out)

        logger.info(f"successfully downloaded {successful} files, {error} errors, {skipped} skipped")

    except ftp_errors as e:
        logger.error(f"error connecting to ivs.bkg.bund.de: {e}")

