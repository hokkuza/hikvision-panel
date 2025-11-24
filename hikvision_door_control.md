# HikVision Door Control API for Node-RED Home Assistant

This document contains the API configuration for remotely opening HikVision door systems via Node-RED automation in Home Assistant.

## HikVision Door Control API Request

The API endpoint for remotely opening a door through HikVision ISAPI is:

```
POST /ISAPI/AccessControl/RemoteControl/door
```

## Required Headers
- Content-Type: application/xml
- Authorization: Digest authentication with username and password

## Request Body (XML)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<RemoteControlDoor>
    <cmd>open</cmd>
    <doorNo>1</doorNo>
</RemoteControlDoor>
```

## Node-RED Configuration

To implement this in Node-RED, configure an HTTP request node with:

- Method: POST
- URL: `http://[YOUR_HIKVISION_IP]:[PORT]/ISAPI/AccessControl/RemoteControl/door`
- Authentication: Digest
- Headers:
  - Content-Type: application/xml
- Body: raw XML as shown above

## Alternative Endpoint

Some HikVision devices may use:
```
POST /ISAPI/AccessControl/RemoteControl/door/{door_number}
```

## Parameters
- doorNo: The door number to open (typically 1, 2, 3, etc.)
- cmd: The command to execute (open, close, lock, unlock)

## Home Assistant Automation Example

Use the "Call Service" node in Node-RED to trigger the door opening when needed.

## Complete Node-RED Flow Example

```json
[
    {
        "id": "door-open-flow",
        "type": "http request",
        "z": "flow-id",
        "name": "Open HikVision Door",
        "method": "POST",
        "ret": "txt",
        "paytoqs": "ignore",
        "url": "http://[YOUR_HIKVISION_IP]:[PORT]/ISAPI/AccessControl/RemoteControl/door",
        "tls": "",
        "persist": false,
        "proxy": "",
        "authType": "digest",
        "senderr": false,
        "x": 300,
        "y": 200,
        "wires": [
            []
        ],
        "headers": [
            {
                "key": "Content-Type",
                "value": "application/xml"
            }
        ],
        "params": [],
        "xproperty": [],
        "payload": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><RemoteControlDoor><cmd>open</cmd><doorNo>1</doorNo></RemoteControlDoor>",
        "options": []
    }
]
```

## Authentication Setup

For digest authentication in Node-RED, you may need to use a function node to properly handle the authentication:

1. Install the `node-red-contrib-http-request` node if needed
2. Configure credentials for your HikVision device in the HTTP Request node
3. Make sure to use HTTPS if your device supports it for security