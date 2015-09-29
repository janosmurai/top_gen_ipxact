'''
@author: janosmurai
'''

import os

import handle_conf_file
import automatic_mode_functions
import ipxact_handle
import system_functions
import core_functions


class IPNode:
    parameters = []
    ports = []
    name = ""
    connections_to_file = []
    val = ""
    output_path = ""

    def __init__(self, moduleNode, top_gen_output_path):

        self.top_gen_output_path = top_gen_output_path
        self.name = moduleNode.name
        self.portlist = []
        self.paramlist = []
        self.connections = []





    def set_connections(self, portlist, is_connection_file_exists):
        for line in portlist:
            if not "wb" in line:
                self.connections

    def set_core_params(self, parameterlist):
        output_path = ""
        for element in self.top_gen_output_path:
            output_path += element + "/"

        if os.path.isfile(output_path + self.name + "_paramlist"):
            print("We found an existing parameter file. (" + self.name + ")\n If the list is ready, please press enter.\n")
            print("If the list is not up to date, please fix or delete it and restart the process.\n")
            input()
        else:
            f = open(output_path + self.name + "_paramlist", "w")
            for param in parameterlist:
                isnumeric = False
                for num in range(10):
                    if param.argname.value.startswith(str(num)):
                        f.write("." + param.paramname.name + "(" + param.argname.value + "),\n")
                        isnumeric = True

                if not isnumeric:
                    f.write("." + param.paramname.name + "(\"" + param.argname.value + "\"),\n")

            f.close()
            print("\nPlease fill up the " + self.name + " cores parameter list, which is available in the output folder.")
            print("\nFirst the parameter list is filled up with the default values.")
            input("\nIf the list is ready, please press enter!\n")

    def get_core_params(self, parameterlist):
        output_path = ""
        for element in self.top_gen_output_path:
            output_path += element + "/"

        f = open(output_path + self.name + "_paramlist", "r")
        for line in f:
            param_type = line.split("(")[0][1:]
            param_value = line.split("(")[1][:-3].replace("\"", "")
            for param in parameterlist:
                # Only print out the non default parameters, to avoid redundant information.
                if param_type.startswith(str(param.paramname.name)):
                    if param.argname.value == param_value:
                        param.argname.value = ""
                        param.paramname.name = ""
                    else:
                        param.argname.value = param_value
        f.close()

    def get_connections(self, inst, rank):
        for line in inst.portlist:
            if (line.argname.name != "wb_clk") & (line.argname.name != "wb_rst") & ("wb" in line.argname.name):
                if rank == "slave":
                    if line.argname.name.endswith("i"):
                        line.argname.name = "wb_m2s_{modul_name}_{port}".format(modul_name=self.name,
                                                                                port=line.argname.name[-5:-2])
                    else:
                        line.argname.name = "wb_s2m_{modul_name}_{port}".format(modul_name=self.name,
                                                                                port=line.argname.name[-5:-2])
                else:
                    if line.argname.name.endswith("o"):
                        line.argname.name = "wb_m2s_{modul_name}_{port}".format(modul_name=self.name,
                                                                                port=line.argname.name[-5:-2])
                    else:
                        line.argname.name = "wb_s2m_{modul_name}_{port}".format(modul_name=self.name,
                                                                                port=line.argname.name[-5:-2])


def set_comment_field(is_interactive, auto_mode_param):
    description_comment = ""
    if is_interactive == "I":
        print("Do you want to add a description comment?\n")
        user_in = input("If yes, please add the path to the appropriate file, if no just press enter!\n")
    else:
        user_in = auto_mode_param["Description comment"]
        user_in = str(user_in).replace("\n", "")
        user_in = user_in.replace(" ", "")
    if not user_in == "":
        f = open(user_in, "r")
        description_comment = f.read()
        f.close()
    return description_comment

def set_top_modul_params(is_interactive, auto_mode_param):
    top_modul_param_list = []
    top_modul_param_list_out = []
    top_module_param_input = ""
    if is_interactive == "I":
        top_modul_instantiation_name = input("Please add the top module's name, then press enter!\n")
        print("Do you want to add any parameters for the top modul?\n")
        print("In case of yes, please add the parameters as follows: param1 = value1; param2 = value2; etc...\n")
        top_module_param_input = input("In case of no, just press enter!\n")
    else:
        top_modul_instantiation_name = auto_mode_param["Top module's instantiation name"]
        top_modul_instantiation_name = str(top_modul_instantiation_name).replace(" ", "")
        top_module_param_input = auto_mode_param["Top module's parameters"]
        top_module_param_input = str(top_module_param_input).replace(" ", "")
    if top_module_param_input == "":
        top_modul_param_list_out.append("module " + top_modul_instantiation_name + " (")
    else:
        top_modul_param_list.append("module " + top_modul_instantiation_name + "#(\n")
        for element in top_module_param_input.split(";"):
            top_modul_param_list.append(element)
        for param in top_modul_param_list:
            param_to_string = str(param)
            if not param_to_string.startswith("module"):
                top_modul_param_list_out.append("\tparameter\t" + param + ",\n")
            else:
                top_modul_param_list_out.append(param)
        top_modul_param_list_out.pop()
        top_modul_param_list_out[len(top_modul_param_list_out) - 1] = str(top_modul_param_list_out[len(top_modul_param_list_out) - 1]).replace(",","")
        top_modul_param_list_out.append(")(\n")
    return top_modul_param_list_out

