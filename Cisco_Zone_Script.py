import paramiko
import pandas as pd
import time
from getpass import getpass
passwd = getpass()

def alias_F1():
    config_commands_F1 = ["vsan database",
                          "vsan 2"
                         ]
    for x in range(len(alias_all_f1)):
        if str(alias_all_f1[x]) == 'nan':
            break
        added_item1 = ("fcalias name " + str(alias_all_f1[x]) + " vsan 2")
        config_commands_F1.append(added_item1)
        added_item2 = ("member pwwn " + str(wwpn_all_f1[x]))
        config_commands_F1.append(added_item2)
    return config_commands_F1

def alias_F2():
    config_commands_F2 = ["vsan database",
                          "vsan 2"
                         ]
    for x in range(len(alias_all_f2)):
        if str(alias_all_f2[x]) == 'nan':
            break
        added_item1 = ("fcalias name " + alias_all_f2[x] + " vsan 2")
        config_commands_F2.append(added_item1)
        added_item2 = ("member pwwn " + wwpn_all_f2[x])
        config_commands_F2.append(added_item2)
    return config_commands_F2

def zone_F1():
    config_commands_F1 = ["vsan database",
                          "vsan 2"
                         ]
    zone_list_F1 = ["zoneset name PRODZONESET_SAN01 vsan 2"]
    for x in Tar_Alias_f1:
        if pd.isna(x):
            break
        for y in Init_Alias_f1:
            if pd.isna(y):
                break
            output = str(x) + "_" + str(y)
            zone_list_F1.append("member " + output)
            added_item1 = ("zone name " + output + " vsan 2")
            config_commands_F1.append(added_item1)
            added_item2 = ("member fcalias " + str(x))
            config_commands_F1.append(added_item2)
            added_item3 = ("member fcalias " + str(y))
            config_commands_F1.append(added_item3)
    config_commands_F1.extend(zone_list_F1)
    return config_commands_F1
    

def zone_F2():
    config_commands_F2 = ["vsan database",
                          "vsan 2"
                         ]
    zone_list_F2 = ["zoneset name PRODZONESET_SAN02 vsan 2"]
    for x in Tar_Alias_f2:
        if pd.isna(x):
            break
        for y in Init_Alias_f2:
            if pd.isna(y):
                break
            output = str(x) + "_" + str(y)
            zone_list_F2.append("member " + output)
            added_item1 = ("zone name " + output + " vsan 2")
            config_commands_F2.append(added_item1)
            added_item2 = ("member fcalias " + str(x))
            config_commands_F2.append(added_item2)
            added_item3 = ("member fcalias " + str(y))
            config_commands_F2.append(added_item3)
    config_commands_F2.extend(zone_list_F2)
    return config_commands_F2

def configure_cisco_switch(ip, username, password, commands):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port=22, username=username, password=password, look_for_keys=False)
    ssh_shell = ssh.invoke_shell()
    ssh_shell.send("config t\n")
    ssh_shell.send("")
    time.sleep(0.1)

    for command in commands:
        ssh_shell.send(command + "\n")
        time.sleep(0.1)
    ssh_shell.send("end\n")
    ssh_shell.send("exit\n")

    #output = ""
    #while ssh_shell.recv_ready():
    #    output += ssh_shell.recv(1024).decode()

    ssh.close()
    #return output

if __name__ == "__main__":
    i = 1
    username = "admin"
    password = passwd
    excel_file_path = 'Zone_Cisco_SS_List.xlsx'
    df1 = pd.read_excel(excel_file_path, sheet_name='Alias')
    df2 = pd.read_excel(excel_file_path, sheet_name='Zone')
    wwpn_all_f1 = df1['WWPN_F1'].tolist()
    alias_all_f1 = df1['Alias_F1'].tolist()
    Tar_Alias_f1 = df2['TarAlias_F1'].tolist()
    Init_Alias_f1 = df2['InitAlias_F1'].tolist()
    wwpn_all_f2 = df1['WWPN_F2'].tolist()
    alias_all_f2 = df1['Alias_F2'].tolist()
    Tar_Alias_f2 = df2['TarAlias_F2'].tolist()
    Init_Alias_f2 = df2['InitAlias_F2'].tolist()
    while i <= 1:
        req = str(input("1: Create Alias\n2: Create Zone\n3: Create Alias and Zone\n4: Exit\nEnter your choice: "))
        if req != "1" and req != "2" and req != "3" and req != "4":
            print("Wrong Choice")
            break
        if req == "4":
            print("Bye")
            break
        fab = input("Enter the Fabric 1/2 : ")
        if fab == "1":
            switch_ip = "192.168.1.180"
            if req == "1":
                config_comm = alias_F1()
                configure_cisco_switch(switch_ip,username,password,config_comm)
            elif req == "2":
                config_comm = zone_F1()
                configure_cisco_switch(switch_ip,username,password,config_comm)
            elif req == "3":
                config_comm = alias_F1()
                configure_cisco_switch(switch_ip,username,password,config_comm)
                config_comm = zone_F1()
                configure_cisco_switch(switch_ip,username,password,config_comm)
            elif req == "4":
                break
            #else:
             #   print("Wrong Choice")
        elif fab == "2":
            switch_ip = "192.168.1.181"
            if req == "1":
                config_comm = alias_F2()
                configure_cisco_switch(switch_ip,username,password,config_comm)
            elif req == "2":
                config_comm = zone_F2()
                configure_cisco_switch(switch_ip,username,password,config_comm)
            elif req == "3":
                config_comm = alias_F2()
                configure_cisco_switch(switch_ip,username,password,config_comm)
                config_comm = zone_F2()
                configure_cisco_switch(switch_ip,username,password,config_comm)
            elif req == "4":
                break
            #else:
             #   print("Wrong Choice")
        else:
                print("Wrong Choice")