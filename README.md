# HikVision Door Control for Node-RED Home Assistant

This repository provides all necessary files and documentation to remotely open HikVision doors through Node-RED automation in Home Assistant.

## Overview

The solution includes:
- API documentation for HikVision door control
- Node-RED flow configuration
- Python test script
- Implementation instructions

## HikVision Door Control API

According to HikVision's official ISAPI (Integrated Security API) documentation, the correct endpoint for door control is:

### Primary Endpoint
```
POST /ISAPI/AccessControl/door/{door_number}/open
```

Alternative endpoints that may be supported by different models:
- `POST /ISAPI/AccessControl/door/open`
- `POST /ISAPI/AccessControl/RemoteControl/door`

### Headers
- Content-Type: application/xml
- Authorization: Digest authentication

### Request Body (XML)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<AccessControlDoorOpen xmlns="urn:psialliance:params:xml:ns:ptz-1">
    <doorID>{door_number}</doorID>
    <delayTime>{delay_in_seconds}</delayTime>
</AccessControlDoorOpen>
```

Or for some models:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<RemoteControlDoor>
    <cmd>open</cmd>
    <doorNo>{door_number}</doorNo>
    <delayTime>{delay_in_seconds}</delayTime>
</RemoteControlDoor>
```

## Files Included

1. `hikvision_door_control.md` - Complete documentation with correct API endpoints
2. `hikvision_door_control_flow.json` - Importable Node-RED flow
3. `test_hikvision_door.py` - Python test script with multiple endpoint/protocol fallbacks
4. `check_hikvision_capabilities.py` - Utility script to check device capabilities and supported endpoints
5. `hikvision_collection.json` - Original Postman collection for reference

## Node-RED Implementation

### Method 1: Import Flow
1. Open Node-RED editor
2. Go to Menu > Import > Clipboard
3. Paste the content from `hikvision_door_control_flow.json`
4. Deploy the flow
5. Configure credentials in the HTTP Request node

### Method 2: Manual Configuration
1. Add an HTTP Request node
2. Set method to POST
3. Set URL to `http://[YOUR_HIKVISION_IP]:[PORT]/ISAPI/AccessControl/door/{door_number}/open`
4. Set authentication to Digest
5. Set headers: Content-Type: application/xml
6. Set payload to the XML above
7. Connect to appropriate trigger nodes

## Testing

First, use the capability checker script to identify which endpoints your device supports:

```bash
python3 check_hikvision_capabilities.py <ip> <port> <username> <password>
```

Example:
```bash
python3 check_hikvision_capabilities.py 192.168.1.100 80 admin mypassword
```

Or use the automated test script:

```bash
./run_tests.sh <ip> <port> <username> <password>
```

Example:
```bash
./run_tests.sh 192.168.1.100 80 admin mypassword
```

Then, to test the door opening API directly, use the test script:

```bash
python3 test_hikvision_door.py <ip> <port> <username> <password> <door_number>
```

Example:
```bash
python3 test_hikvision_door.py 192.168.1.100 80 admin mypassword 1
```

## Integration with Home Assistant

Connect the HTTP request node to Home Assistant service call nodes to trigger door opening from Home Assistant automations, dashboards, or voice commands.

## Security Notes

- Use strong credentials for your HikVision device
- Consider using HTTPS if supported by your device
- Restrict network access to the HikVision device
- Use dedicated user accounts with minimal required permissions

## Troubleshooting

1. Ensure your HikVision device supports the ISAPI Access Control API
2. Verify credentials are correct
3. Check that the door number is valid for your device
4. Confirm network connectivity to the device
5. Check device logs for any error messages
6. Try different endpoints if the primary one doesn't work
7. Consult your device's specific ISAPI documentation for model-specific requirements