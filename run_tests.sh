#!/bin/bash

echo "HikVision Door Control Test Suite"
echo "================================="

if [ $# -ne 4 ]; then
    echo "Usage: $0 <ip> <port> <username> <password>"
    echo "Example: $0 192.168.1.100 80 admin mypassword"
    exit 1
fi

IP=$1
PORT=$2
USERNAME=$3
PASSWORD=$4

echo "Target: http://$IP:$PORT"
echo "Username: $USERNAME"
echo ""

# Check if required Python modules are available
echo "Checking Python modules..."
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: 'requests' module not found. Please install it with: pip3 install requests"
    exit 1
fi

echo "✓ requests module is available"
echo ""

# Check device capabilities first
echo "1. Checking device capabilities..."
python3 check_hikvision_capabilities.py $IP $PORT $USERNAME $PASSWORD
echo ""

# Ask for door number
read -p "Enter door number to test (default: 1): " DOOR_NUMBER
DOOR_NUMBER=${DOOR_NUMBER:-1}

echo ""
echo "2. Testing door $DOOR_NUMBER control..."
python3 test_hikvision_door.py $IP $PORT $USERNAME $PASSWORD $DOOR_NUMBER
echo ""

echo "Test suite completed."