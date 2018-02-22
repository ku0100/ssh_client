#!/usr/local/env python3.4

import time
import paramiko
import getpass
from netmiko import ConnectHandler
from mac_netmri import *

class sshClient(object):

    def __init__(self):
        self.device_type = "cisco_ios"
        self.enable_pw = "enable_password_for_devices"
        self.port = 22

    def client_login(self, hostname, username, password):
        sshClient = paramiko.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshClient.load_system_host_keys()
        cisco_device = {"device_type": self.device_type,
                        "ip": hostname,
                        "username": username,
                        "password": password
                        "secret": self.enable_pw}
        print("Connecting to device...")
        net_device = ConnectHandler(**cisco_device)
        net_device.enable()
        
        while True:
            command = input(hostname + "#")
            if command.lower() == "exit":
                exitClient(device=net_device)
            elif command.lower().startswith("con"):
                output = net_device.send_config_set(command,
                                    exit_config_mode=False)
                print(output)
                while True:
                    command = input(hostname + "(config)#")
                    if command.lower() == "exit":
                        net_device.exit_config_mode()
                        break
                    elif command.lower().startswith("int"):
                        output = net_device.send_config_set(command,
                                            exit_config_mode=False)
                        print(output)
                        while True:
                            command = input(hostname + "(config-if)#")
                            if command.lower() == "exit":
                                net_device.exit_config_mode()
                                break
                            else:
                                output = net_device.send_config_set(
                                            command,
                                            exit_config_mode=False)
                                print(output)
                    else:
                        output = net_device.send_config_set(command)
            else:
                output = net_device.send_config_set(command)
                print(output)
                continue

def returnFunction(self, device, save_changes):
    if save_changes:
        message = "[Config changes saved]"
    else:
        message = "[Config changes NOT saved]"
    print("%s. Returning to MAC_NetMRI..." % (message))
    # close ssh connection first
    device.disconnect()
    time.sleep(3)
    addressSearch()

def exitClient(self, device):
    while True:
        save_changes = input("Save any config changes? (y/n)>>> ")
        if save_changes.lower() == "y":
            output = device.send_command("copy run start")
            print(output)
            returnFunction(device, save_changes=True)
            break
        else:
            returnFunction(device, save_changes=False)
            break