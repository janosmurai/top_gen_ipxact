'''
@author: janosmurai
'''

import sys
import os

class ConfFileParameters:
    def __init__(self, conf_file_location):
        self.rank = []
        self.module_name = []
        self.instantiation_name = []
        self.conf_file_location = conf_file_location

        self.processConfFile()

    def processConfFile(self):
        conf_file = open(self.conf_file_location, "r")
        for line in conf_file:
            if line.startswith("[") & line.endswith("]\n"):
                if line[1:-2] == "slave":
                    # Module is a slave
                    self.rank.append("slave")
                elif line[1:-2] == "master":
                    # Module is a master
                    self.rank.append("master")
                else:
                    print("Rank must be slave or master")
            elif line.startswith("modul_name"):
                self.module_name.append(line.split("=").pop()[1:-1])
            elif line.startswith("instantiation_name"):
                self.instantiation_name.append(line.split("=").pop()[1:-1])
            else:
                print("Syntax error in the conf file")

