#!/usr/bin/env python3

import argparse
import re
import time

class UpdateVersion:

    def parse_cli(self):
        """Parse Unix command line arguments"""
        parser = argparse.ArgumentParser(description="Process some integers.")
        parser.add_argument("filenames", metavar="file", nargs="*", help="Filenames")
        parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity for debugging")

        self.args = parser.parse_args()
        if self.args.verbose:
            # print(f"lsutil ver. {__init__.__version__}, {__init__.__built__}")
            print(self.args)

    @staticmethod
    def main_cli():
        """Unix command line interface"""
        self = UpdateVersion()
        self.parse_cli()
        lines = []

        for filename in self.args.filenames:
            with open(filename, encoding='utf8') as filep:
                for line in filep:
                    line = line.rstrip()
                    if mrx := re.search(r'^\s*__version__\s*=\s*"(\d+)\.(\d+)\.(\d+)\"\s*$', line):
                        major, minor, patch = mrx.group(1), mrx.group(2), int(mrx.group(3))
                        print(f'version "{major}.{minor}.{patch}" updated to ', end='')
                        patch += 1
                        print(f'"{major}.{minor}.{patch}"')
                        lines.append(f'__version__ = "{major}.{minor}.{patch}"')
                    elif mrx := re.search(r'^\s*__build__\s*=\s*"([\w :])+\"\s*$', line):
                        lines.append(f'__build__ = "{time.asctime()} {time.tzname[0]}"')
                    else:
                        lines.append(line)
            print(f'// Saving to {filename}')
            with open(filename, "w", encoding='utf8') as filep:
                for line in lines:
                    print(line, file=filep)
        

if __name__ == "__main__":

    UpdateVersion.main_cli()

