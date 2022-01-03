import re
import os

class GetHardwareInfo():
    def __init__(self):
        self.mem_output = os.popen("sudo dmidecode -t 17").read()
        self.cpu_output = os.popen("sudo dmidecode -t processor").read()
        self.gpu_output = os.popen('glxinfo | egrep "OpenGL vendor string:|Dedicated video memory|Version:|OpenGL renderer string:"').read()
        self.motherboard_output = os.popen("sudo dmidecode -t baseboard").read()
        self.vendor_id = os.popen("lspci -vn | grep VGA").read()
        self.vendor_id = re.findall(r"(?<=0300: ).*(?=\(rev)", self.vendor_id)[0].split(":")[0]

        self.mem_info = {}
        self.cpu_info = {}
        self.gpu_info = {}
        self.motherboard_info = {}


    def get_mem_info(self):
        self.mem_info.update({"form_factor": re.findall(r"(?<=Form\sFactor:\s).*",
                        self.mem_output)[0]})
        self.mem_info.update({"manufacturer": re.findall(r"(?<=Manufacturer:\s).*", self.mem_output)[0]})
        self.mem_info.update({"serial_number": re.findall(r"(?<=Serial\sNumber:\s).*", self.mem_output)[0]})
        self.mem_info.update({"voltage": re.findall(r"(?<=Configured\sVoltage:\s).*", self.mem_output)[0]})
        if self.mem_info["voltage"] == "1.35":
            voltage = f'{re.findall(r"(?<=Type: ).*", self.mem_output)[0]}L'
            self.mem_info.update({"type": voltage})
        else:
            self.mem_info.update({"type": re.findall(r"(?<=Type:\s).*", self.mem_output)[0]})

        self.mem_info.update({"size": re.findall(r"(?<=Size:\s).*", self.mem_output)[0]})

    def get_cpu_info(self):

        self.cpu_info.update({"name": re.findall(r"(?<=Version:\s).*",
                self.cpu_output)[0]})
        self.cpu_info.update({"socket": re.findall(r"(?<=Socket\sDesignation: Socket\s).*",
                        self.cpu_output)[0]})
        self.cpu_info.update({"family": re.findall(r"(?<=Family:\s).*",
                        self.cpu_output)[0]})
        self.cpu_info.update({"manufacturer": re.findall(r"(?<=Manufacturer:\s).*",
                self.cpu_output)[0]})
        self.cpu_info.update({"clock_speed": re.findall(r"(?<=Max\sSpeed:\s).*",
                self.cpu_output)[0]})
        self.cpu_info.update({"cores": re.findall(r"(?<=Core\sCount:\s).*",
                        self.cpu_output)[0]})
        self.cpu_info.update({"threads": re.findall(r"(?<=Thread\sCount:\s).*",
                        self.cpu_output)[0]})

    def get_gpu_info(self):
        if self.vendor_id == "1002":
            self.gpu_info.update({"vendor": "AMD"})
        elif self.vendor_id == "10de":
            self.gpu_info.update({"vendor": "NVIDIA"})
        elif self.vendor_id == "8086":
            self.gpu_info.update({"vendor": "Intel"})
        else:
            self.gpu_info.update({"vendor": "Unknown"})

        self.gpu_info.update({"memory": re.findall(r"(?<=Dedicated video memory: ).*",
                        self.gpu_output)[0]})
        self.gpu_info.update({"product": re.findall(r"(?<=controller: ).*(?=\(rev )",
                        os.popen("lspci | grep VGA").read())[0]})

        vendors = ["NVIDIA Corporation", "Advanced Micro Devices, Inc.", "Intel Corporation"]

        for vendor in vendors:
            if vendor in self.gpu_info["product"]:
                self.gpu_info["product"] = self.gpu_info["product"].replace(vendor, "")

    def get_motherboard_info(self):
        self.motherboard_info.update({"manufacturer": re.findall(r"(?<=Manufacturer:\s).*",
                        self.motherboard_output)[0]})
        self.motherboard_info.update({"serial_number": re.findall(r"(?<=Serial\sNumber:\s).*",
                        self.motherboard_output)[0]})
        self.motherboard_info.update({"version": re.findall(r"(?<=Version:\s).*",
                        self.motherboard_output)[0]})
        self.motherboard_info.update({"asset_tag": re.findall(r"(?<=Asset\sTag:\s).*",
                        self.motherboard_output)[0]})
        self.motherboard_info.update({"product": re.findall(r"(?<=Product\sName:\s).*",
                        self.motherboard_output)[0]})






