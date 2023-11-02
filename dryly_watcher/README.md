# DryLy API

This is a simple POC repository to communicate with the DryLy api. It runs between 20 and 8, which is hardcoded.

Copy this to Home Assistant in the python_scripts folder. Add the following to the `configuration.yaml`:

```YAML
command_line:
  - sensor:
    name: Dryly Command Line
    scan_interval: 10
    command_timeout: 86400
    command: python3 /config/python_scripts/dryly_watcher.py
```

Create an input boolean in Home Assistant. This will be set to `True` by the script.

Edit the `dryly_watcher.json`

```JSON
{
    "configuration": {
        "wait": 5
    },
    "authentication": {
        "email": "", # Your DryLy email
        "password": "", # Your DryLy password
        "access_token": "" # This will be configured by the script
    },
    "log": {
        "level": "info"
    },
    "notification": {
        "last": 1764495
    },
    "home_assistant": {
        "url": "", # Home Assistant URL
        "port": 8123, # Port where Home Assistant runs
        "access_token": "", # A JSON Access token from Home Assistant
        "input_boolean": "peepee_peep" # The name of the boolean. The script will prepent input_boolean. so do not configure that here
    }
}
```