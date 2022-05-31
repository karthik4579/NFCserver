import board
import busio
import textwrap
import digitalio
from digitalio import DigitalInOut
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
from adafruit_pn532.spi import PN532_SPI
from firebasecmp import cmp
from gpiozero import Servo
from gpiozero import LED
from time import sleep
from firebaselog import log


spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D8)
pn532 = PN532_SPI(spi, cs_pin, debug=False)


# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

key = b"\xFF\xFF\xFF\xFF\xFF\xFF"


myGPIO = 27  # servo

myCorrection = 0.50

maxPW = (2.0+myCorrection)/1000
minPW = (1.0-myCorrection)/1000

servo = Servo(myGPIO, min_pulse_width=minPW, max_pulse_width=maxPW)

Yellow = LED(23)

def read():
    global uid
    while True:
        Yellow.on()
        sleep(0.5)
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            if uid is not None:
                break
        tmp = []
        # Read the data
        try :
            authenticated0 = pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
            r0 = str(pn532.mifare_classic_read_block(4), 'utf-8')
            tmp.append(r0)


            authenticated1 = pn532.mifare_classic_authenticate_block(uid, 5, MIFARE_CMD_AUTH_B, key)
            r1 = str(pn532.mifare_classic_read_block(5), 'utf-8')
            tmp.append(r1)


            authenticated2 = pn532.mifare_classic_authenticate_block(uid, 6, MIFARE_CMD_AUTH_B, key)
            r2 = str(pn532.mifare_classic_read_block(6), 'utf-8')
            tmp.append(r2)

            authenticated3 = pn532.mifare_classic_authenticate_block(uid, 8, MIFARE_CMD_AUTH_B, key)
            r3 = str(pn532.mifare_classic_read_block(8), 'utf-8')
            tmp.append(r3)

            authenticated4 = pn532.mifare_classic_authenticate_block(uid, 9, MIFARE_CMD_AUTH_B, key)
            r4 = str(pn532.mifare_classic_read_block(9), 'utf-8')
            tmp.append(r4)

            authenticated5 = pn532.mifare_classic_authenticate_block(uid, 10, MIFARE_CMD_AUTH_B, key)
            r5 = str(pn532.mifare_classic_read_block(10), 'utf-8')
            tmp.append(r5)

            authenticated6 = pn532.mifare_classic_authenticate_block(uid, 12, MIFARE_CMD_AUTH_B, key)
            r6 = str(pn532.mifare_classic_read_block(12), 'utf-8')
            tmp.append(r6)
        except:
            continue


        tmpstr = "".join(tmp)
        finalstr = tmpstr.replace("#", "")
        uname = list(finalstr.split(":"))

        a = cmp(finalstr)
        if a == None:
            uid = None
            Yellow.off()
            sleep(0.5)
            Yellow.on()
            continue

        else:
            uid = None
            servo.max()
            log(uname[0])
            Yellow.off()
            sleep(1)
            Yellow.on()
            sleep(5)
            Yellow.off()
            sleep(1)
            servo.min()
            continue

if __name__ == '__main__':
    read()
