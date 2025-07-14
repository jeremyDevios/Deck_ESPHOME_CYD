#pragma once

#include <stdint.h>

typedef struct {
    int width;
    int height;
    const uint8_t *data;
} Image;

extern const Image Room;