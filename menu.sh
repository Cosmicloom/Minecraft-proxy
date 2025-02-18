#!/bin/bash
clear
echo "Minecraft Server Proxy Menu"
echo "==========================="
echo "1. Start Proxy Server"
echo "2. Stop Proxy Server"
echo "3. Edit Server IP"
echo "4. Exit"
read -p "Choose an option: " choice

case $choice in
    1) python3 proxy.py ;;
    2) pkill -f proxy.py ;;
    3) nano config.txt ;;
    4) exit ;;
    *) echo "Invalid option!" ;;
esac

./menu.sh