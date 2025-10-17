import os
from time import sleep
from machine import ADC, RTC, Pin
from LCD import CharLCD
import math
import time

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
#Useful variables
temperature_list = []
menu = 0 # 0: main menu ; # 1: temperature menu
language = -1
password = 000000


# Allows you to display two lines that you fill in
def display(phrase1, phrase2):
    lcd.set_line(0) 
    lcd.message(phrase1)
    lcd.set_line(1) 
    lcd.message(phrase2)
    
def update_buttons_states():
    # Set the button_1 button_2 button_3 to the values of the buttons
    global button_1
    global button_2
    global button_3
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
    global temperature
    value = adc.read_u16()
    v_m = 3.3/pow(2,16)*value
    resistance = R_FIXE*V_TOT/v_m - R_FIXE
    temperature = (A1 + B1*math.log(resistance/R_REF)+C1*math.log(resistance/R_REF)**2+D1*math.log(resistance/R_REF)**3)**-1
    temperature = temperature - 273.15
    
def save_temperature():
    line = ""
    for string in temperature_list :
        line = line + string + ";"
    line = line[:(len(line)-1)]
    print(line)
    with open("datas.txt", "w") as f:
        f.write(line)
    print("saved !")


    
def update_language():
    global button_1
    global button_2
    global language
    lcd.clear()
    language = -1
    while language == -1 :
        display("1.English","2.French")
        update_buttons_states()
        if button_1 :
            language = 0
            button_1 = 0
            display("               ","               ")
            display("English choosed","")
            sleep(1)
            lcd.clear()
        if button_2 :
            language = 1
            button_2 = 0
            display("               ","               ")
            display("Francais choisie","")
            sleep(1)
            lcd.clear()
    with open("language.txt","w") as f:
        f.write("language:" + str(language))

def save_mode() :
    with open("mode.txt","w")as f:
        f.write("mode:" + str(mode))
    print("mode saved !")
    lcd.clear()

def update_mode():
    global button_1
    global button_2
    global mode
    global menu
    t = 0
    while button_1 == 0 and button_2 == 0 :
        update_buttons_states()
        t = t + 1
        display("1.Chauffage", "2.Climatisation")
        if button_1 :
            mode = 0
            print("1")
        elif button_2 :
            mode = 1
            print("2")
    button_1 = 0
    button_2 = 0
    save_mode()
    menu = 0
    sleep(0.5)
    
    

# Check if the language is set, put it in the "language" variale, if not, ask it and save it
if "language.txt" in os.listdir():
    with open("language.txt","r") as f:
        lines_list = f.readlines()
        language = int(lines_list[0].split(":")[1])
else :
    with open("language.txt","a") as f:
        update_language()
        f.write("language:" + str(language))

# Check if the mode.txt exist, if yes, set the mode value, if note ask for the mode and save it
if "mode.txt" in os.listdir():
    with open("mode.txt", "r") as f:
        lines_list = f.readlines()
    mode = int(lines_list[0].split(":")[1]) # 0 : Chauffage ; 1 : Climatisation
    print("Mode : " + str(mode))

else :
    update_mode()
    with open("mode.txt", "a") as f:
        f.write("mode:" + str(mode))

# Look if the data.txt exist, if not create it and set all values to 20c°
if "datas.txt" in os.listdir():
    with open("datas.txt", "r") as f:
        lines_list = f.readlines()
        temperature_list = lines_list[0].split(";")
else :
    with open("datas.txt", "a") as f:
        f.write("20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20")
    temperature_list = "20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20;20".split(";")
    
        

# Indicator of proper functioning
temoin.on()


# Main
while True:
    update_buttons_states()
    update_temperature()
    
    
    if menu == 0 :
        # Display actual temperature and the choose temperature
        display("T : " + f"{temperature:.2f}", "Select T : " + temperature_list[time.localtime()[3]])
        # Display the language on th right
        if language :
            string = "F"
        else :
            string = "E"
        lcd.set_cursor(15,0)
        lcd.message(string)
        # Check if button 1 and 2 is pressed
        if button_1 and button_2 and button_3:
            menu = 2
            button_1 = 0
            button_2 = 0
            button_3 = 0
            lcd.clear()
            sleep(1)
        elif button_1 :
            button_1 = 0
            menu = 1 # Set to temperature menu
            lcd.clear()
            hour = time.localtime()[3]
        elif button_2 :
            button_2 = 0
            sleep(0.1)
            update_language()
    if menu == 1 :
        # Display the temperature menu
        lcd.set_cursor(0,0)
        lcd.message("<")
        lcd.set_cursor(15,0)
        lcd.message(">")
        lcd.set_cursor(7,0)
        lcd.message("   ")
        lcd.set_cursor(7,0)
        lcd.message(str(hour) + "h")
        display("","-      ok      +")
        
        # Check the buttons 1 and 3 to change the hour
        sleep(0.05)
        if button_1 == 1 :
            hour = hour - 1
        if button_3 == 1 :
            hour = hour + 1
        # check if the hour stay in the range (0;24)
        if hour > 23 :
            hour = 0
        if hour < 0 :
            hour = 23
            
        if button_2 == 1 :
            menu = 1.1
            button_2 = 0
            temp = int(temperature_list[hour])

    if menu == 1.1 :
        
        print("")
        # Display the temperature/hour menu
        lcd.set_cursor(0,0)
        lcd.message("<")
        lcd.set_cursor(15,0)
        lcd.message(">")
        lcd.set_cursor(7,0)
        lcd.message("   ")
        lcd.set_cursor(7,0)
        lcd.message(str(temp) + "C")
        display("","-      ok      +")
        
        sleep(0.05)
        if button_1 == 1 :
            temp = temp - 1
        if button_3 == 1 :
            temp = temp + 1
        
        if button_2 :
            menu = 0
            button_2 = 0
            temperature_list[hour] = str(temp)
            save_temperature()
    if menu == 2 :
        display("1.change mode","2.back")
        if button_1 :
            button_1 = 0
            lcd.clear()
            menu = 2.1
            psw = ""
            number = 0
            timer = 0
            char = " "
        elif button_2 :
            menu = 0
            lcd.clear()
            
    if menu == 2.1 :
        lcd.set_cursor(0,0)
        lcd.message("-")
        lcd.set_cursor(15,0)
        lcd.message("+")
        lcd.set_cursor(7,0)
        lcd.message("   ")
        lcd.set_cursor(7,0)
        lcd.message(str(number))
        
        timer = timer + 1
        print(timer)
        if timer > 3 :
            if char == " " :
                char = "_"
            else :
                char = " "
            timer = 0
        lcd.set_cursor(0,1)
        lcd.message(psw + char)
        
        sleep(0.05)
        if button_1 :
            button_1 = 0
            number = number - 1
        elif button_3 :
            button_3 = 0
            number = number + 1
        elif button_2 :
            button_2 = 0
            psw = psw + str(number)
            sleep(0.1)
            
            number = 0
        if number > 9 :
            number = 0
        if number < 0 :
            number = 9
            
        if len(psw) >= 6 :
            if int(psw) == password :
                lcd.clear()
                display("Right Password !","")
                menu = 2.2
            else :
                lcd.clear()
                display("Wrong Password","")
                menu = 0
            sleep(2)
            lcd.clear()
            
    if menu == 2.2 :
        update_mode()
             
        
    sleep(0.1)



