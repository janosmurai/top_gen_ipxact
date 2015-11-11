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
        self.bus_types = ""

    def create_connection_file(self):
        inputs = []
        outputs = []
        inputs.append("--- INPUTS ---\n")
        outputs.append("\n--- OUTPUTS ---\n")

        interface_list = []
        for bus in self.bus_interface_dict:
            interface_list.append(str(bus).split(":")[1])

        for port in sorted(self.portdict):
            port_name = str(port).split(":")[1]
            if port_name not in interface_list:
                if str(self.portdict[port]).split(":")[0] == "in":
                    inputs.append(port + ":in(TOP)")
                elif str(self.portdict[port]).split(":")[0] == "out":
                    outputs.append(port + ":out(TOP)")
                else:
                    outputs.append(port + ":(TOP)")
        self.portlist_to_file = inputs + outputs

    def create_final_text(self):
        final_text = ""
        final_text = self.set_top_modul_ports(final_text)
        final_text = self.set_final_wires(final_text)
        for i, core in enumerate(self.cores):
            final_text = self.set_final_parameters(final_text, i, core)
            final_text = self.set_final_buses(final_text, core)
            final_text = self.set_final_ports(final_text, core)

        return  final_text

    def set_top_modul_ports(self, final_text):
        inputs = ""
        outputs = ""
        inouts = ""
        for wire in self.updated_portdict:
            wire_name = self.updated_portdict[wire]
            port_name = str(wire).split(":")[0] + ":" + str(wire).split(":")[1]
            port_direction = str(wire).split(":")[2]
            #Get port width
            port_width = ""
            for port in self.portdict:
                if port in wire:
                    port_width = str(self.portdict[port]).split(":")[1]
            if wire_name == "TOP":
                wire_name = port_name.split(":")[1]
                if port_width == "0":
                    if port_direction == "in":
                        inputs += "\t" + port_direction + "put\t\t" + wire_name + "_pin,\n"
                    elif port_direction == "out":
                        outputs += "\t" + port_direction + "put\t\t" + wire_name + "_pin,\n"
                    else:
                        inouts += "\tinout\t\t" + wire_name + "_pin,\n"
                else:
                    if port_direction == "in":
                        inputs += "\t" + port_direction + "put [" + port_width + ":0]\t" + wire_name + "_pin,\n"
                    elif port_direction == "out":
                        outputs += "\t" + port_direction + "put [" + port_width + ":0]\t" + wire_name + "_pin,\n"
                    else:
                        inouts += "\tinout [" + port_width + ":0]\t" + wire_name + "_pin,\n"
        final_text = inputs + outputs + inouts
        final_text = final_text[:-2]
        final_text += "\n);\n\n"

        return final_text

    def set_final_wires(self, final_text):
        # Initialize wires
        # wire = {name, width}
        for wire in self.updated_portdict:
            wire_name = self.updated_portdict[wire]
            port_name = str(wire).split(":")[0] + ":" + str(wire).split(":")[1]
            if wire_name == "TOP":
                wire_name = port_name.split(":")[1] + "_pin"
            wire_width = ""
            if not wire_name == "NOT_USED":
                for port in self.portdict:
                    if port == port_name:
                        wire_width = str(self.portdict[port]).split(":")[1]
                if not wire_width == "0":
                    final_text += "wire\t[" + wire_width + ":0]\t" + wire_name + "\n"
                else:
                    final_text += "wire\t\t" + wire_name + "\n"

        return  final_text

    def set_final_parameters(self, final_text, i, core):
        # Get the current core parameters
        current_params = {}
        for param in self.updated_parameters:
            if str(param).startswith(core):
                current_params.update({str(param).split(":")[1]: self.updated_parameters[param]})

        # If only the current core name is in the parameter list
        if len(current_params) == 0:
            final_text += "\n" + core + " " + self.instatiation_names[i] + "(\n"
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
            final_text = final_text[:-2]
            final_text += "\n) " + self.instatiation_names[i] + " (\n"
        return final_text

    def set_final_buses(self, final_text, core):
         # Get the current core buses
        current_buses = {}
        for bus in self.bus_interface_dict:
            if str(bus).startswith(core):
                current_buses.update({str(bus).split(":")[1]: self.bus_interface_dict[bus]})

        for bus in current_buses:
            bus_name = str(current_buses[bus]).split(":")[2]
            direction = str(current_buses[bus]).split(":")[0]
            wire_name = str(bus).split("_")[0]
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

        return final_text

    def set_final_ports(self, final_text, core):
         # Get the current core ports
        current_ports = {}
        for port in self.updated_portdict:
            if str(port).startswith(core):
                current_ports.update({str(port).split(":")[1]: self.updated_portdict[port]})

        for port in current_ports:
            if current_ports[port] == "TOP":
                final_text += "\t." + port + "(" + port + "_pin),\n"
            elif not current_ports[port] == "NOT_USED":
                final_text += "\t." + port + "(" + current_ports[port] + "),\n"
        final_text = final_text[:-2]
        final_text += "\n);"
        return  final_text