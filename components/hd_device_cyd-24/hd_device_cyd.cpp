#include "hd_device_cyd.h"
#include "Room_rgb565.h"
#include "LovyanGFX.hpp"

namespace esphome {
namespace hd_device {

static const char *const TAG = "HD_DEVICE";
static lv_disp_draw_buf_t draw_buf;
static lv_color_t *buf = (lv_color_t *)heap_caps_malloc(TFT_HEIGHT * 20 * sizeof(lv_color_t), MALLOC_CAP_DMA);

int x = 0;
int y = 0;

SPIClass mySpi = SPIClass(VSPI);
XPT2046_Touchscreen ts(XPT2046_CS, XPT2046_IRQ);

LGFX lcd;

lv_disp_t *indev_disp;
lv_group_t *group;


void IRAM_ATTR flush_pixels(lv_disp_drv_t *disp, const lv_area_t *area, lv_color_t *color_p)
{
    uint32_t w = (area->x2 - area->x1 + 1);
    uint32_t h = (area->y2 - area->y1 + 1);
    uint32_t len = w * h;

    lcd.startWrite();                            /* Start new TFT transaction */
    lcd.setAddrWindow(area->x1, area->y1, w, h); /* set the working window */
    lcd.writePixels((uint16_t *)&color_p->full, len, true);
    lcd.endWrite();                              /* terminate TFT transaction */

    lv_disp_flush_ready(disp);
}

void IRAM_ATTR touchpad_read(lv_indev_drv_t *indev_driver, lv_indev_data_t *data)
{

    if (ts.touched()) {
        TS_Point p = ts.getPoint();
        x = map(p.x, 220, 3850, 320, 1);
        y = map(p.y, 310, 3773, 1, 240);
        data->point.x = x;
        data->point.y = y;
        data->state = LV_INDEV_STATE_PR;
        ESP_LOGCONFIG(TAG, "X: %d ", x);
        ESP_LOGCONFIG(TAG, "Y: %d ", y);
        ESP_LOGD("TOUCH", "Raw X: %d, Raw Y: %d", p.x, p.y);
    } else {
        data->state = LV_INDEV_STATE_REL;
    }
}

void HaDeckDevice::setup() {
    lv_init();
    lv_theme_default_init(NULL, lv_color_hex(0xFFEB3B), lv_color_hex(0xFF7043), 1, LV_FONT_DEFAULT);

    mySpi.begin(XPT2046_CLK, XPT2046_MISO, XPT2046_MOSI, XPT2046_CS);
    ts.begin(mySpi);
    ts.setRotation(2);

    lcd.init();
    lcd.setRotation(2);

    
    lv_disp_draw_buf_init(&draw_buf, buf, NULL, TFT_HEIGHT * 20);

    static lv_disp_drv_t disp_drv;
    lv_disp_drv_init(&disp_drv);
    disp_drv.hor_res = TFT_WIDTH;
    disp_drv.ver_res = TFT_HEIGHT;
    disp_drv.rotated = 0;
    disp_drv.sw_rotate = 0;
    disp_drv.flush_cb = flush_pixels;
    disp_drv.draw_buf = &draw_buf;
    lv_disp_t *disp = lv_disp_drv_register(&disp_drv);

    static lv_indev_drv_t indev_drv;
    lv_indev_drv_init(&indev_drv);
    indev_drv.type = LV_INDEV_TYPE_POINTER;
    indev_drv.long_press_time = 1000;
    indev_drv.long_press_repeat_time = 300;
    indev_drv.read_cb = touchpad_read;
    lv_indev_drv_register(&indev_drv);

    group = lv_group_create();
    lv_group_set_default(group);

    lcd.setBrightness(brightness_);

    // Do NOT create the background image here (in setup), because it will always be visible.
    // Instead, create and show/hide the background image dynamically when the screen changes.
}

// Add this function to handle screen changes
void HaDeckDevice::on_screen_change(const std::string &screen_name) {
    static lv_obj_t *bg_image = nullptr;

    // Remove previous bg image if it exists
    if (bg_image) {
        lv_obj_del(bg_image);
        bg_image = nullptr;
    }

    if (screen_name == "temperature") { // or use your SCREEN_TEMP substitution value
        bg_image = lv_img_create(lv_scr_act());
        lv_img_set_src(bg_image, &bg_room);
        lv_obj_align(bg_image, LV_ALIGN_CENTER, 0, 0);
        lv_obj_move_background(bg_image); // Ensure it's at the back
    }
    // else: no bg image, default background
}

// NOTE: The function on_screen_change will only be called if you explicitly call it
// from your screen change logic. ha_deck does NOT call this automatically.
// You must connect this function to the screen change event in your code.

// Example: If you have access to the screen change event in your ha_deck integration,
// call this function like:
//   id(device).on_screen_change(screen_name);

// If you are using only YAML and ha_deck, there is currently NO way to trigger this C++ function
// automatically on screen change. You would need to patch ha_deck or add a custom lambda
// in the ha_deck component to call this function when the screen changes.

void HaDeckDevice::loop() {
    lv_timer_handler();

    unsigned long ms = millis();
    if (ms - time_ > 60000) {
        time_ = ms;
        ESP_LOGCONFIG(TAG, "Free memory: %d bytes", esp_get_free_heap_size());
    }
}

float HaDeckDevice::get_setup_priority() const { return setup_priority::DATA; }

uint8_t HaDeckDevice::get_brightness() {
    return brightness_;
}

void HaDeckDevice::set_brightness(uint8_t value) {
    brightness_ = value;
    lcd.setBrightness(brightness_);
}


}  // namespace hd_device
}  // namespace esphome