def set_includes(is_interactive, auto_mode_param):
    if is_interactive == "I":
        print("If you would like to include core files, please type the name, separated with a semicolon, then press enter\n")
        print("(For example: core1.v; core2.v)\n")
        top_module_include = input("If you would not like to include anything, please press enter!\n")
    else:
        top_module_include = auto_mode_param["Files to include"]
    top_module_include = top_module_include.replace(" ", "")
    top_module_include = top_module_include.replace("\n", "")
    top_module_include_separated = top_module_include.split(";")
    top_module_include_list = []
    top_module_include_list.append("\n")
    if not top_module_include_separated == [""]:
        for element in top_module_include_separated:
            top_module_include_list.append("`include \"" + element + "\"\n")
    top_module_include_list.append("\n")
    return top_module_include_list


def writeToFile(output, top_gen_output_path, top_modul_name):
    output_path = ""
    for element in top_gen_output_path:
        output_path += element + "/"

    f = open(output_path + top_modul_name, 'w+')
    if (f.readlines() != ""):
        f.write("")
    f.close()

    f = open(output_path + top_modul_name, 'a')
    f.write(output)
    f.close()


class SourcePreparations(object):

    system_path = ""
    core_path = ""
    source_list = []

    def __init__(self, name, top_gen_output_path, is_interactive):
        self.name = name
        self.top_gen_output_path = top_gen_output_path
        self.is_interactive = is_interactive
        self.setEnvironment()

    def setEnvironment(self):
        home_path = os.environ["HOME"]
        fusesoc_confing_path = home_path + "/.config/fusesoc/fusesoc.conf"
        fusesoc_conf_file = open(fusesoc_confing_path, "r")
        data_path = []

        for line in fusesoc_conf_file:
            data_path.append(line)

        self.fusesoc_system_path = "/" + str(data_path[1]).split(sep="/", maxsplit=1).pop()[:-1]
        self.fusesoc_core_path = "/" + str(data_path[2]).split(sep="/", maxsplit=1).pop()[:-1]


def print_core_parameters(paramlist, top_gen_path, core_name):
    f = open(top_gen_path + core_name, "w")
    for param in paramlist:
        f.write(param)

def print_core_ports(portlist, top_gen_path):
    # Check if connection file exist
    if os.path.isfile(top_gen_path + "top_connections"):
        print("We found an existing connection file. If the list is ready, please enter \"yes\". \n")
        is_connection_file_exists = input("If the list is not up to date, please fix or delete it and restart the process.\n")
    else:
        f = open(top_gen_path + "top_connections")


def top_gen_main():
    auto_mode_params = {}
    core_inst = ""
    top_gen_conf_path = "/home/murai/openrisc/orpsoc-cores-ng/systems/atlys/top_generating/atlys_topgen" #TODO: input("Give the output folder for the top generation!\n")
    top_gen_path_list = top_gen_conf_path.split("/")[:-1]
    top_gen_path = ""
    for element in top_gen_path_list:
        top_gen_path += element

    port_list = []

    is_interactive = input("Interactive (I) or automatic(A) mode?\n")
    if is_interactive == "I":
        top_modul_file_name = input("Give the top module's filename (with extension): \n")
    else:
        auto_mode_param_file_path = automatic_mode_functions.create_auto_mode_param_file(top_gen_path)
        auto_mode_params = automatic_mode_functions.handle_conf_file(auto_mode_param_file_path)
        top_modul_file_name = auto_mode_params["Top module's filename"]
        top_modul_file_name = str(top_modul_file_name).replace(" ", "")
        top_modul_file_name = str(top_modul_file_name).replace("\n", "")

    # Open configuration file
    conf_file_parameters = handle_conf_file.ConfFileParameters(top_gen_conf_path)

    # Set the environment and look for source files
    sourcePreparations = SourcePreparations(conf_file_parameters, top_gen_path, is_interactive)

    # Create the system
    system = system_functions.System()

    # Iterating through the cores
    for i, core_name in enumerate(conf_file_parameters.module_name):
        core = core_functions.IPCore(core_name, conf_file_parameters.rank[i], conf_file_parameters.instantiation_name[i],
                                     sourcePreparations.fusesoc_core_path)
        system.portlist += core.portlist
        print_core_parameters(core.paramlist, top_gen_path, core.core_name)




    # Set the comment if any
    output = set_comment_field(is_interactive, auto_mode_params)

    # Set the top module's includes if any/home/murai/openrisc/top_gen_fusesoc/top_gen_fusesoc
    top_modul_include_list = set_includes(is_interactive, auto_mode_params)
    for element in top_modul_include_list:
        output += element

    # Set the top module's parameters if any
    top_modul_param_list = set_top_modul_params(is_interactive, auto_mode_params)
    for param in top_modul_param_list:
        output += param

    # Create the top.v file
    output += core_inst
    writeToFile(output, top_gen_path, top_modul_file_name)

top_gen_main()

#pycharm test