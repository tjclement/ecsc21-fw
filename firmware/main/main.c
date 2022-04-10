#include "include/nvs_init.h"
#include "include/platform.h"
#include "include/ota_update.h"
#include "include/factory_reset.h"
#include "driver_framebuffer.h"

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "backported_efuse.h"  // Backported ESP efuse functionality from espressif 3.3
#include "backported_efuse_table.h"
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

void write_1a_flag_to_efuse() {
    printf("INFO: writing 1a flag to efuse.\n");

    uint8_t flag[] = {
        0x50, 0xd1, 0xf7, 0xf8, 0xcb, 0x5d, 0xe7, 0x65,
        0xcc, 0x0e, 0x91, 0x0a, 0x90, 0x8b, 0xa4, 0x82,
        0x2a, 0x08, 0x5e, 0xf8, 0x49, 0x1d, 0x1f, 0xee
    };

    if (esp_efuse_write_block(EFUSE_BLK2, flag, 0, 192) != ESP_OK) {
        printf("ERROR: efuse write block failed. The CTF flag for 1a is potentially not set!\n");
    }
}

void set_1d_flag_in_rtc_mem() {
    const char* flag = "CTF{5b37698be4993691588502823f7d54966634f144aada030e}";

    char* target = 0x3FF80000;
    memcpy(target, flag, strlen(flag));
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

        // Write flag for challange 1a to EFUSE_BLK2 at offset 0
        write_1a_flag_to_efuse();

        // Set access bits in custom1 partition to 0x0 for challenge 1e of ICSC
        set_1e_access_permission_bits();

        esp_restart();
    }

    // Write flag for 1d to RTC_FAST memory at offset 0
    set_1d_flag_in_rtc_mem();

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
