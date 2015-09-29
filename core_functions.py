import ipxact_handle
import os

class IPCore:

    def __init__(self, core_name, rank, instantiation_name, fusesoc_core_path):
        self.core_name = core_name
        self.rank = rank
        self.instantiation_name = instantiation_name
        self.portlist = []
        self.paramlist = []
        self.fusesoc_core_path = fusesoc_core_path
        self.ipxact_file = ""

        self.look_for_ipxact_file()
        self.get_core_parameters()
        self.get_core_ports()

    def look_for_ipxact_file(self):
        ipxact_list = []
        for root, dirs, files in os.walk(self.fusesoc_core_path + "/" + self.core_name):
            for file in files:
                if file.endswith(".xml"):
                    ipxact_list.append(os.path.join(root, file))

        if len(ipxact_list) == 0:
            print("We couldn't find any ip-xact file for the " + self.core_name + "core.\n")
        elif len(ipxact_list) == 1:
            self.ipxact_file = ipxact_list[0]
        else:
            print("We found multiple ip-xact files, please type the name of the desired one.\n")
            for file in ipxact_list:
                print(file)
            self.ipxact_file = input()


    def get_core_ports(self):
        self.portlist = ipxact_handle.get_port_list(self.ipxact_file)


    def get_core_parameters(self):
        self.paramlist = ipxact_handle.get_parameter_list(self.ipxact_file)

