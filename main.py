import os
import sys
from time import sleep
from machine import ADC, RTC, Pin
from LCD import CharLCD
import math

# Inputs/Outputs
temoin = Pin(25, Pin.OUT)
pin13 = Pin(13, Pin.IN, Pin.PULL_UP)
pin14 = Pin(14, Pin.IN, Pin.PULL_UP)
pin15 = Pin(15, Pin.IN, Pin.PULL_UP)
lcd = CharLCD(rs=2, en=4, d4=7, d5=8, d6=9, d7=10, cols=16, rows=2)
button_1 = 0
button_2 = 0
button_3 = 0
#Variables and values for the temperature
adc = ADC(27)
value = 0
resistance = 0
temperature = 0
v_m = 0
R_REF = 2200
R_FIXE = 1000
V_TOT = 3.3
A = -14.6337
B = 4791.842
C = -115334
D = -3.730535*10**6
A1 = 0.003354016
B1 = 0.000256985
C1 = 0.000002620131
D1 = 0.00000006383091

# Allows you to display two lines that you fill in
def display(phrase1, phrase2):
    lcd.set_line(0) 
    lcd.message(phrase1)
    lcd.set_line(1) 
    lcd.message(phrase2)
    
def update_buttons_states():
    # Set the button_1 button_2 button_3 to the values of the buttons
    if pin13.value() == 0 :
        button_1 = 1
    else :
        button_1 = 0
    if pin14.value() == 0 :
        button_2 = 1
    else :
        button_2 = 0
    if pin15.value() == 0 :
        button_3 = 1
    else :
        button_3 = 0
        
def update_temperature():
    # Calculate the temperature
    value = adc.read_u16()
    v_m = 3.3/pow(2,16)*value
    resistance = R_FIXE*V_TOT/v_m - R_FIXE
    temperature = (A1 + B1*math.log(resistance/R_REF)+C1*math.log(resistance/R_REF)**2+D1*math.log(resistance/R_REF)**3)**-1
    temperature = temperature - 273.15
    display("%f" % temperature,"")

if "mode.txt" in os.listdir():
    with open("mode.txt", "r") as f:
        lines_list = f.readlines()
    mode = int(lines_list[0].split(":")[1]) # 0 : thermostat ; 1 : séchoir a fruits

    if mode != 0 and mode != 1:
        print("mode incorrect")
        sys.exit()
    else :
        print("Mode : ",mode )
    
else :
    print("création du fichier")
    with open("mode.txt", "a") as f:
        f.write("mode:0\n")
    print("fichier crée")
    print("mode sur mis sur 0")

# Indicator of proper functioning
temoin.on()

# Main
while True:
    update_buttons_states()
    update_temperature()

    
    sleep(0.1)

