import os


def call_wb_intercon_gen(top_gen_path):
    wb_intercon_path = os.getcwd() + "/wb_intercon_gen/"
    system_path_list = top_gen_path.split("/")[:-2]
    rtl_path = ""
    for element in system_path_list:
        rtl_path += "/" + element
    rtl_path += "/rtl/verilog"
    os.system("python " + wb_intercon_path + "wb_intercon_gen " + wb_intercon_path + "wb_intercon.conf " + rtl_path +
              "/wb_intercon.v")


def create_wb_intercon_conf(core_names, ranks):
    wb_intercon_path = os.getcwd() + "/wb_intercon_gen/"

    # Get the masters
    wb_conf = "; --- MASTRERS ---\n"
    for i, core_name in enumerate(core_names):
        if ranks[i] == "master":
            wb_conf += "[master " + core_name + "]\nslaves = \n \n"

    # Get the slaves
    wb_conf += "; --- SLAVES ---\n"
    for i, core_name in enumerate(core_names):
        if ranks[i] == "slave":
            wb_conf += "[slave " + core_name + "]\ndatawidth = \noffset = \nsize = \n"

    if os.path.isfile(wb_intercon_path + "wb_intercon.conf"):
        print("We found an existing config file.\n If the file is ready, please press enter.\n")
        input("If the file is not up to date, please fix or delete it and restart the process.\n")
    else:
        f = open(wb_intercon_path + "wb_intercon.conf", "w")
        f.write(wb_conf)
        f.close()
    print("\nPlease fill up the config file, which is available in the " + wb_intercon_path + " folder.")
    input("\nIf the list is ready, please press enter!\n")