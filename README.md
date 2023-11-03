# PeePee Peep

Ever in the need of a bedwetting alarm? Want to keep the data to yourself? This is the repository that will help you to keep the data to yourself. All solutions are Home Assistant oriented.

## Commercial solution

### DryLy

Why start with a commercial bedwetting alarm if this is about DIY? Because this one is used as a reference. [DryLy](https://dryly.com/) is a cloud oriented bedwetting alarm. It allows you to use the alarm in offline mode, but then it is only the alarm transmitter that communicates with the alarm receiver and you cannot receive a alarm on the device of your choosing. The alarm receiver is a Espressif device, so it could be hacked, but hardware hacking is not my cup of tea. I did some reasearch into the API and I created a small POC in the [DryLy](dryly_watcher/README.md) folder that allows you to integrate DryLy into Home Assistant for instance.

| ✅ Pros | ❌ Cons |
| ------- | ------- |
| It's ready to use.                                  | It's expensive. |
| When internet is down, the alarm receiver will work | Cloud oriented. |
| It can be integrated in Home Assistant              | It's not a sensetive alarm. |
| It can be used outside of your home.                | You will need to charge it every other night |

## DIY Bedwetting

## Aqara

You can use an [Aqara Water Leak Sensor](https://www.aqara.com/us/product/water-sensor/) and attach it to bedwetting underwear. You will still need underwear to attach the device to, the DryLy underwear can be used perfectly if you'll use something to attach the sensor to. The perfect item to do this with is the [dubble connection component](https://www.speeltechniek.nl/Spektro-Dubbel-verbindingsonderdeel) from a game called Spektro.

<img src="./images/spektro.png" height="150"/>

Take a look at the [PeePee Peep automation](peepee-peep/README.md) example. It also has detection when the sensor is being unpaired from the zigbee network.

### How To:

1. Flip the connector and cut through the metal plate or else the both buttons will be connected.
2. Unscrew the screws from the Aqara sensor, attach two wires
3. Attach/solder the wires to  the corresponding buttons of the Spektro component
4. Make sure the Aqara sensor is attached to the Spektro component, with tape for instance, and it will fit perfectly onto the DryLy underpants.
5. Make sure the Aqara sensor is added to the zigbee network with the router closes to the bed of the bedwetter

<img src="./images/ppp_aqara_front.png" height="250"/> <img src="./images/ppp_aqara_bottom.png" height="250"/> <img src="./images/ppp_aqara_attached.png" height="250"/>

| ✅ Pros | ❌ Cons |
| ------- | ------- |
| Completely local                              | The zigbee protocol is not correctly implemented in the sensor, it will always to talk to the device that added the sensor to zigbee. You will need that zigbee router close the the bedwetter. |
| You can be alarmed before the whole bed is wet   | It is very sensitive. With sweating alone it can trigger. It's best to wear underwear beneath the underwear it`s attached to. |
| It's cheaper then a commercial solution          | It's attached to the zigbee network at home, so it can only be used at home. Therefor it cannot be used for sleepovers. |
| It can last more then a year on a CR2032 battery | You will need a speaker to wake up your bed wetter |
|                                                  | You will need underpants to attach the sensor to |
|                                                  | If the alarm is being pushed for 5 seconds, it will disconnect from the zibee network. It is hard to push it and it needs to be precise, so the chance it happens by accident is small but we've got murphy... |

## Mi Temperature and Humidity Monitor 2

With the [Mi Temperature and Humidity Monitor 2](https://ams.buy.mi.com/uk/item/3204500023), I have not done a live test but I have tested it with underpeants that I made slowly wetter. I have been testing it because I was searching for a less sensitive sensor. We eventually ended up using the Aqara with extra underpants. The Mi device is less sensitive, but seems to be more sensitive then DryLy. To get this to work, you will need to flash custom firmware from https://github.com/pvvx/ATC_MiThermometer. After flashing you will need to configure the following:

* Advertising type: BT Home v1 (depending on how it's going to be read)
* RS Mode: Switch
* RS Report interval: 1

Once you have done that, you can read the switch state from bluetooth. To get a switch state, 2 wires need to be soldered to the Ground and P8, those wires need to be attached/soldered to the Spektro [dubble connection component](https://www.speeltechniek.nl/Spektro-Dubbel-verbindingsonderdeel). Also see the How To of the Aqara sensor. When done you will need to make the sensor water resistant. I think enough tape should work...

Another advantage of this device is that due to bluetooth is being used, it's possible to use an ESP32 device to read and report the switch state. That same ESP device could be the [ESP Muse](https://www.amazon.com/RASPIAUDIO-ESPMUSE-Development-Speaker-Microphone/dp/B09N3S9S29) with a speaker "integrated" or a simple, cheaper, [Rtttl buzzer](https://esphome.io/components/rtttl.html). If one of these is used, the whole package can be used during sleepovers. You will need to program the ESP device to react to the switch state and play a sound on the speaker or buzzer.


| ✅ Pros | ❌ Cons |
| ------- | ------- |
| Completely local                               | You will need a seperate speaker to wake up your bed wetter |
| You can be alarmed before the whole bed is wet | It's not water resistant |
| It is the cheapest solution                    | Soldering is needed |
| It can be used with sleepovers                 | You will need a bluetooth receiver |
| It can last a year on a CR2032 battery         | You will need underpants to attach the sensor to |