#!/bin/bash

hostname=$(hostname)
user=$(whoami)

clear
echo
echo
cat << "EOF"
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
     __          ___      _                      _  _       _       __ 
    | _|  _ __  / _ \ ___| |_          __      _| || |  ___| |__   |_ |
    | |  | '_ \| | | / __| __|  _____  \ \ /\ / / || |_/ __| '_ \   | |
    | |  | |_) | |_| \__ \ |_  |_____|  \ V  V /|__   _\__ \ | | |  | |
    | |  | .__/ \___/|___/\__|           \_/\_/    |_| |___/_| |_|  | |
    |__| |_|                                                       |__|
                            [p0st-w4sh]:[v1]
                          [d3k@t3ss3r4]:[2024]
                            [hack.the.planet]
                    [all.your.nekworkz.are.belong.us]

|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
EOF

read -p $'\n[?]:['$user', Reset monitor link iface and network config?]:[y/n]\n' -r
echo
echo
echo
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sleep .5
    echo -e "\n[O]:[Resetting iface and networking.]"
    echo -e "[.]:[...]"
    sleep .5
    echo -e "\n[x]:[airmon-ng]:[Disabling and resetting monitor link.]"
    sudo airmon-ng stop "wlan1mon"
    echo -e "[.]:[...]"
    sleep 1.5
    echo -e "[x]:[airmon-ng]:[Monitor link down.]\n"
    sleep .5
    echo -e "\n[x]:[Systemctl]:[Restarting dhcpcd.service.]" >&2
    echo -e "[.]:[...]"
    sudo systemctl restart dhcpcd.service
    sleep .5
    echo -e "[x]:[Systemctl]:[dhcpcd.service active.]\n" >&2
    sleep .5
    echo -e "\n[x]:[Systemctl]:[Restarting networking.service.]" >&2
    echo -e "[.]:[...]"
    sudo systemctl restart networking.service
    sleep .5
    echo -e "[x]:[Systemctl]:[networking.service active.]\n" >&2
    sleep .5
    echo -e "\n[x]:[Systemctl]:[Restarting NetworkManager.]" >&2
    echo -e "[.]:[...]"
    sudo systemctl restart NetworkManager
    sleep .5
    echo -e "[x]:[Systemctl]:[NetworkManager active.]\n" >&2
    sleep 1
    clear
    echo -e "\n[+]:[cyb3rd3ck '$hostname' is ready to run, '$user'.]\n" >&2
    read -p $'\n[?]:[Do you want to deploy another tool?]:\n[y/n]\n' -n 1 -r
echo
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # For personal config, replace the below options with your preferred names for the tools you want.
    read -p $'\n[?]:['$user'Choose your weapon wisely.]:\n[1]:[bettercap]\n[2]:[wifiphisher]\n[3]:[pyphisher]\n[4]:[wifipumpkin3]\n[5]:[routersploit]\n[6]:[BeEF]\n[X]:[Exit]\n' -n 1 -r
    echo
    case $REPLY in
            [1])
                # Insert name of tool 1 on next line.
                echo -e "\n[+]:[Arming bettercap.]\n" >&2
                sleep .5
                echo -e "[.]:[...]"
                # Insert command to launch desired tool. This would require different paths, depending on aliasing etc. 
                # PLease note this, if you are not an experienced linux user and know how to set up aliases (stop trying to steal yourneighbors wifi and do your homework), using my commands will not work because they rely on MY aliasing in-system.
                sudo bettercap
                ;;
            [2])
                echo -e "\n[+]:[Arming wifiphisher.]\n" >&2
                sleep .5
                echo -e "[.]:[...]"
                sudo wifiphisher
                ;;
            [3])
                echo -e "\n[+]:[Arming pyphisher.]\n" >&2
                sleep .5
                echo -e "[.]:[...]"
                sudo pyphisher
                ;;
            [4])
                echo -e "\n[+]:[Arming wifipumpkin3.]\n" >&2
                sleep .5
                echo -e "[.]:[...]"
                sudo wifipumpkin3 
                ;;
            [5])
                echo -e "\n[+]:[Arming routersploit.]\n" >&2
                sleep .5
                echo -e "[.]:[...]"
                sudo rsf.py
                ;;
            [6])
                echo -e "\n[+]:[Arming BeEF]\n" >&2
                sleep .5
                echo -e "[.]:[...]"
                sudo beef-xss
                ;;
            *)
                sleep .5
        echo -e "\n[x]:[p0st-w4sh]:[Exiting.]\n"
        sleep .5
    cat << "EOF"
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
     __          ___      _                      _  _       _       __ 
    | _|  _ __  / _ \ ___| |_          __      _| || |  ___| |__   |_ |
    | |  | '_ \| | | / __| __|  _____  \ \ /\ / / || |_/ __| '_ \   | |
    | |  | |_) | |_| \__ \ |_  |_____|  \ V  V /|__   _\__ \ | | |  | |
    | |  | .__/ \___/|___/\__|           \_/\_/    |_| |___/_| |_|  | |
    |__| |_|                                                       |__|
                             [d3k@t3ss3r4]
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
EOF

sleep .5
echo -e "\n[!]:[Hack the Planet!]\n"
                ;;
        esac
    else
        clear
        sleep .5
        echo -e "\n[x]:[p0st-w4sh]:[Exiting.]\n"
        sleep .5
    cat << "EOF"
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
     __          ___      _                      _  _       _       __ 
    | _|  _ __  / _ \ ___| |_          __      _| || |  ___| |__   |_ |
    | |  | '_ \| | | / __| __|  _____  \ \ /\ / / || |_/ __| '_ \   | |
    | |  | |_) | |_| \__ \ |_  |_____|  \ V  V /|__   _\__ \ | | |  | |
    | |  | .__/ \___/|___/\__|           \_/\_/    |_| |___/_| |_|  | |
    |__| |_|                                                       |__|
                             [d3k@t3ss3r4]
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
EOF

sleep .5
echo -e "\n[!]:[Hack the Planet!]\n"
fi


else
    clear
    echo -e "\n[!]:[stop slackin gonk]:[get back to work!]\n"
    sleep .5
    echo -e "\n[x]:[p0st-w4sh]:[Exiting.]\n"
    sleep .5
cat << "EOF"
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
     __          ___      _                      _  _       _       __ 
    | _|  _ __  / _ \ ___| |_          __      _| || |  ___| |__   |_ |
    | |  | '_ \| | | / __| __|  _____  \ \ /\ / / || |_/ __| '_ \   | |
    | |  | |_) | |_| \__ \ |_  |_____|  \ V  V /|__   _\__ \ | | |  | |
    | |  | .__/ \___/|___/\__|           \_/\_/    |_| |___/_| |_|  | |
    |__| |_|                                                       |__|
                             [d3k@t3ss3r4]
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
EOF

sleep .5
echo -e "\n[!]:[Hack the Planet!]\n"

fi                 
