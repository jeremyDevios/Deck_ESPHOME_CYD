# Home Assistant Deck CYD Component

This project is inspired by the CYD Screen (2 USB Version) support component for [HA_Deck](https://github.com/strange-v/ha_deck) by [strange_v](https://github.com/strange-v). It has been updated to be installed on ESP32-2432S024R or ESP32-2432S028.

To launch the application on `ESP32-2432S024R`, use the command:

```bash
esphome run examples/ha_deck_cyd.yaml
```

For `ESP32-2432S028`, use the command:

```bash
esphome run examples/ha_deck_cyd-28.yaml
```

The code has been completely rewritten to display a view and provide control of connected objects on my Home Assistant server (e.g., light control, temperature display, etc.).

### Description

This project provides a touchscreen interface for your Home Assistant installation using an ESP32-based CYD display.  
Currently, the interface is organized into 5 different pages:

- **Power Monitoring:** Displays the real-time power consumption (Watts) of all monitored equipment available in Home Assistant.
- **Lights Control:** Allows activation/deactivation of lights in the children's rooms.
- **Heating Control:** Allows activation/deactivation of heating in the children's rooms and in the washroom.
- **Garden Control:** Allows activation/deactivation of the garden watering system and the swimming pool pump.
- **Temperature Monitoring:** Displays the temperature values for each room in the house.

All these data points are sourced from Home Assistant and can be monitored and controlled directly from the ESP32 Home Deck.

### Hardware reference:
[ESP32-2432S028 aka CYD (Cheap Yellow Display) or ESP32-2432S024R ](https://ali.ski/vNTYds)

---

## Result of Development

Below are some screenshots and animations of the current interface:

**Home Screen:**  
![](/images/HomeScreen.jpeg)

**Animation Result:**  
![](/images/animated-deck.gif)

**Temperature Screen:**  
![](/images/House-temperature.jpg)

---

## Legal Notice

This project is provided as-is, without any warranty or guarantee of fitness for a particular purpose.  
All trademarks, product names, and company names or logos cited herein are the property of their respective owners.  
This project is not affiliated with or endorsed by Home Assistant, Espressif, or any hardware manufacturer.  
Use at your own risk.
