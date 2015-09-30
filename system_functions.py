class System:
    def __init__(self):
        self.portdict = {}
        self.bus_interface_dict = {}
        self.portlist_to_file = []

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
