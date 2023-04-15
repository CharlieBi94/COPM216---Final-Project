import json
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import threading
import time
import paho.mqtt.client as mqtt


class TempApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Temperature Variations")

        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax1 = self.fig.add_subplot(111)
        self.dynamic_update = False

        # canvas to display the chart
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # generating random values to plot
        self.values = [random.uniform(15, 35) for i in range(10)]

        # plotting the line chart
        self.line, = self.ax1.plot(range(len(self.values)), self.values)
        self.ax1.set_ylim([0, 40])
        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("Temperature (°C)")
        self.ax1.set_title("Temperature Variations")

        # creating a frame for the button
        # self.button_frame = tk.Frame(self.root)
        # self.button_frame.pack(side=tk.TOP, fill=tk.X)
        #
        # self.go_button = tk.Button(
        #     self.button_frame,
        #     text="DYNAMIC TEMPERATURE DISPLAY",
        #     command=self.activate_dynamic_update
        # )
        #
        # self.go_button.pack(side=tk.TOP, padx=10, pady=10, anchor=tk.CENTER)

        # self.thread = None

        # setting up mqtt subscriber
        self.broker_address = "broker.emqx.io"
        self.topic = "group2/temperature"
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def update_values(self, value):
        self.values.pop(0)
        self.values.append(value)
        self.line.set_ydata(self.values)
        self.canvas.draw()

    def run(self):
        self.client.connect(self.broker_address)
        self.client.loop_start()
        self.root.mainloop()

    def on_connect(self, client, userdata, flags, rc):
        print("connected with result code " + str(rc))
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        data_dict = json.loads(msg.payload)
        temperature = data_dict['temp']
        if type(temperature) == float:
            self.update_values(temperature)
        else:
            print("Invalid temperature")
        print(temperature)


app = TempApp()
app.run()
