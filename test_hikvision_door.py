#!/usr/bin/env python3
"""
Test script for HikVision door control API
This script demonstrates how to remotely open a HikVision door via ISAPI
"""

import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET
import sys

def open_door(ip, port, username, password, door_number=1, protocol='http'):
    """
    Open a HikVision door via ISAPI
    
    Args:
        ip (str): IP address of the HikVision device
        port (int): Port number of the HikVision device
        username (str): Username for authentication
        password (str): Password for authentication
        door_number (int): Door number to open (default: 1)
        protocol (str): Protocol to use (default: http)
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    # API endpoint - primary method
    url = f"{protocol}://{ip}:{port}/ISAPI/AccessControl/door/{door_number}/open"
    
    # Alternative endpoints that might work with different models
    alternative_urls = [
        f"{protocol}://{ip}:{port}/ISAPI/AccessControl/door/open",
        f"{protocol}://{ip}:{port}/ISAPI/AccessControl/RemoteControl/door"
    ]
    
    # XML payload for primary method
    xml_payload = f'''<?xml version="1.0" encoding="UTF-8"?>
<AccessControlDoorOpen xmlns="urn:psialliance:params:xml:ns:ptz-1">
    <doorID>{door_number}</doorID>
    <delayTime>5</delayTime>
</AccessControlDoorOpen>'''
    
    # Alternative XML payload for some models
    alt_xml_payload = f'''<?xml version="1.0" encoding="UTF-8"?>
<RemoteControlDoor>
    <cmd>open</cmd>
    <doorNo>{door_number}</doorNo>
    <delayTime>5</delayTime>
</RemoteControlDoor>'''
    
    # Headers
    headers = {
        'Content-Type': 'application/xml'
    }
    
    try:
        # First, try the primary endpoint with primary XML
        response = requests.post(
            url,
            data=xml_payload,
            headers=headers,
            auth=HTTPDigestAuth(username, password),
            timeout=10
        )
        
        # Check response
        if response.status_code == 200:
            print(f"Door {door_number} opened successfully using primary endpoint!")
            return True
        else:
            print(f"Primary endpoint failed with status code: {response.status_code}")
            print("Trying alternative endpoints...")
            
            # Try alternative endpoints with primary XML
            for alt_url in alternative_urls:
                try:
                    print(f"Trying alternative endpoint: {alt_url}")
                    response = requests.post(
                        alt_url,
                        data=xml_payload,
                        headers=headers,
                        auth=HTTPDigestAuth(username, password),
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        print(f"Door {door_number} opened successfully using alternative endpoint: {alt_url}")
                        return True
                    else:
                        print(f"Alternative endpoint {alt_url} failed with status code: {response.status_code}")
                        
                except requests.exceptions.RequestException as e:
                    print(f"Error trying alternative endpoint {alt_url}: {e}")
            
            # If all primary XML attempts failed, try alternative XML with primary endpoint
            print("Trying alternative XML format with primary endpoint...")
            try:
                response = requests.post(
                    url,
                    data=alt_xml_payload,
                    headers=headers,
                    auth=HTTPDigestAuth(username, password),
                    timeout=10
                )
                
                if response.status_code == 200:
                    print(f"Door {door_number} opened successfully using alternative XML format!")
                    return True
                else:
                    print(f"Alternative XML format with primary endpoint failed with status code: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Error trying alternative XML format: {e}")
            
            # Finally, try alternative endpoints with alternative XML
            print("Trying alternative endpoints with alternative XML format...")
            for alt_url in alternative_urls:
                try:
                    print(f"Trying alternative endpoint with alternative XML: {alt_url}")
                    response = requests.post(
                        alt_url,
                        data=alt_xml_payload,
                        headers=headers,
                        auth=HTTPDigestAuth(username, password),
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        print(f"Door {door_number} opened successfully using {alt_url} with alternative XML!")
                        return True
                    else:
                        print(f"Alternative endpoint {alt_url} with alternative XML failed with status code: {response.status_code}")
                        
                except requests.exceptions.RequestException as e:
                    print(f"Error trying alternative endpoint with alternative XML {alt_url}: {e}")
            
            print(f"All attempts to open door {door_number} failed.")
            print(f"Last response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return False

def main():
    """
    Main function to demonstrate usage
    """
    if len(sys.argv) != 6:
        print("Usage: python test_hikvision_door.py <ip> <port> <username> <password> <door_number>")
        print("Example: python test_hikvision_door.py 192.168.1.100 80 admin mypassword 1")
        return
    
    ip = sys.argv[1]
    port = int(sys.argv[2])
    username = sys.argv[3]
    password = sys.argv[4]
    door_number = int(sys.argv[5])
    
    success = open_door(ip, port, username, password, door_number)
    
    if success:
        print("Door opened successfully!")
    else:
        print("Failed to open door!")

if __name__ == "__main__":
    main()