import gc
import machine, time

# Basics for receiving:
# * Startup by enabling the IR receiver to eat power
# * Enable an interrupt (hardware) for receiving the initial pulse
# * When the interrupt is fired disable the rest of the interrupts for the duration of this read
# * Read the pulses with time_pulse_us (it's extremely fast)
# * Store this in a buffer with a fixed size, (256 empty arrays)
# * Set a timer to decode the data instantly after interrupts are enabled again.
# * a class can inherit this class and just define a decoder and specify a send pattern
# * if a send pattern is not the way to go (some totally different protocols) you can just implement another tx function

class BadgeIr():
    freq = 38000
    ticks = 500
    start = 4000
    rxpin = 18
    txpin = 19
    rxenablepin = 21
    rxtimer = None
    readcallback = None
    bitform = []
    pwm_tx = None

    def __init__(self, pins = None, badge = None, freq=38000):
        self.freq = freq

        if pins:
            self.rxpin = pins[0]
            self.txpin = pins[1]
            self.rxenablepin = pins[3]
        elif badge == 'Hackerhotel_2019':
            self.rxpin = 12
            self.txpin = 14
            self.rxenablepin = -1
        elif badge == 'Disobey_2019':
            self.rxpin = 18
            self.txpin = 19
            self.rxenablepin = 21
        elif badge == 'ecsc2021':
            self.rxpin = 36
            self.txpin = 14
            self.rxenablepin = -1
        else:
            raise("Please provide badge name or pin numbers [rx, tx, rxEnable], enter -1 for rxEnable if it is not used!")
    def initbuffer(self):
        self.buffer=[[]] * 256
        self.bufpos = 0
    # If it returns 1 the buffer gets emptied out and initialized.
    # This is the default, protocol implementations should choose if they want to.
    def decoder(self):
        return 1
    def real_decoder(self,timer):
        # print("Real decoder called.")
        self.rxtimer.deinit()
        self.rxtimer = None
        if self.decoder():
            self.initbuffer()
    def cleanbuffer(self,i):
        self.buffer=self.buffer[i:256]+[[]]*i
        self.bufpos-=i
        gc.collect()
    def mr(self):
        if self.bufpos == len(self.buffer):
            return 0
        waitfor=0 if self.pin_rx.value() else 1
        while True:
            t=machine.time_pulse_us(self.pin_rx,waitfor,50*1000)
            if t<0:
                if t == -2:
                    return 1
                return 0
            elif t>0:
                waitfor = 0 if waitfor else 1
                self.buffer[self.bufpos]=[waitfor,round(t/self.ticks)]
                self.bufpos+=1
                if self.bufpos == len(self.buffer):
                    return 1
    def callback(self,pin):
        # print("Callback.")
        irqs = machine.disable_irq()
        hasdata = self.mr()
        machine.enable_irq(irqs)
        if hasdata and not self.rxtimer:
            self.rxtimer = machine.Timer(2)
            self.rxtimer.init(mode=machine.Timer.ONE_SHOT, period=1,callback=self.real_decoder)

    def rx_enable(self):
        if self.rxenablepin >= 0:
            self.pin_rx_enable = machine.Pin(self.rxenablepin, machine.Pin.OUT)
        pullup = None if 34 <= self.rxpin <= 39 else machine.Pin.PULL_UP
        self.pin_rx = machine.Pin(self.rxpin, machine.Pin.IN, pullup, trigger=machine.Pin.IRQ_FALLING, handler=self.callback)
        self.initbuffer()
        if self.rxenablepin >= 0:
            self.pin_rx_enable.value(True)
    def rx_disable(self):
        self.pin_rx = None
        if self.rxenablepin >= 0:
            self.pin_rx_enable.value(False)
    def tx_enable(self):
        if not self.pwm_tx:
            self.pin_tx        = machine.Pin(self.txpin, machine.Pin.OUT)
            self.pwm_tx        = machine.PWM(self.pin_tx, freq = self.freq, duty = 0)
    def tx_disable(self):
        self.pwm_tx.duty(0)
    def tx_setduty(self,duty):
        self.pwm_tx.duty(duty)
    def txBit(self,bit):
        for (on,tijd) in self.bitform[bit]:
            self.tx_setduty(50 if on else 0)
            time.sleep_us(tijd)
    def txByte(self,byte):
        for bit in range(8):
            self.txBit( ( byte >> ( 7 - bit ) ) & 1 ) # MSB


