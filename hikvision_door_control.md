# HikVision Door Control API for Node-RED Home Assistant

This document contains the correct API configuration for remotely opening HikVision door systems via Node-RED automation in Home Assistant.

## Official HikVision ISAPI Documentation Reference

According to HikVision's official ISAPI (Integrated Security API) documentation, the correct endpoint for door control is:

```
POST /ISAPI/AccessControl/door/{door_number}/open
```

Alternative endpoints that may be supported by different models:
- `POST /ISAPI/AccessControl/door/open`
- `POST /ISAPI/AccessControl/RemoteControl/door`

## Required Headers
- Content-Type: application/xml
- Authorization: Digest authentication with username and password

## Request Body (XML)
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

## Node-RED Configuration

To implement this in Node-RED, configure an HTTP request node with:

- Method: POST
- URL: `http://[YOUR_HIKVISION_IP]:[PORT]/ISAPI/AccessControl/door/{door_number}/open`
- Authentication: Digest
- Headers:
  - Content-Type: application/xml
- Body: raw XML as shown above

## Parameters
- door_number: The door number to open (typically 1, 2, 3, etc.)
- delayTime: Time in seconds for how long the door should remain open (optional, device-dependent)

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
        "url": "http://[YOUR_HIKVISION_IP]:[PORT]/ISAPI/AccessControl/door/1/open",
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
        "payload": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><AccessControlDoorOpen xmlns=\"urn:psialliance:params:xml:ns:ptz-1\"><doorID>1</doorID><delayTime>5</delayTime></AccessControlDoorOpen>",
        "options": []
    }
]
```

## Authentication Setup

For digest authentication in Node-RED:

1. Install the `node-red-contrib-http-request` node if needed
2. Configure credentials for your HikVision device in the HTTP Request node
3. Make sure to use HTTPS if your device supports it for security

## Testing the API

You can test the API using curl:

```bash
curl -X POST \
  -u username:password \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?><AccessControlDoorOpen xmlns="urn:psialliance:params:xml:ns:ptz-1"><doorID>1</doorID><delayTime>5</delayTime></AccessControlDoorOpen>' \
  http://[YOUR_HIKVISION_IP]:[PORT]/ISAPI/AccessControl/door/1/open
```

## Important Notes

1. The exact endpoint may vary depending on your HikVision device model
2. Some devices may require different XML namespaces or structures
3. Make sure to use proper credentials with sufficient permissions
4. Check your device's ISAPI documentation for specific capabilities
5. Test the API with your specific device model before implementing in production