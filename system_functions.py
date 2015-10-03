class System:
    def __init__(self):
        self.portdict = {}
        self.bus_interface_dict = {}
        self.portlist_to_file = []
        self.updated_portdict = {}
        self.wires = {}
        self.default_parameters = {}
        self.updated_parameters = {}
        self.cores = []
        self.instatiation_names = []
        self.rank = []

    def create_connection_file(self):
        inputs = []
        outputs = []
        output_num = 0
        for port in self.portdict:
            if port not in self.bus_interface_dict:
                if str(self.portdict[port]).split(":")[0] == "in":
                    inputs.append(port + ":TOP")
                elif str(self.portdict[port]).split(":")[0] == "out":
                    outputs.append(port + ":TOP")
                    # TODO: Ha nincs irany meghatarozva -> kulon lekezelni (pl: clk, rst)

        self.portlist_to_file = inputs + outputs

    def create_final_text(self):
        final_text = ""
        # Initialize wires
        # wire = {name, width}
        for wire in self.updated_portdict:
            wire_name = self.updated_portdict[wire]
            wire_width = ""
            for port in self.portdict:
                if port == wire:
                    wire_width = str(self.portdict[port]).split(":")[1]
            if not wire_width == "0":
                final_text += "wire\t[" + wire_width + "]\t" + wire_name + "\n"
            else:
                final_text += "wire\t\t" + wire_name + "\n"

        for i, core in enumerate(self.cores):
            # Get the current core parameters
            current_core = False
            current_params = {}
            for param in self.updated_parameters:
                if self.updated_parameters[param] == "new_core":
                    if param == core:
                        current_core = True
                    else:
                        current_core = False

                if current_core:
                    current_params[param] = self.updated_parameters[param]
            # If only the current core name is in the parameter list
            if len(current_params) == 1:
                final_text += core + " " + self.instatiation_names[i] + "(\n"
            else:
                final_text += core + " #(\n"
                for param in current_params:
                    isnumeric = False
                    for num in range(10):
                        if str(current_params[param]).startswith(str(num)):
                            final_text += "\t." + param + "(" + current_params[param] + "),\n"
                            isnumeric = True

                    if not isnumeric:
                        final_text += "\t." + param + "(\"" + current_params[param] + "\"),\n"
                final_text += ") " + self.instatiation_names[i] + " (\n"

            # Get the current core buses
            current_core = False
            current_buses = {}
            for bus in self.bus_interface_dict:
                if self.bus_interface_dict[bus] == "new_core":
                    if bus == core:
                        current_core = True
                    else:
                        current_core = False

                if current_core:
                    current_buses[bus] = self.bus_interface_dict[bus]
            for bus in current_buses:
                (direction, bus_name) = str(current_buses[bus]).split(":")[0:-1]
                wire_name = str(bus).split(_)[0]
                if self.rank == "slave":
                    if direction == "in":
                        final_text += "\t." + bus + "(" + bus_name + "_m2s_" + core + wire_name + "),\n"
                    else:
                        final_text += "\t." + bus + "(" + bus_name + "_s2m_" + core + wire_name + "),\n"
                else:
                    if direction == "out":
                        final_text += "\t." + bus + "(" + bus_name + "_m2s_" + core + wire_name + "),\n"
                    else:
                        final_text += "\t." + bus + "(" + bus_name + "_s2m_" + core + wire_name + "),\n"

            # Get the current core wires
            is_input = False
            current_core = False
            current_ports = {}
            for port in self.updated_portdict:
                if self.updated_portdict[port] == "INPUTS":
                    is_input == True
            if is_input:
                for port in self.updated_portdict:
                    if self.updated_portdict[port] == "new_core":
                        if bus == core:
                            current_core = True
                            is_input = False
                        else:
                            current_core = False

                    if current_core:
                        current_ports[port] = self.updated_portdict[bus]
            final_text += "//INPUTS:"
            for port in current_ports:
                final_text += "\t." + port + "(" + current_ports[port] + "),\n"
            final_text = final_text[:-2]
            final_text += "\n);"

        return  final_text

    def create_common_paramdict(self, core_name, paramdict):
        tmp_paramdict = {}
        for param in paramdict:
            # TODO: A core_name erteket hamarabb kell hozzadni, mert kell a beolvasasos-osszehasonlitasos resznel
            tmp_paramdict[core_name + param] = param

        self.updated_parameters.update(tmp_paramdict)
        pass