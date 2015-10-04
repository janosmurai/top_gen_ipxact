import xml.etree.ElementTree as ET

def get_port_dict(ipxact_path):
    port_dict = {}

    tree = ET.parse(ipxact_path)
    root = tree.getroot()
    for component in root:
        if "model" in component.tag:
            for model in component:
                if "ports" in model.tag:
                    for port in model:
                        if "port" in port.tag:
                            name = ""
                            direction = ""
                            length = ""
                            for element in port:
                                if "name" in element.tag:
                                    name = element.text
                                elif "wire" in element.tag:
                                    for param in element:
                                        if "direction" in param.tag:
                                            direction = param.text
                                        elif "vector" in param.tag:
                                            for dir in param:
                                                if "left" in dir.tag:
                                                    length = dir.text
                            port_dict[name] = direction + ":" + length
    return port_dict

def get_parameter_dict(ipxact_path):
    parameter_dict = {}

    tree = ET.parse(ipxact_path)
    root = tree.getroot()
    for component in root:
        if "model" in component.tag:
            for model in component:
                if "modelParameters" in model.tag:
                    for port in model:
                        if "modelParameter" in port.tag:
                            name = ""
                            value = ""
                            for element in port:
                                if "name" in element.tag:
                                    name = element.text
                                elif "value" in element.tag:
                                    value = element.text
                            parameter_dict[name] = value
    return parameter_dict

def get_bus_interface_types(ipxact_path):

    bus_interface_types = []

    tree = ET.parse(ipxact_path)
    root = tree.getroot()
    for component in root:
        if "busInterfaces" in component.tag:
            for busInterface in component:
                if "busInterface" in busInterface.tag:
                    for element in busInterface:
                        if "name" in element.tag:
                            bus_interface_types.append(element.text)

    if len(bus_interface_types) > 1:
        print("We found more then one bus interface:\n")
        for bus_i in bus_interface_types:
            print(bus_i)
        corrected_bus_i = input("Type the names of the desired bus interfaces, separated with a semicolon!\nIf you want them "
                                "all, then just press enter!\n")
        if not corrected_bus_i == "":
            corrected_bus_i = corrected_bus_i.replace(" ", "")
            bus_interface_types = corrected_bus_i.split(";")

    return bus_interface_types

def get_bus_interface_dict(ipxact_path, bus_interface_types):
    bus_interface_dict = {}
    tree = ET.parse(ipxact_path)
    root = tree.getroot()
    for component in root:
        if "busInterfaces" in component.tag:
            for busInterface in component:
                bus_name = ""
                actual_bus_interface_dict = {}
                if "busInterface" in busInterface.tag:
                    for element in busInterface:
                        if "name" in element.tag:
                            bus_name = element.text
                        elif "portMaps" in element.tag:
                            for portMap in element:
                                if "portMap" in portMap.tag:
                                    for port in portMap:
                                        if "physicalPort" in port.tag:
                                            name = ""
                                            length = ""
                                            direction = ""
                                            for param in port:
                                                if "name" in param.tag:
                                                    name = param.text
                                                elif "vector" in param.tag:
                                                    for dir in param:
                                                        if "left" in dir.tag:
                                                            length = dir.text
                                            if name.endswith("i"):
                                                direction = "in"
                                            elif name.endswith("o"):
                                                direction = "out"
                                            actual_bus_interface_dict[name] = direction + ":" + length + ":" + bus_name

                if bus_name in bus_interface_types:
                    bus_interface_dict.update(actual_bus_interface_dict)

    return bus_interface_dict
