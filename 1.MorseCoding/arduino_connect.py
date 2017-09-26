import serial

# Connects to the arduino via a COM port (USB).
# Does not work if the serial monitor in arduino is open.
def pc_connect():
    for i in range(100):
        try:
            arduino = serial.Serial('COM' + str(i), 9600, timeout=.1)
            print("Connected to arduino")
            return arduino
        except serial.SerialException:
            pass
    exit("Arduino was not found")

# arport = Arduino device port, which you can find at the bottom of your arduino window or via Arduino menu options tools/port.
#   The default will probably NOT work for your machine, but it may look quite similar (for Mac users), differing only
#  in the final 4 digits.

def basic_connect(arport='/dev/cu.wchusbserial1410'):
    return serial.Serial(arport,9600,timeout=.1)