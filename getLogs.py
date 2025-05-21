from netmiko import ConnectHandler
import datetime
import os

log_datetime = datetime.datetime.now().strftime("%d-%b-%Y %I:%M:%S %p")

def cisco_device(hostIP):
    try:
        now = datetime.datetime.now()
        date = now.strftime("%b") + " " + str(now.day)
    
        cisco_switches = {
            'device_type': 'cisco_ios',
            'host': hostIP,
            'username': '', #put here your cisco username
            'password': '', #put here your cisco password
            'port': 22
        }
        
        open_connection = ConnectHandler(**cisco_switches)
        logs = open_connection.send_command(f"show logging | i {date}(.*Broadcast)")

        if logs:
            with open("BSlogs.txt", "a") as file:
                file.write(f"{hostIP}\n")
                file.write(f"{logs}\n\n")
        else:
            with open("BSlogs.txt", "a") as err_file:
                err_file.write(f"{hostIP}\n")
                err_file.write("No Broadcast Storm logs.\n\n")
        
    except Exception as e:
        print(f"An error occurred on {hostIP}: {e}\n")
    
if os.path.exists("BSlogs.txt"):
    os.remove("BSlogs.txt")

hostnames = ['0.0.0.0','1.1.1.1'] #put all the Host IPs that you want to remote.

with open("BSlogs.txt", "w") as file:
    file.write(f"Logging started at {log_datetime}\n")
    file.write("File:\n")
    file.write("-------------------------------------------------------------------------------\n")

for hostname in hostnames:
    cisco_device(hostname)