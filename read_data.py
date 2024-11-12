import serial
import csv
from datetime import datetime

def read_data(port, baud):
    ser = serial.Serial(port, baud)
    ser.flushInput()
    heading_list = ["Humidity (%)","Temperature (*C)", "Light Intensity", "Time"]

    with open("data.csv", "w+", newline='') as file: # empties data from csv file before writing headings
        writer = csv.writer(file)
        writer.writerow(heading_list)

    data = []
    while True:
        try:
            ser_bytes = ser.readline()
            decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            data.append(decoded_bytes)

            if len(data) == 3:
                data.append(current_time)
                with open("data.csv","a", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)
                    data = []
        except:
            print("Keyboard Interrupt")
            break

read_data("COM5", 9600)