class NecIR(BadgeIr):
    # Implements NEC Infrared
    # Example:
    #    IR=NecIR()
    #    NecIR.command= <function (address,command)>
    #    NecIR.repeat=  <function ()>
    #    NecIR.rx_enable()
    #  To stop receiving:
    #    NecIR.rx_disable()
    #  To send:
    #    NecIR.tx(<byte address>,<byte command>)
    #    NecIR.tx_repeat()
    command = None
    repeat = None
    bitform = { 0: [[1,562],[0,562]], 1: [[1,562],[0,1687]], 's': [[1,9000],[0,4500]], 'e': [[1,562],[0,100]], 'r': [[1,9000],[0,2500],[1,562],[0,100]] }

    def tx(self,addr,cmd):
        self.tx_enable()
        self.txBit('s')
        self.txByte(addr)
        self.txByte(addr ^ 0xFF)
        self.txByte(cmd)
        self.txByte(cmd ^ 0xFF)
        self.txBit('e')
        self.tx_disable()

    def tx_repeat(self):
        self.txBit('r')

    def decoder(self):
        decoded=0
        i=0
        while True and self.bufpos-i>0:
            (val,time)=self.buffer[i]
            i+=1
            if val==0 and time==9:
                if self.bufpos<66: return(0) # Not yet complete....
                p1=None
                p2=None
                bits=0
                while True and self.bufpos-i>0:
                    (val,time)=self.buffer[i]
                    i+=1
                    if time>0:
                        if p1==None:
                            p1=(val,time)
                            if bits==32 and p1[1]==1:
                                self.cleanbuffer(i)
                                if (decoded >> 24 & 0xFF) == (0xFF ^ (decoded >> 16 & 0xFF)) and (decoded >> 8 & 0xFF) == (0xFF ^ (decoded >> 0 & 0xFF)) and self.command:
                                    self.command(decoded >> 24 & 0xFF,decoded >> 8 & 0xFF)
                                return(0)
                        else:
                            p2=(val,time)
                            if p1[1]==1 and p2[1]==3:
                                decoded=decoded<<1 | 1
                                bits+=1
                            elif p1[1]==1 and p2[1]==1:
                                decoded=decoded<<1
                                bits+=1
                            if bits==32 and p2==None:
                                self.cleanbuffer(i)
                                return(0)
                            p1=None
                            p2=None
                    elif time<0:
                        self.cleanbuffer(i)
                        return(0)
            elif val==1 and time==18:
                if self.buffer[i] == [0,4] and self.buffer[i+1] == [1,1]:
                    i+=2
                    if self.repeat: self.repeat()
                    return(0)
        self.cleanbuffer(i)
        return(0)

class CustomIR(BadgeIr):
    # Implements custom Infrared protocol for 4-byte transfers using NEC timing
    # Example:
    #    IR=CustomIR()
    #    CustomIR.command= <function (data1, data2, data3, data4)>
    #    CustomIR.repeat=  <function ()>
    #    CustomIR.rx_enable()
    #  To stop receiving:
    #    CustomIR.rx_disable()
    #  To send:
    #    CustomIR.tx(<byte data1>,<byte data2>,<byte data3>,<byte data4>)
    #    CustomIR.tx_repeat()
    command = None
    repeat = None
    bitform = { 0: [[1,562],[0,562]], 1: [[1,562],[0,1687]], 's': [[1,9000],[0,4500]], 'e': [[1,562],[0,100]], 'r': [[1,9000],[0,2500],[1,562],[0,100]] }

    def tx(self,data1,data2,data3,data4):
        self.tx_enable()
        self.txBit('s')
        self.txByte(data1)
        self.txByte(data2)
        self.txByte(data3)
        self.txByte(data4)
        self.txBit('e')
        self.tx_disable()

    def tx_repeat(self):
        self.txBit('r')

    def decoder(self):
        decoded=0
        i=0
        while True and self.bufpos-i>0:
            (val,time)=self.buffer[i]
            i+=1
            if val==0 and time==9:
                if self.bufpos<66: return(0) # Not yet complete....
                p1=None
                p2=None
                bits=0
                while True and self.bufpos-i>0:
                    (val,time)=self.buffer[i]
                    i+=1
                    if time>0:
                        if p1==None:
                            p1=(val,time)
                            if bits==32 and p1[1]==1:
                                self.cleanbuffer(i)
                                self.command(decoded >> 24 & 0xFF, decoded >> 16 & 0xFF,
                                             decoded >> 8 & 0xFF, decoded & 0xFF)
                                return(0)
                        else:
                            p2=(val,time)
                            if p1[1]==1 and p2[1]==3:
                                decoded=decoded<<1 | 1
                                bits+=1
                            elif p1[1]==1 and p2[1]==1:
                                decoded=decoded<<1
                                bits+=1
                            if bits==32 and p2==None:
                                self.cleanbuffer(i)
                                return(0)
                            p1=None
                            p2=None
                    elif time<0:
                        self.cleanbuffer(i)
                        return(0)
            elif val==1 and time==18:
                if self.buffer[i] == [0,4] and self.buffer[i+1] == [1,1]:
                    i+=2
                    if self.repeat: self.repeat()
                    return(0)
        self.cleanbuffer(i)
        return(0)


