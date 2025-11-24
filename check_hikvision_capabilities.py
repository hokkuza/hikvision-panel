#!/usr/bin/env python3
"""
Utility script to check HikVision device capabilities and supported endpoints
This script helps identify which door control endpoints are supported by your device
"""

import requests
from requests.auth import HTTPDigestAuth
import sys
import xml.etree.ElementTree as ET

def check_device_info(ip, port, username, password, protocol='http'):
    """
    Get basic device information
    """
    url = f"{protocol}://{ip}:{port}/ISAPI/System/deviceInfo"
    
    try:
        response = requests.get(
            url,
            auth=HTTPDigestAuth(username, password),
            timeout=10
        )
        
        if response.status_code == 200:
            print("✓ Device info retrieved successfully")
            try:
                root = ET.fromstring(response.text)
                device_name = root.find('.//deviceName')
                device_model = root.find('.//model')
                firmware_version = root.find('.//firmwareVersion')
                
                print(f"  Device Name: {device_name.text if device_name is not None else 'Unknown'}")
                print(f"  Model: {device_model.text if device_model is not None else 'Unknown'}")
                print(f"  Firmware: {firmware_version.text if firmware_version is not None else 'Unknown'}")
            except ET.ParseError:
                print(f"  Raw response: {response.text[:200]}...")
        else:
            print(f"✗ Failed to get device info. Status: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error getting device info: {e}")

def check_access_control_capabilities(ip, port, username, password, protocol='http'):
    """
    Check access control capabilities
    """
    endpoints_to_check = [
        "/ISAPI/AccessControl/capabilities",
        "/ISAPI/AccessControl/door/capabilities", 
        "/ISAPI/AccessControl/remoteControl/capabilities"
    ]
    
    for endpoint in endpoints_to_check:
        url = f"{protocol}://{ip}:{port}{endpoint}"
        
        try:
            response = requests.get(
                url,
                auth=HTTPDigestAuth(username, password),
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                print(f"✓ {endpoint} - Available (Status: {response.status_code})")
                
                # Try to parse and display some capabilities if available
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.text)
                        # Look for door count or similar capabilities
                        door_count = root.find('.//doorNum')
                        if door_count is not None:
                            print(f"  - Number of doors: {door_count.text}")
                    except ET.ParseError:
                        pass
            else:
                print(f"✗ {endpoint} - Not available (Status: {response.status_code})")
                
        except Exception as e:
            print(f"✗ {endpoint} - Error: {e}")

def check_door_status(ip, port, username, password, door_number=1, protocol='http'):
    """
    Check door status
    """
    endpoints_to_check = [
        f"/ISAPI/AccessControl/door/{door_number}/status",
        "/ISAPI/AccessControl/door/status",
        f"/ISAPI/AccessControl/remoteControl/doorStatus/{door_number}"
    ]
    
    for endpoint in endpoints_to_check:
        url = f"{protocol}://{ip}:{port}{endpoint}"
        
        try:
            response = requests.get(
                url,
                auth=HTTPDigestAuth(username, password),
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                print(f"✓ {endpoint} - Available (Status: {response.status_code})")
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.text)
                        # Print some status info if available
                        status_elem = root.find('.//status')
                        if status_elem is not None:
                            print(f"  - Current status: {status_elem.text}")
                    except ET.ParseError:
                        pass
            else:
                print(f"✗ {endpoint} - Not available (Status: {response.status_code})")
                
        except Exception as e:
            print(f"✗ {endpoint} - Error: {e}")

def main():
    if len(sys.argv) != 5:
        print("Usage: python check_hikvision_capabilities.py <ip> <port> <username> <password>")
        print("Example: python check_hikvision_capabilities.py 192.168.1.100 80 admin mypassword")
        return
    
    ip = sys.argv[1]
    port = int(sys.argv[2])
    username = sys.argv[3]
    password = sys.argv[4]
    
    print(f"HikVision Device Capability Check")
    print(f"Target: {ip}:{port}")
    print("-" * 40)
    
    # Check basic device info
    check_device_info(ip, port, username, password)
    print()
    
    # Check access control capabilities
    print("Checking Access Control Capabilities:")
    check_access_control_capabilities(ip, port, username, password)
    print()
    
    # Check door status endpoints
    print("Checking Door Status Endpoints:")
    check_door_status(ip, port, username, password)
    print()
    
    print("Check complete. Use this information to determine the correct endpoint for door control.")

if __name__ == "__main__":
    main()