from machine import Pin, PWM

class DRL9110(object):   
 
    def __init__(self, in1, in2, freq=1000):        
        self.freq = freq
        self.speed = 0
        self.p_in2 = Pin(in2, Pin.OUT)
        self.p_in1 = PWM(Pin(in1), freq=self.freq, duty=self.speed) # duty 0-1023       
        self.p_in2.value(0)

    def stop(self):    
        self.p_in2.value(0)
        self.p_in1.duty(0)

    def forward(self):
        self.p_in2.value(0)
        self.p_in1.duty(self.speed)

    def reverse(self):
        self.p_in2.value(1)
        self.p_in1.duty(1023-self.speed)

    def set_speed(self, speed):
        self.speed = min(1023, max(0, int(speed)))



