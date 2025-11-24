# HikVision Door Control for Node-RED Home Assistant

This repository provides all necessary files and documentation to remotely open HikVision doors through Node-RED automation in Home Assistant.

## Overview

The solution includes:
- API documentation for HikVision door control
- Node-RED flow configuration
- Python test script
- Implementation instructions

## HikVision Door Control API

### Endpoint
```
POST /ISAPI/AccessControl/RemoteControl/door
```

### Headers
- Content-Type: application/xml
- Authorization: Digest authentication

### Request Body (XML)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<RemoteControlDoor>
    <cmd>open</cmd>
    <doorNo>1</doorNo>
</RemoteControlDoor>
```

## Files Included

1. `hikvision_door_control.md` - Complete documentation
2. `hikvision_door_control_flow.json` - Importable Node-RED flow
3. `test_hikvision_door.py` - Python test script

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
3. Set URL to `http://[YOUR_HIKVISION_IP]:[PORT]/ISAPI/AccessControl/RemoteControl/door`
4. Set authentication to Digest
5. Set headers: Content-Type: application/xml
6. Set payload to the XML above
7. Connect to appropriate trigger nodes

## Testing

To test the API directly, use the Python script:

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