class SamsungIR(BadgeIr):
    # Implements Samsung Infrared
    # Example:
    #    IR=SamsungIR()
    #    SamsungIR.command= <function (long data)>
    #    SamsungIR.repeat=  <function ()>
    #    SamsungIR.rx_enable()
    #  To stop receiving:
    #    SamsungIR.rx_disable()
    #  To send:
    #    SamsungIR.tx(<long data>,<int datalen in bits>)
    #    SamsungIR.tx_repeat()
    command = None
    repeat = None
    bitform = { 0: [[1,560],[0,560]], 1: [[1,560],[0,1600]], 's': [[1,4500],[0,4500]], 'e': [[1,562],[0,100]], 'r': [[1,4500],[0,2250],[1,562],[0,100]] }
    ticks = 250

    def tx(self,data,bits):
        self.tx_enable()
        self.txBit('s')
        for mask in range(0,bits):
            self.txBit((data >> (bits-mask)) & 1)
        self.txBit('e')
        self.tx_disable()

    def tx_repeat(self):
        self.txBit('r')

    def decoder(self):
        decoded=0
        i=0
        while True and self.bufpos-i>0:
            (val,time)=self.buffer[i]
            i+=1
            if val==0 and time==18:
                if self.bufpos<10: return(0) # Not yet complete....
                if self.buffer[i] == [0,9] and self.buffer[i+1] == [1,2]:
                    i+=2
                    if self.repeat: self.repeat()
                    return(0)
                p1=None
                p2=None
                bits=0
                while True and self.bufpos-i>0:
                    (val,time)=self.buffer[i]
                    i+=1
                    if time>0:
                        if p1==None:
                            p1=(val,time)
                            if bits==32 and p1[1]==1:
                                self.cleanbuffer(i)
                                self.command(decoded)
                                return(0)
                        else:
                            p2=(val,time)
                            if p1[1]==2 and p2[1]==6:
                                decoded=decoded<<1 | 1
                                bits+=1
                            elif p1[1]==2 and p2[1]==2:
                                decoded=decoded<<1
                                bits+=1
                            if bits==32 and p2==None:
                                self.cleanbuffer(i)
                                return(0)
                            p1=None
                            p2=None
                    elif time<0:
                        self.cleanbuffer(i)
                        return(0)
        self.cleanbuffer(i)
        return(0)

class NokiaIR(BadgeIr):
    # Implements Nokia Infrared
    # Example:
    #    IR=NokiaIR()
    #    NokiaIR.command= <function (command,address,subcode)>
    #    NokiaIR.rx_enable()
    #  To stop receiving:
    #    NokiaIR.rx_disable()
    #  To send:
    #    NokiaIR.tx(command,address,subcode)
    #    NokiaIR.tx_repeat()
    command = None
    repeat = None
    bitform = { 0: [[0,500],[1,500]], 1: [[1,500],[0,500]], 's': [[1,500],[0,2500]], 'e': [[1,500],[0,100]] }
    ticks = 250

    def tx(self,command,address,subcode):
        self.tx_enable()
        self.txBit('s')
        for mask in range(0,8):
            self.txBit((command >> (mask)) & 1)
        for mask in range(0,4):
            self.txBit((address >> (mask)) & 1)
        for mask in range(0,4):
            self.txBit((subcode >> (mask)) & 1)
        self.txBit('e')
        self.tx_disable()

    def decoder(self):
        decoded=0
        i=0
        while True and self.bufpos-i>0:
            (val,time)=self.buffer[i]
            i+=1
            if val==0 and time==9:
                if self.bufpos<66: return(0) # Not yet complete....
                p1=None
                p2=None
                bits=0
                while True and self.bufpos-i>0:
                    (val,time)=self.buffer[i]
                    i+=1
                    if time>0:
                        if p1==None:
                            p1=(val,time)
                            if bits==32 and p1[1]==1:
                                self.cleanbuffer(i)
                                if (decoded >> 24 & 0xFF) == (0xFF ^ (decoded >> 16 & 0xFF)) and (decoded >> 8 & 0xFF) == (0xFF ^ (decoded >> 0 & 0xFF)) and self.command:
                                    self.command(decoded >> 24 & 0xFF,decoded >> 8 & 0xFF)
                                return(0)
                        else:
                            p2=(val,time)
                            if p1[1]==1 and p2[1]==3:
                                decoded=decoded<<1 | 1
                                bits+=1
                            elif p1[1]==1 and p2[1]==1:
                                decoded=decoded<<1
                                bits+=1
                            if bits==32 and p2==None:
                                self.cleanbuffer(i)
                                return(0)
                            p1=None
                            p2=None
                    elif time<0:
                        self.cleanbuffer(i)
                        return(0)
            elif val==1 and time==18:
                if self.buffer[i] == [0,4] and self.buffer[i+1] == [1,1]:
                    i+=2
                    if self.repeat: self.repeat()
                    return(0)
        self.cleanbuffer(i)
        return(0)