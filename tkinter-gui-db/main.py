from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from conn import Database
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime
from functools import partial


class Validator:
    @staticmethod
    def validate_types_of_measurements(temperature, humidity, voltage):
        if not temperature and not humidity and not voltage:
            raise ValueError("You must choose at least one type of measurement.")

        return True

    @staticmethod
    def check_device_id(device_name):
        if Devices.get_device_id(device_name) is None:
            raise ValueError("Device not found.")

        return True

    @staticmethod
    def check_start_date(start):
        if start:
            try:
                return datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("Start time is not valid date.")

        return None

    @staticmethod
    def check_stop_date(stop):
        if stop:
            try:
                return datetime.strptime(stop, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("Stop time is not valid date.")

        return None

    def validate_dates(self, start, stop):
        validated_start = self.check_start_date(start)
        validated_stop = self.check_stop_date(stop)

        if validated_start and validated_stop and validated_start > validated_stop:
            raise ValueError("Start time must be less or equal to stop time.")

        return True

    def validate_all(self, device_name, temperature, humidity, voltage, start, stop):
        errors = ""

        try:
            self.validate_types_of_measurements(temperature, humidity, voltage)
        except ValueError as e:
            errors += str(e) + "\n"

        try:
            self.check_device_id(device_name)
        except ValueError as e:
            errors += str(e) + "\n"

        try:
            self.validate_dates(start, stop)
        except ValueError as e:
            errors += str(e) + "\n"

        return errors


class Devices:
    devices = dict()

    def __init__(self):
        self.conn = Database()
        self.get_devices_from_database()

    @staticmethod
    def get_device_names_list():
        return list(Devices.devices.keys())

    @staticmethod
    def get_device_id(name):
        try:
            return Devices.devices[name]
        except KeyError:
            return None

    @staticmethod
    def make_data_columns_list(temperature, humidity, voltage):
        columns = ['time']

        if temperature:
            columns.append('temperature')

        if voltage:
            columns.append('voltage')

        if humidity:
            columns.append('humidity')

        return columns

    def get_devices_from_database(self):
        devices = self.conn.fetch("SELECT id, name FROM devices")
        for device in devices:
            Devices.devices[device[1]] = device[0]

    def device_probes_from_database(self, device_name, temperature, humidity, voltage, start, stop):
        dev_id = self.get_device_id(str(device_name))
        columns = self.make_data_columns_list(temperature, humidity, voltage)
        columns_joined = ','.join(columns)

        query = f"SELECT {columns_joined} FROM data WHERE device_id = {dev_id} "

        if start:
            query += f"AND time >= '{start}'"

        if stop:
            query += f"AND time <= '{stop}'"

        data = self.conn.fetch(query)
        df = pd.DataFrame(data, columns=columns)
        if df.empty:
            messagebox.showinfo("No data", "There is nothing to show")

        return df


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x500")
        self.root.title("Apka IoT")
        self.root.resizable(False, False)

        self.devices = Devices()
        self.make_controls()

    def make_controls(self):
        temperature = IntVar()
        voltage = IntVar()
        humidity = IntVar()
        device = StringVar()

        label_checkboxes = Label(self.root, text="Zaznacz typy pomiarów:")
        label_checkboxes.pack()
        temperature_checkbox = Checkbutton(self.root, text='Temperatura', variable=temperature, onvalue=1, offvalue=0)
        temperature_checkbox.pack()
        voltage_checkbox = Checkbutton(self.root, text='Napięcie', variable=voltage, onvalue=1, offvalue=0)
        voltage_checkbox.pack()
        humidity_checkbox = Checkbutton(self.root, text='Wilgotność', variable=humidity, onvalue=1, offvalue=0)
        humidity_checkbox.pack()

        label_start = Label(self.root, text="Data startowa:")
        label_start.pack()
        entry_start = Entry(self.root)
        entry_start.pack()

        label_stop = Label(self.root, text="Data końcowa:")
        label_stop.pack()
        entry_stop = Entry(self.root)
        entry_stop.pack()

        label_devices = Label(self.root, text="Dostępne urządzenia:")
        label_devices.pack()
        devices_list = Combobox(self.root, textvariable=device, state="readonly",
                                values=self.devices.get_device_names_list())
        devices_list.pack()

        submit_button = Button(self.root, text='Wyświetl wykres',
                               command=partial(self.validate_and_get_data, device, temperature, humidity, voltage,
                                               entry_start, entry_stop),
                               width=20, height=3)
        submit_button.pack()

    def validate_and_get_data(self, device, temperature, humidity, voltage, entry_start, entry_stop):
        validate = Validator()
        validate_errors = validate.validate_all(device.get(), temperature.get(), humidity.get(), voltage.get(),
                                                entry_start.get(),
                                                entry_stop.get())

        if validate_errors:
            messagebox.showerror('Error', validate_errors)
            return

        df = self.devices.device_probes_from_database(device.get(), temperature.get(), humidity.get(), voltage.get(),
                                                      entry_start.get(), entry_stop.get())
        self.draw_chart(df)

    @staticmethod
    def draw_chart(df):
        if df.empty:
            return

        plt.rcParams["figure.figsize"] = (16, 9)

        fig, axs = plt.subplots(nrows=len(df.columns) - 1, squeeze=False, sharex=True)
        i = 0

        if 'voltage' in df:
            axs[i, 0].plot(df['time'], df['voltage'], '-r', label='Napięcie')
            axs[i, 0].grid(visible=True, axis='x')
            axs[i, 0].legend()
            axs[i, 0].set_xlabel('Czas')
            axs[i, 0].set_ylabel('Napięcie [V]')
            i += 1

        if 'humidity' in df:
            axs[i, 0].plot(df['time'], df['humidity'], '-g', label='Wilgotność')
            axs[i, 0].grid(visible=True, axis='x')
            axs[i, 0].legend()
            axs[i, 0].set_xlabel('Czas')
            axs[i, 0].set_ylabel('Wilgotność [%]')
            i += 1

        if 'temperature' in df:
            axs[i, 0].plot(df['time'], df['temperature'], label="Temperatura")
            axs[i, 0].grid(visible=True, axis='x')
            axs[i, 0].legend()
            axs[i, 0].set_xlabel('Czas')
            axs[i, 0].set_ylabel('Temperatura [C]')
            i += 1

        axs[0, 0].set_title('Data visualization')
        plt.subplots_adjust(hspace=.0)  # remove space between plots
        plt.savefig('chart.png')
        plt.show()


root = Tk()
app = MainApplication(root)
root.mainloop()
