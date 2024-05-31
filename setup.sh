#!/bin/bash

hostname=$(hostname)
operator=$(whoami)

# Function to prompt user to continue
prompt_continue() {
    read -e -p"[>]:[$hostname]:[CarWash]:[set^]:[>]:[press]:[ENTER]:[>]\n"
}

# Exit immediately if a command exits with a non-zero status
set -e


# Function to install aircrack-ng
install_aircrack() {
    cat << "EOF"






                                      ((( /\ )))
                                          ||
    [r0ll1n 1n my (arm) six-f0']          ||
                         _________________||__
                        [|||||||||||||||||||||]
                    ___/~~~~~~~~~~~~~~~~~~~~~~~\___
                   /                               \             
                 _/       [CarWash]::[1.0.4]        \_           
             {_}/_____                           _____\{_}       
            .-''      ~~~~~~~~~~~~~~~~~~~~~~~~~~~     ``-.       
          .-~            ____________________            ~-.
         '~~/~~~~~~~~~~~~TTTTTTTTTTTTTTTTTTTT~~~~~~~~~~~~\~~'
         | | | #### #### || | | | [] | | | || #### #### | | |
         ;__\|___________|++++++++++++++++++|___________|/__;
          (~~====___________________________________====~~~)
           \------____________[_Hosaka_]___________-------/
              |      ||                        ||      |
               \_____/  [d3k@t3ss3r4]:[2024]   \_____/
EOF
    sleep .2
    echo -e "\n[!]:[sysangel@$hostname]:[I need to install [aircrack-n] for CarWash?]:[!]\n"
    sleep .2
    prompt_continue
    sleep .2
    echo -e "[+]:[$hostname]:[CarWash]:[set^]:[apt.update]:[init]:[+]\n"
    if sudo apt update &> /dev/null; then
        sleep .2
        echo -e "[=]:[$hostname]:[CarWash]:[set^]:[apt.update]:[complete]:[=]"
        sleep .2
        echo -e "[↓]:[$hostname]:[CarWash]:[set^]:[aircrack-ng]:[=]:[installing]:[↓]"
        if sudo apt install -y aircrack-ng &> /dev/null; then
            sleep .2
            echo -e "[=]:[$hostname]:[CarWash]:[set^]:[aircrack-ng]:[=]:[installed]:[=]\n"
        else
            sleep .2
            echo -e "[!!!!]:[$hostname]:[CarWash]:[set^]:[aircrack-ng]:[=]:[install.fail]:[!!!!]\n"
            sleep .2
            echo -e "[!!!!]:[$hostname]:[CarWash]:[set^]:[aircrack-ng]:[=]:[review.error]:[!!!!]\n"
        fi
    else
        sleep .2
        echo -e "[!!!!]:[$hostname]:[CarWash]:[set^]:[apt.update]:[=]:[apt.error]:[!!!!]\n"
        sleep .2
        echo -e "[!!!!]:[$hostname]:[CarWash]:[set^]:[apt.update]:[=]:[review.error]:[!!!!]\n"
        
    fi
}

# Function to install reaver
install_reaver() {
    cat << "EOF"






                                      ((( /\ )))
                                          ||
    [r0ll1n 1n my (arm) six-f0']          ||
                         _________________||__
                        [|||||||||||||||||||||]
                    ___/~~~~~~~~~~~~~~~~~~~~~~~\___
                   /                               \             
                 _/       [CarWash]::[1.0.4]        \_           
             {_}/_____                           _____\{_}       
            .-''      ~~~~~~~~~~~~~~~~~~~~~~~~~~~     ``-.       
          .-~            ____________________            ~-.
         '~~/~~~~~~~~~~~~TTTTTTTTTTTTTTTTTTTT~~~~~~~~~~~~\~~'
         | | | #### #### || | | | [] | | | || #### #### | | |
         ;__\|___________|++++++++++++++++++|___________|/__;
          (~~====___________________________________====~~~)
           \------____________[_Hosaka_]___________-------/
              |      ||                        ||      |
               \_____/  [d3k@t3ss3r4]:[2024]   \_____/
EOF
    sleep .2
    echo -e "\n[!]:[sysangel@$hostname]:[I need to install [t6x_reaver_wash] for CarWash?]:[!]\n"
    sleep .2
    prompt_continue
    sleep .2
    echo -e "[↓]:[$hostname]:[CarWash]:[set^]:[↓git.clone↓]:[t6x_reaver]:[t6x_wash]:[↓]\n"
    if git clone https://github.com/t6x/reaver-wps-fork-t6x.git &> /dev/null; then
        sleep .2
        echo -e "[=]:[$hostname]:[CarWash]:[set^]:[git.CLONED]:[t6x_reaver]:[t6x_wash]:[=]\n"
        sleep .2
        echo -e "[<]:[$hostname]:[CarWash]:[set^]:[config]:[t6x_reaver]:[t6x_wash]:[>]\n"
        sleep .2
        (cd reaver-wps-fork-t6x*/src)
        if sudo ./configure &> /dev/null; then
            sleep .2
            echo -e "[=]:[$hostname]:[CarWash]:[set^]:[CONFIGURED]:[t6x_reaver]:[t6x_wash]:[=]\n"
            sleep .2
            echo -e "[=]:[$hostname]:[CarWash]:[set^]:[make]:[t6x_reaver]:[t6x_wash]:[=]\n"
            if make &> /dev/null; then
                sleep .2
                echo -e "[=]:[$hostname]:[CarWash]:[set^]:[MADE]:[t6x_reaver]:[t6x_wash]:[=]\n"
                sleep .2
                echo -e "[!]:[CarWash]:[set^]:[t6x_reaver]:[t6x_wash]:[=]:[install.successful]:[!]\n"
            else
                sleep .2
                echo -e "[!!!!]:[$hostname]:[CarWash]:[set^]:[t6x_reaver]:[t6x_wash]:[=]:[install.fail]:[!!!!]\n"
                sleep .2
                echo -e "[!!!!]:[$hostname]:[CarWash]:[set^]:[t6x_reaver]:[t6x_wash]:[=]:[review.error]:[!!!!]\n"
            fi
        else
            sleep .2
            echo -e "[!!!!]:[$hostname]:[CarWash]:[set^]:[t6x_reaver]:[t6x_wash]:[=]:[config.fail]:[!!!!]\n"
            sleep .2
            echo -e "[!!!!]:[$hostname]:[CarWash]:[set^]:[t6x_reaver]:[t6x_wash]:[=]:[review.error]:[!!!!]\n"
        fi
    else
        sleep .2
        echo -e "[!!!!]:[$hostname]:[CarWash]:[set^]:[git.clone]:[=]:[clone.fail]:[!!!!]\n"
        sleep .2
        echo -e "[!!!!]:[$hostname]:[CarWash]:[set^]:[git.clone]:[=]:[review.error]:[!!!!]\n"
    fi
}

# Function to run setup.py
run_setup_py() {
    if [[ -f setup.py ]]; then
        echo -e "\n[!]:[$hostname:]:[CarWash]:[set^]:[running]:[setup.py]:[!]\n"
        pip install .
        echo -e "\n[!]:[$hostname:]:[CarWash]:[set^]:[setup.py]:[complete]:[!]\n"
    else
        echo -e "\n[!]:[$hostname:]:[CarWash]:[set^]:[setup.py]:[not found]:[!]\n"
    fi
}

# Function to handle script exit
exit_script() {
  echo -e "\n[x]:[$hostname]:[CarWash]:[set^]:[operation.complete/interrupted]:[x]"
            sleep .2
            echo "[.]:[...]"
            sleep .2
            echo "[!]:[d3k4t3ss3r4]:[thanks for using CarWash, $operator]:[!]"
            sleep .2
            echo "[.]:[...]"
            sleep .3
            echo -e "\n[x]:[exiting...]:[hack_the_planet]:[x]"
  exit 0
}

# Install dependencies
clear
cat << "EOF"






                                      ((( /\ )))
                                          ||
    [r0ll1n 1n my (arm) six-f0']          ||
                         _________________||__
                        [|||||||||||||||||||||]
                    ___/~~~~~~~~~~~~~~~~~~~~~~~\___
                   /                               \             
                 _/       [CarWash]::[1.0.4]        \_           
             {_}/_____                           _____\{_}       
            .-''      ~~~~~~~~~~~~~~~~~~~~~~~~~~~     ``-.       
          .-~            ____________________            ~-.
         '~~/~~~~~~~~~~~~TTTTTTTTTTTTTTTTTTTT~~~~~~~~~~~~\~~'
         | | | #### #### || | | | [] | | | || #### #### | | |
         ;__\|___________|++++++++++++++++++|___________|/__;
          (~~====___________________________________====~~~)
           \------____________[_Hosaka_]___________-------/
              |      ||                        ||      |
               \_____/  [d3k@t3ss3r4]:[2024]   \_____/
EOF
sleep .2
echo -e "\n[!]:[sysangel@$hostname]:[Welcome to the set^ process for CarWash,$operator.]:[!]\n"
sleep .2
prompt_continue
sleep .3
install_aircrack
install_reaver
run_setup_py
exit_script

