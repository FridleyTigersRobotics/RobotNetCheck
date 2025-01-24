import subprocess
import itertools
import time
import sys
import requests
import json
from termcolor import colored
import socket

#if library not found: "py -m pip install library_name" (replace library_name with the name of the missing library)

def get_team_number():
    while True:
        # Get the team number from user input
        team_number = input("Please enter a four digit team number: ")
        
        # Check if the team number is four digits long
        if len(team_number) == 4 and team_number.isdigit():
            return team_number
        else:
            print("Invalid team number. Please try again.")

def split_team_number(team_number):
    first_two_digits = int(team_number[:2])
    last_two_digits = int(team_number[2:])
    
    return first_two_digits, last_two_digits

def get_json(ip):
    try:
        response = requests.get('http://' + ip + '/status')
        data = json.loads(response.text)
        return data
    except Exception as e:
        print("Error occurred while connecting to the IP address or loading JSON data.")
        print(str(e))
        return None

def display_info(ip):
    ip_components = ip.split('.')
    lastaddr=ip_components[-1]

    if (lastaddr=="1"):
        print(colored("VH-109 robot radio found, showing status:",'green'))
        json_data = get_json(ip)
        if json_data is not None:
            print(json.dumps(json_data, indent=4))  # pretty-printing JSON

    elif (lastaddr=="2"):
        print(colored("roboRIO found",'green'))

    elif (lastaddr=="4"):
        print(colored("VH-109 team access point radio found, showing status:",'green'))
        json_data = get_json(ip)
        if json_data is not None:
            print(json.dumps(json_data, indent=4))  # pretty-printing JSON

    elif (lastaddr=="20"):
        print(colored("2227 BotBay Router found",'green'))
    
    else:
        print(colored("unknown active device found:",'red'))
        print(colored(ip,'red'))

def get_ip():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return host_name, ip_address

#begin main code
team_number = get_team_number()
d1, d2 = split_team_number(team_number)
spinner = itertools.cycle(['-', '/', '|', '\\'])
host_name, ip_address = get_ip()
print("Computer Host Name: " + host_name)
print("IP Address: " + ip_address)
print(colored("scanning FRC static IPs (1-19)...",'yellow'))

for i in range(1, 21):
    ip = f"10.{d1}.{d2}.{i}"
    response = subprocess.call(['ping', '-n', '1', '-w', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if response == 0:
        print(colored(f"\rPing to {ip} successful.",'blue'))
        display_info(ip)
        
    else:
        sys.stdout.write("\r" + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)

print(colored("DONE",'yellow'))
input("Press Enter to exit...")
