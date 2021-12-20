import easydraw, machine, display
machine.nvs_setint('system', 'jobs_unlocked', 1)
display.drawPng(90, 20, '/private/system/logo_small.png')
easydraw.messageCentered('Congratulations\n\n\nYou\'ve shown yourself to be capable enough. You are now one of us. The job board on your home screen has been unlocked.\n\nCheck it out, or finish the remaining challenges to increase your ranking.')
