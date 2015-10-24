import os

def call_wb_intercon_gen(top_gen_path):
    wb_intercon_path = os.getcwd()
    wb_intercon_path += "/wb_intercon_gen/"
    system_path_list = top_gen_path.split("/")[:-2]
    rtl_path = ""
    for element in system_path_list:
        rtl_path += "/" + element
    rtl_path += "/rtl/verilog"
    os.system("python " + wb_intercon_path + "wb_intercon_gen " + wb_intercon_path + "wb_intercon.conf " + rtl_path +
              "/wb_intercon.v")



call_wb_intercon_gen("/home/murai/openrisc/orpsoc-cores-ng/systems/atlys/top_generating/atlys_topgen")
