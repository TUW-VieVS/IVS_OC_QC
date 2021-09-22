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

import pandas as pd

def read_master(file):
    pattern = re.compile(r'^\|([\w-]+)\s*\|([\w-]+)\s*\|')

    df_master = pd.DataFrame(None, None, ["name","code"], dtype=str)
    with open(file,'r') as f:
        for l in f:
            match = pattern.search(l)
            if match:
                op = match.group(1)
                code = match.group(2).lower()
                s = pd.Series([op, code], index=["name","code"], dtype=str)
                df_master = df_master.append(s, ignore_index=True)
    return df_master.astype(str)
