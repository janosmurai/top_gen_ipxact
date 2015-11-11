import ipxact_handle
import os

class IPCore:

    def __init__(self, core_name, rank, instantiation_name, fusesoc_core_path, system_buses):
        self.core_name = core_name
        self.rank = rank
        self.instantiation_name = instantiation_name
        self.fusesoc_core_path = fusesoc_core_path
        self.ipxact_file = ""
        self.bus_interfacedict = {}
        self.portdict = {}
        self.bus_types = {}
        self.system_buses = system_buses

        self.look_for_ipxact_file()
        self.get_core_parameters()
        self.get_core_ports()

    def look_for_ipxact_file(self):
        ipxact_list = []
        for root, dirs, files in os.walk(self.fusesoc_core_path + "/" + self.core_name + "/ip-xact"):
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

        tmp_port_dict = ipxact_handle.get_port_dict(self.ipxact_file)
        for port in tmp_port_dict:
            self.portdict[self.core_name + ":" + port] = tmp_port_dict[port]

        tmp_bus_types = ipxact_handle.get_bus_interface_types(self.ipxact_file, self.system_buses)
        tmp_bus_interface_dict = ipxact_handle.get_bus_interface_dict(self.ipxact_file, tmp_bus_types)
        for bus in tmp_bus_interface_dict:
            self.bus_interfacedict[self.core_name + ":" + bus] = tmp_bus_interface_dict[bus]
        for bus_type in tmp_bus_types:
            self.bus_types.update({bus_type: self.core_name})



    def get_core_parameters(self):
        self.paramdict = ipxact_handle.get_parameter_dict(self.ipxact_file)


def get_updated_core_parameters(f, paramdict, core_name):
    # paramdict: contains the default parameters of all the cores.
    updated_paramdict = {}
    current_params = {}
    for param in paramdict:
        if str(param).startswith(core_name):
            current_params.update({str(param).split(":")[1]: paramdict[param]})

    for line in f:
        param_type = line.split("(")[0][1:]
        param_value = line.split("(")[1][:-3].replace("\"", "")
        for param in current_params:
            # Only print out the non default parameters, to avoid redundant information.
            if param_type.startswith(str(param)):
                if not current_params[param] == param_value:
                    updated_paramdict[core_name + ":" + param_type] = param_value

    return updated_paramdict