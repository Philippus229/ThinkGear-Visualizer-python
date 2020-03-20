import serial, math, pygame

codes = [0x02,     0x03,       0x04,       0x05,        0x06,      0x80,     0x83      ]
names = ["quality","heartrate","attention","meditation","8bit_raw","eeg_raw","eeg_asic"]
c_len = [1,        1,          1,          1,           1,         3,        25        ]

bands = ["delta","theta","low-alpha","high-alpha","low-beta","high-beta","low-gamma","mid-gamma"]

#convert signed bit/byte array to int
def signed_thing_to_int(b, length):
    return b-((b >> (length-1)) & 1)*2**length #if first bit is 0, return b, otherwise subtract max value representable with given number of bits and return

'''EEG Device Class'''
class ThinkGear(object):
    def __init__(self, port, baudrate=57600):
        self.ser = serial.Serial(port, baudrate) #initialize serial communication/connection
        self.data = {}

    def fetch_data(self):
        self.data = {} #reset values
        while True:
            self.ser.read_until(b"\xAA\xAA") #wait for sync bytes
            plength = ord(self.ser.read(1)) #payload length
            payload = self.ser.read(plength) #read entire payload of given length
            checksum = ~(int(math.fsum([b for b in payload])) & 0xFF) & 0xFF #calculate checksum by doing... checksum-calculation stuff (described in the docs)
            if checksum == ord(self.ser.read(1)): break #checksums match, move on
            else: print("ERROR: Checksum mismatch!") #checksum mismatch, repeat
        i = 0
        while i < len(payload)-1:
            code = payload[i]
            if code in codes: #check if current byte is a supported code
                c = codes.index(code) #find corresponding index in the three code-related lists above
                '''old code which I prefer (because it's technically one line) (sadly without a way to add comments)
                self.data[names[c]] = payload[i+1] if c < 5 \
                                        else signed_thing_to_int(payload[i+2] << 8 | payload[i+3], 16) if c == 5 \
                                        else dict(zip(bands, [payload[b] << 16 | payload[b+1] << 8 | payload[b+2] for b in range(i+1, i+25, 3)]))
                '''
                if c < 5: #all single-byte codes (quality, heartrate, attention, meditation, 8bit_raw)
                    self.data[names[c]] = payload[i+1]
                elif c == 5: #eeg_raw (fun fact: the first byte after the code is completely useless)
                    self.data[names[c]] = signed_thing_to_int(payload[i+2] << 8 | payload[i+3], 16)
                elif c == 6: #eeg_asic
                    self.data[names[c]] = dict(zip(bands, [payload[b] << 16 | payload[b+1] << 8 | payload[b+2] for b in range(i+1, i+25, 3)]))
                i += c_len[c] #add code-specific number of bytes to i
            i += 1 #add 1 each time to avoid getting stuck on unused bytes

eeg_device = ThinkGear("COM7")

'''Visualization Stuff'''
vis_points = 640 #number of eeg readings to be plotted at once
size = (640, 480) #window size in pixels
x_vals = [int(size[0]*(x+0.5)/vis_points) for x in range(vis_points)]
y_vals = [int(size[1]/2) for x in range(vis_points)]
surface = pygame.display.set_mode(size) #initialize window
pygame.display.set_caption("EEG Visualizer") #...
raw_eeg_range = 8192 #technically 2*32768=65536 (2^16), but for some reason it doesn't use the full available range
#clock = pygame.time.Clock()
while True:
    try:
        #clock.tick(30)
        eeg_device.fetch_data()
        if len(eeg_device.data) == 1: y_vals = y_vals[1:]+[int(size[1]/2-size[1]*eeg_device.data["eeg_raw"]/raw_eeg_range)]
        surface.fill((0,0,0)) #Do I really need to explain this?
        points = list(zip(x_vals, y_vals)) #zip x and y values to pairs (list(zip([x0,x1,...xN], [y0,y1,...,yN])) = [(x0,y0),(x1,y1),...,(xN,yN)])
        pygame.draw.lines(surface, (255,255,255), False, points) #draw continuous line segments through points
        pygame.display.flip() #display changes
    except KeyboardInterrupt: #I don't even know if this works, heck. <insert wrinkly Pikachu>
        pygame.quit()
