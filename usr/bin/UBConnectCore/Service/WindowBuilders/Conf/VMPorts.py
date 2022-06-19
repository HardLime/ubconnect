import subprocess
class Rule:
    def __init__(self, name, type, host_ip, host_port, guest_ip, guest_port):
        self.name = name
        self.type = type
        self.host_ip = host_ip
        self.host_port = host_port
        self.guest_ip = guest_ip
        self.guest_port = guest_port

class ConfigureRules:
    def get_rule_list(self, vmname):
        #куча массивов
        names = subprocess.getoutput(f"v=$(a=$(VBoxManage showvminfo \"{vmname}\" | grep NIC | grep Rule); awk -F ':   ' '{{print $2}}' <<< $a); awk -F '=|,' '{{print $2}}' <<< $v").split("\n")
        types = subprocess.getoutput(f"v=$(a=$(VBoxManage showvminfo \"{vmname}\" | grep NIC | grep Rule); awk -F ':   ' '{{print $2}}' <<< $a); awk -F '=|,' '{{print $4}}' <<< $v").split("\n")
        hosts_ip = subprocess.getoutput(f"v=$(a=$(VBoxManage showvminfo \"{vmname}\" | grep NIC | grep Rule); awk -F ':   ' '{{print $2}}' <<< $a); awk -F '=|,' '{{print $6}}' <<< $v").split("\n")
        hosts_ports = subprocess.getoutput(f"v=$(a=$(VBoxManage showvminfo \"{vmname}\" | grep NIC | grep Rule); awk -F ':   ' '{{print $2}}' <<< $a); awk -F '=|,' '{{print $8}}' <<< $v").split("\n")
        guest_ip = subprocess.getoutput(f"v=$(a=$(VBoxManage showvminfo \"{vmname}\" | grep NIC | grep Rule); awk -F ':   ' '{{print $2}}' <<< $a); awk -F '=|,' '{{print $10}}' <<< $v").split("\n")
        guest_ports = subprocess.getoutput(f"v=$(a=$(VBoxManage showvminfo \"{vmname}\" | grep NIC | grep Rule); awk -F ':   ' '{{print $2}}' <<< $a); awk -F '=|,' '{{print $12}}' <<< $v").split("\n")
        #основной список
        rules_list = []
        i = 0
        for item in range(len(names)):
            temp = Rule(names[i], types[i], hosts_ip[i], hosts_ports[i], guest_ip[i], guest_ports[i])
            rules_list.append(temp)
            i = i+1
        #чистим память
        del names
        del types
        del hosts_ip
        del hosts_ports
        del guest_ip
        del guest_ports
        return rules_list

    def create_rule(self, rule, vm_name):
        subprocess.getoutput(f"VBoxManage modifyvm \"{vm_name}\" --natpf1 \"{rule.name},{rule.type},{rule.host_ip},{rule.host_port},{rule.guest_ip},{rule.guest_port}\"")

    def delete_rule(self, rule_name, vm_name):
        subprocess.getoutput(f"VBoxManage modifyvm \"{vm_name}\" --natpf1 delete \"{rule_name}\"")
