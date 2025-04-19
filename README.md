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

### Hardware reference:
[ESP32-2432S028 aka CYD (Cheap Yellow Display) or ESP32-2432S024R ](https://ali.ski/vNTYds)

![](/images/ha-deck-cyd.jpg)
