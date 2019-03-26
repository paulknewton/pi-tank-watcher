"""Display water tank message on LCD. Currently unused."""
import time
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

# 2 line LCD
lcd_columns = 16
lcd_rows = 2

# Initialise I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialise the LCD class
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

lcd.clear()
lcd.color = [100, 0, 0]

# read latest message
file = open("sample-lcd-msg.txt", "r")
msg = file.readlines()

# assumes water level is the 1st line
water = msg[0]
for line in msg[1:]:
    row1 = water.rstrip()
    row2 = line.rstrip()

    lcd.clear()
    message = row1 + "\n" + row2
    lcd.message = message
    print(row1 + "\n" + row2)

    time.sleep(2)

    # scroll long messages up
    while len(row2) > 16:
        row1 = row2
        row2 = row2[16:]
        message = row1 + "\n" + row2
        time.sleep(0.3)
        lcd.clear()
        lcd.message = message
        print("-----\n" + message)

    time.sleep(2)  # wait before moving to next message

# Turn off LCD backlights and clear text
lcd.color = [0, 0, 0]
lcd.clear()
