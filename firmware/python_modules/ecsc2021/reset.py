import machine, system

machine.nvs_setint('system', 'factory_checked', 1)
system.reboot()