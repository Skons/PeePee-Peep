# PeePee Peep

Automation example. In this example there is an event for the unpair of the Aqara sensor. I had not renamed the device, i dont now if the device id is used on the `zigbee2mqtt/bridge/event` topic, or the friendly name.

```yaml
- id: "peepeepeep"
  alias: PeePee Peep
  trigger:
  - platform: mqtt
    topic: "zigbee2mqtt/bridge/event"
    payload: "0x0012345678900000"
    value_template: "{{ value_json.data.ieee_address }}"
    id: unpair
  - platform: state
    entity_id: binary_sensor.0x0012345678900000_water_leak
    to: 'on'
    id: peepeepeep
  - platform: state
    entity_id: binary_sensor.0x0012345678900000_water_leak
    from: 'on'
    to: 'off'
    id: detach
  action:
  - choose:
    - conditions:
      - condition: trigger
        id: unpair
      - condition: template
        value_template: '{{ trigger.payload_json.type == "device_leave" }}'
      sequence:
        service: notify.mobile_app
        data:
            message: "Aqara sensor just got unpaired"
            title: Unpaired
    - conditions:
      - condition: trigger
        id: peepeepeep
      sequence:
        - service: media_player.play_media
          continue_on_error: true
          data:
            media_content_id: http://homeassistant.local:8123/local/peepee-peep.mp3
            media_content_type: audio
          target:
            device_id: [mediaplayer_device_id]
        - service: notify.mobile_app
          continue_on_error: true
          data:
            title: "PeePee Peep on"
            message: "The bed just became wet 🚽"
            data:
              push:
                sound:
                  name: "default"
                  critical: 1
                  volume: 0.5
    - conditions:
      - condition: trigger
        id: detach
      sequence:
        - service: media_player.media_stop
          continue_on_error: true
          target:
            device_id: [mediaplayer_device_id]
        - service: notify.mobile_app
          continue_on_error: true
          data:
            title: PeePee Peep off
            message: PeePee Peep has just been detached from the underpants
```