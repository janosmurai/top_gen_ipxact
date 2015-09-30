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
                    inputs.append(port)
                elif str(self.portdict[port]).split(":")[0] == "out":
                    outputs.append(str(output_num) + ": " + port)
                    output_num += 1
                    # TODO: Ha nincs irany meghatarozva -> kulon lekezelni (pl: clk, rst)

        self.portlist_to_file = inputs + outputs
        print("cica")
