#!/usr/bin/env python3

# Copyright 2021 Christopher Simpkins

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import sys


def main(argv):
    # Note:
    # VTT exports XML with CRLF line endings on Win.
    # Python writes universal LF line endings on macOS.
    # This script maintains the line ending format that is
    # read in to avoid unnecessary cross-platform text diffs

    regex_1 = re.compile(
        r"(?<=USEMYMETRICS\[\])([^\<]*)(SVTCA\[X\][^\<]*)(?=\<\/assembly\>)"
    )
    regex_2 = re.compile(
        r"(?<=VTTTalk\sUnicode)([^\<]*)(SVTCA\[X\][^\<]*)(?=\<\/assembly\>)"
    )
    for path in argv:
        # Note: keep deactivation of universal newline mode
        with open(path, mode="r", newline="") as fr:
            xmlstring = fr.read()
            # convert all ResYDist to YShift operations
            xmlstring_pass1 = xmlstring.replace("ResYDist", "YShift")
            # the following regex replacements remove the glyf table
            # SVTCA[X] source blocks
            xmlstring_pass_2 = regex_1.sub(r"\1", xmlstring_pass1)
            cleaned_xmlstring = regex_2.sub(r"\1", xmlstring_pass_2)

        with open(path, mode="w", newline="") as fw:
            fw.write(cleaned_xmlstring)
            print(f"Modified {path}")


if __name__ == "__main__":
    main(sys.argv[1:])
