#include "include/nvs_init.h"
#include "include/platform.h"
#include "include/ota_update.h"
#include "include/factory_reset.h"
#include "driver_framebuffer.h"

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_err.h"
#include "esp_partition.h"
#include "esp_spi_flash.h"
#include "nvs_flash.h"
#include "nvs.h"

extern void micropython_entry(void);

extern esp_err_t unpack_first_boot_zip(void);

void nvs_write_zip_status(bool status) {
    nvs_handle my_handle;
    esp_err_t res = nvs_open("system", NVS_READWRITE, &my_handle);
    if (res != ESP_OK) {
        printf("NVS seems unusable! Please erase flash and try flashing again. (1)\n");
        halt();
    }
    res = nvs_set_u8(my_handle, "preseed", status);
    if (res != ESP_OK) {
        printf("NVS seems unusable! Please erase flash and try flashing again. (2)\n");
        halt();
    }
}

void set_1e_access_permission_bits() {
    printf("INFO: setting 1e permission bits.\n");

    const esp_partition_t *custom1 = esp_partition_find_first(0x40, 0x0, "custom1");
    if (custom1 == NULL) {
        printf("ERROR: custom1 partition is missing!\n");
        return;
    }

    if (esp_partition_erase_range(custom1, 0x0, 0x1000) != ESP_OK) {
        printf("WARNING: custom1 erase failed. Still continuing with the write.\n");
    }

    uint8_t data[4] = {0};
    if (esp_partition_write(custom1, 0x0FFC, data, 4) != ESP_OK) {
        printf("ERROR: custom1 write failed. Permission bits for challenge 1e potentially not set!\n");
    }

    if (esp_partition_read(custom1, 0x0FFC, data, 4) != ESP_OK) {
        printf("WARNING: custom1 read failed. Couldn't check for permission bits.\n");
        return;
    }

    if(*((uint32_t*)data) != 0) {
        printf("ERROR: custom1 4 bytes at 0x0FFC != 0.\n");
    }
}

void app_main() {
    logo();
    bool is_first_boot = nvs_init();
    platform_init();

    if (is_first_boot) {
#ifdef CONFIG_DRIVER_FRAMEBUFFER_ENABLE
        driver_framebuffer_fill(NULL, COLOR_BLACK);
        driver_framebuffer_print(NULL, "Extracting ZIP...\n", 0, 0, 1, 1, COLOR_WHITE, &roboto_12pt7b);
        driver_framebuffer_flush(0);
#endif
        printf("Attempting to unpack FAT initialization ZIP file...\b");
        if (unpack_first_boot_zip() != ESP_OK) {  // Error
#ifdef CONFIG_DRIVER_FRAMEBUFFER_ENABLE
            driver_framebuffer_fill(NULL, COLOR_BLACK);
            driver_framebuffer_print(NULL, "ZIP error!\n", 0, 0, 1, 1, COLOR_WHITE, &roboto_12pt7b);
            driver_framebuffer_flush(0);
#endif
            printf("An error occured while unpacking the ZIP file!");
            nvs_write_zip_status(false);
        } else {
            nvs_write_zip_status(true);
        }

        // Set access bits in custom1 partition to 0x0 for challenge 1e of ICSC
        set_1e_access_permission_bits();

        esp_restart();
    }

    int magic = get_magic();

    switch (magic) {
        case MAGIC_OTA:
            badge_ota_update();
            break;
        case MAGIC_FACTORY_RESET:
            factory_reset();
            break;
        default:
            micropython_entry();
    }
}
