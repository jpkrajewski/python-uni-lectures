import serial

ser = serial.Serial(port='COM4', timeout=5)

data = []

ser.write(b'Ping')
x = ser.read()

print(x.decode())

ser.write(b'rand')
data.append(ser.read(1000))

ser.write(b'file load 10 10')
data.append(ser.read(1000))

print(data) 
ser.close()