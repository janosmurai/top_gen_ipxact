import xml.etree.ElementTree as ET

def get_port_list(ipxact_path):
    port_list = []

    tree = ET.parse(ipxact_path)
    root = tree.getroot()
    for component in root:
        if "model" in component.tag:
            for model in component:
                if "ports" in model.tag:
                    for port in model:
                        if "port" in port.tag:
                            for element in port:
                                if "name" in element.tag:
                                    port_list.append(element.text)
    return port_list

def get_parameter_list(ipxact_path):
    parameter_list = []

    tree = ET.parse(ipxact_path)
    root = tree.getroot()
    for component in root:
        if "model" in component.tag:
            for model in component:
                if "modelParameters" in model.tag:
                    for port in model:
                        if "modelParameter" in port.tag:
                            for element in port:
                                if "name" in element.tag:
                                    parameter_list.append(element.text)
    return parameter_list

