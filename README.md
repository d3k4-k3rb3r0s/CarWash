# CarWash 1.0.1
WARNING: This script is so bad it needs serious cleaning up and refactoring, but it does work consistently as is so I am sharing it for the purposes of collaboration at this point. I will continue fixing and developing as time goes. It does not even have an entry point yet.

What is it:
Tool to automate Wash>Reaver pixiedust workflow with cyberpunk themed output.

run > determine interface > run wash and sort by signal strength > run reaver in descending order > write successfully recovered pin & psk to csv

Requirements:
Reaver (preferrably the t6x)
Click library

Credit:
Original Credit for Wash and Reaver go to Craig Heffner.
SO far I am the only contributor for CarWash.

Why:
Research into why an obviously active and dangerous attack vector is almost always considered a moot non-issue.

I have been told that the WPS attack vector is more or less dead. While experimenting with WiFi tools I found that far far more routers are susceptible to pixiedust (including some brand new ones) then is claimed and decided to put this to a broader test. 

I wrote a quick and dirty script to automate the Wash>Reaver workflow to start.

Anyone interested in helping develop CarWash can reach out to me here or on discord. Discord = "butlerian jihadist".

Usage: As I said above this script is very under dveloped. It only takes one flag, being -i for interface. If you ignore this flag it will prompt you, and will also run the airmon-ng method of setting monitor mode. KeyboardInterrupt will skip an AP during the reaver process.

To Do List:
- fix "traffic_report.csv" write format. (currently writes all data to one column of csv.)
- fix "traffic_tickets.csv" write format (currently re-writes traffic_report.csv lines to append wps pin and wpa psk, instead of only writing successfuls to this file.)
- add option to convert traffic_tickets.csv" to a google-mappable KML file.
- add option flags to pass certain reaver and wash flags, making it more versatile.
- write a smaller version that can run headless, or with a pwnagotchi style display.
