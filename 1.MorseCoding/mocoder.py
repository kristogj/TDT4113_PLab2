import arduino_connect

               #MÅ fikse slik at loopen fortsetter selv om man ikke finner symbol

class Mocoder:
    #
    def __init__(self):
        self.serial_port = arduino_connect.basic_connect(); #porten som arduino skriver til og python leser fra
        self.current_symbol = ""; #symbolet som er under konstruksjon, bokstaven
        self.current_word = ""; #ordet som er under konstruksjon



        #0 = dot and 1 = dash
        self.morse_codes = {'01':'a','1000':'b','1010':'c', '100':'d','0':'e','0010':'f','110':'g','0000':'h',
                              '00':'i','0111':'j','101':'k','0100':'l','11':'m','10':'n','111':'o',
                              '0110':'p','1101':'q','010':'r','000':'s','1':'t','001':'u','0001':'v',
                              '011':'w','1001':'x','1011':'y','1100':'z','01111':'1','00111':'2',
                              '00011':'3','00001':'4','00000':'5','10000':'6','11000':'7','11100':'8',
                              '11110':'9','11111':'0'}


    def get_morse_codes(self):
        return self.morse_codes

    #Read the next signal from serial port and return it
    def read_one_signal(self,port=None):
        #Mottar et signal mellom 0 og 3
        connection = port if port else self.serial_port
        while True:
            #Leser data fra arduino serial connection
            data = connection.readline()
            if data:
                return data


    #Les motatt signal og kall på en av flere metoder utifra type signal
    #hvis dot eller dash kall update_current_symbol
    #hvis pause kall handle:symbol_end eller handle_word_end avhengig av type pause
    def process_signal(self,signal):
        if (signal == 0 or signal == 1):
            self.update_current_symbol(signal)
        elif signal == 2:
            self.handle_symbol_end()
        elif signal == 3:
            self.handle_word_end()


    #Legg til dot eller dash (0,1) på slutten av current_symbol
    def update_current_symbol(self,signal):
        self.current_symbol += str(signal)

    #Når koden for et symbol ender, bruk den koden som key inn i morse_codes
    #for å finne passende symbol, som er da brukt for å kalle update_current_word
    #Slutt reset current_symbol til tom streng
    def handle_symbol_end(self):
        #Trenger exception hvis jeg skriver feil
        try:
            symbol = self.morse_codes[self.current_symbol]
            self.update_current_word(symbol)
            self.current_symbol = ""
        except KeyError:
            self.current_symbol = ""


    #Legg til siste symbol inn i current_word
    def update_current_word(self,symbol):
        self.current_word += symbol

    #Burde begynne med å kalle handle_sybol_end;
    #Skal så printe current_word til skjerrmen og tilslutt, reset current_word til tom streng
    def handle_word_end(self):
        #self.handle_symbol_end()
        print(self.current_word)
        self.current_word = ""

    def loop(self):
        while True:
            s = self.read_one_signal(self.serial_port)
            print(s)
            #kommer gjennom som bytes
            #lengde enten 1 eller 2

            if len(s) == 2:
                self.process_signal(int(chr(s[0])))
                self.process_signal(int(chr(s[1])))

            else:
                self.process_signal(int(s))

def main():
    code = Mocoder()
    code.loop()

main()


