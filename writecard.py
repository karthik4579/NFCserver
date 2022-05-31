import board
import busio
import textwrap
import time
import digitalio
import sys
from digitalio import DigitalInOut
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
from adafruit_pn532.spi import PN532_SPI
from gpiozero import LED


spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D8)
pn532 = PN532_SPI(spi, cs_pin, debug=False)
# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()
Yellow = LED(23) 
Red = LED(24)
key = b"\xFF\xFF\xFF\xFF\xFF\xFF"

def addchr(b):
    c = textwrap.wrap(b, 1)
    length= len(c)
    if length < 16:
        index = 16 - length
        for i in range(index):
            c.append("#")
        b6_1 = bytearray("".join(c).encode())
        return b6_1
    else:
        return bytearray("".join(c).encode())

    
def write(a, f):
    Yellow.off()
    time.sleep(0.5)
    Red.on()
    time.sleep(0.5)
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        # Try again if no card is available.
        if uid is not None:
            break
        else:
            continue

    if f == "reset":
        password = a
        mes = str(password)
        tmp = textwrap.wrap(mes, width=16)

        b0 = addchr(tmp[0])
        b1 = addchr(tmp[1])
        b2 = addchr(tmp[2])
        b3 = addchr(tmp[3])
        b4 = addchr(tmp[4])
        b5 = addchr(tmp[5])
        b6 = addchr(tmp[6])
        

        #Prepare data for all the 7 blocks to be written
        data0 = b0
        data1 = b1
        data2 = b2
        data3 = b3
        data4 = b4
        data5 = b5
        data6 = b6


        # Write 16 bytes to block 4.
        authenticated0 = pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
        pn532.mifare_classic_write_block(4, data0)



        # Write 16 bytes to block 5.
        authenticated1 = pn532.mifare_classic_authenticate_block(uid, 5, MIFARE_CMD_AUTH_B, key)
        pn532.mifare_classic_write_block(5, data1)



        # Write 16 bytes to block 6.
        authenticated2 = pn532.mifare_classic_authenticate_block(uid, 6, MIFARE_CMD_AUTH_B, key)
        pn532.mifare_classic_write_block(6, data2)



        # Write 16 bytes to block 8.
        authenticated3 = pn532.mifare_classic_authenticate_block(uid, 8, MIFARE_CMD_AUTH_B, key)
        pn532.mifare_classic_write_block(8, data3)



        # Write 16 bytes to block 9.
        authenticated4 = pn532.mifare_classic_authenticate_block(uid, 9, MIFARE_CMD_AUTH_B, key)
        pn532.mifare_classic_write_block(9, data4)



        # Write 16 bytes to block 10.
        authenticated5 = pn532.mifare_classic_authenticate_block(uid, 10, MIFARE_CMD_AUTH_B, key)
        pn532.mifare_classic_write_block(10, data5)


        # Write 16 bytes to block 12.
        authenticated6 = pn532.mifare_classic_authenticate_block(uid, 12, MIFARE_CMD_AUTH_B, key)
        pn532.mifare_classic_write_block(12, data6)
        Red.off()
        time.sleep(2)
        return "done"

    elif f == "register":
        password = a
        mes = str(password)
        tmp = textwrap.wrap(mes, width=16)

        b0 = addchr(tmp[0])
        b1 = addchr(tmp[1])
        b2 = addchr(tmp[2])
        b3 = addchr(tmp[3])
        b4 = addchr(tmp[4])
        b5 = addchr(tmp[5])
        b6 = addchr(tmp[6])
        

        #Prepare data for all the 7 blocks to be written
        data0 = b0
        data1 = b1
        data2 = b2
        data3 = b3
        data4 = b4
        data5 = b5
        data6 = b6


        # Write 16 bytes to block 4.
        authenticated0 = pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
        pn532.mifare_classic_write_block(4, data0)



        # Write 16 bytes to block 5.
        authenticated1 = pn532.mifare_classic_authenticate_block(uid, 5, MIFARE_CMD_AUTH_B, key)
        pn532.mifare_classic_write_block(5, data1)


        # Write 16 bytes to block 6.
        authenticated2 = pn532.mifare_classic_authenticate_block(uid, 6, MIFARE_CMD_AUTH_B, key)
        pn532.mifare_classic_write_block(6, data2)



        # Write 16 bytes to block 8.
        authenticated3 = pn532.mifare_classic_authenticate_block(uid, 8, MIFARE_CMD_AUTH_B, key)
        pn532.mifare_classic_write_block(8, data3)



        # Write 16 bytes to block 9.
        authenticated4 = pn532.mifare_classic_authenticate_block(uid, 9, MIFARE_CMD_AUTH_B, key)
        pn532.mifare_classic_write_block(9, data4)



        # Write 16 bytes to block 10.
        authenticated5 = pn532.mifare_classic_authenticate_block(uid, 10, MIFARE_CMD_AUTH_B, key)
        pn532.mifare_classic_write_block(10, data5)


        # Write 16 bytes to block 12.
        authenticated6 = pn532.mifare_classic_authenticate_block(uid, 12, MIFARE_CMD_AUTH_B, key)
        pn532.mifare_classic_write_block(12, data6)
        Red.off()
        time.sleep(3)
        return uid

if __name__ == '__main__':
    vals = sys.argv
    if vals[2] == "reset":
        g = write(vals[1],vals[2])
        print(g)
    elif vals[2] == "register":
        a = write(vals[1],vals[2]) # val1 is password and val2 activity
        c = [hex(i) for i in a]
        st = ""
        f = st.join(c)
        print(f)