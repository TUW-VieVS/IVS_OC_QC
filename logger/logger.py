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
import logging
from pathlib import Path

logger = logging.getLogger('IVS_OC_QC')


def initialize_logging(severity_console="INFO", severity_file="DEBUG", outdir="data/IVS_OC_QC_LOGS", mode='w'):
    """
    initialize logging environment

    in case level_str cannot be interpreted it will default to "DEBUG"
    log file will be named: yyyy-mm-dd_EOP_PCC_AUTO.log

    :param severity_console: level [DEBUG, INFO, WARNING, ERROR, CRITICAL]
    :param severity_file: level [DEBUG, INFO, WARNING, ERROR, CRITICAL]
    :param outdir: directory where logs will be stored
    :param mode: log file open mode
    :return: None
    """

    c_level_str = severity_console.lower()
    f_level_str = severity_file.lower()

    levels = {"debug": logging.DEBUG,
              "info": logging.INFO,
              "warning": logging.WARNING,
              "error": logging.ERROR,
              "critical": logging.CRITICAL,
              "none": None,
              }

    def log_str2level(str):
        # get logging severity
        if str in levels:
            level = levels[str]
        else:
            # default to DEBUG
            level = logging.DEBUG
        return level

    c_level = log_str2level(c_level_str)
    f_level = log_str2level(f_level_str)

    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    today = str(datetime.datetime.now().date())
    out = outdir / f"{today}_EOP_PCC_AUTO.log"
    out.parent.mkdir(exist_ok=True, parents=True)

    logger.setLevel(min(c_level, f_level))

    formatter = logging.Formatter('[%(asctime)s]  [%(levelname)s] [%(module)s] %(message)s')

    if f_level is not None:
        fh = logging.FileHandler(out, mode=mode)
        fh.setLevel(f_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    if c_level is not None:
        ch = logging.StreamHandler()
        ch.setLevel(c_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if f_level is not None:
        logger.info(f"logging levels: console {c_level_str}, file {f_level_str}")
        logger.info(f"logs will be written to {out.absolute()}")
    else:
        logger.info(f"logging levels: console {c_level_str}, file {f_level_str}")
        logger.info(f"no logs will be written to file")
