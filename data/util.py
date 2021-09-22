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
import re
from pathlib import Path

import data.parser

import pandas as pd

STORAGE = dict()
NAME2PROGRAM = {
    "AOV": re.compile(r"AOV\d{3}"),
    "AUA": re.compile(r"AUS-AST\d{3}"),
    "AUM": re.compile(r"AUS-MIX\d{3}"),
    "CRD": re.compile(r"IVS-CRD\d{3}"),
    "CRF": re.compile(r"IVS-CRF\d{3}"),
    "INT1": re.compile(r"IN1\d{2}-\d{3}"),
    "INT2": re.compile(r"IN2\d{2}-\d{3}"),
    "INT3": re.compile(r"IN3\d{2}-\d{3}"),
    "OHG": re.compile(r"IVS-OHG\d{3}"),
    "R1": re.compile(r"IVS-R1\d{3,4}"),
    "R4": re.compile(r"IVS-R4\d{3,4}"),
    "T2": re.compile(r"IVS-T2\d{3}"),
    "T2P": re.compile(r"IVS-T2P\d{3}"),
    "VO": re.compile(r"VGOS-O\d{4}"),
    "VGOS2": re.compile(r"VGOS-2\d{3}"),
    "VGOSB": re.compile(r"VGOS-B\d{3}"),
    "VGOSC": re.compile(r"VGOS-C\d{3}"),
}


def code2program(code, year):

    if year in STORAGE:
        df = STORAGE[year]
    else:
        path = Path("../IVS_DATA/MASTER")
        year_str = str(year % 100)

        dfs = []
        for f in path.iterdir():
            if year_str in f.name:
                dfs.append(data.parser.read_master(f))
        df = pd.concat(dfs)
        STORAGE[year] = df

    name = df.loc[df.code == code, "name"]
    if name.shape[0] == 1:
        name = name.values[0]
    else:
        return "unknown"

    for op, v in NAME2PROGRAM.items():
        if v.match(name):
            return op

    return "unknown"
