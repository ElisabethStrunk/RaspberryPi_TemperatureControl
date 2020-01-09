# Room Temperature Control

## Getting started

### Connecting the DS18B20 sensor to the Raspberry Pi
First, the DS18B20 needs to be connected to the Raspberry Pi.<br>
<br>
_Figure 1_ shows the pinout of the DS18B20 and _Figure 2_ shows the GPIO connector pinout of the Raspberry Pi 4 (Raspberry Pi 3 and 2 have the same pinout).<br>
<br>
<img src="readme_images/pinout_DS18B20.png" width=150><br>
_Figure 1: DS18B20 pinout. <br>(Source: [DS18B20 datasheet](data_sheets/DS18B20.pdf))_<br>
<br>
<img src="readme_images/pinout_RPi4.png" width=300><br>
_Figure 2: Raspberry Pi 4 GPIO connector pinout. <br>(Source: [Raspberry Pi datasheet](data_sheets/RPi4.pdf))_<br>
<br>
Use the 4.7k Ohm resistor to connect the DS18B20 to the Raspberry Pi as shown in _Figure 3_, establishing the connections summarized in _Table 1_.
(The resistor is neccessary so that the Raspberry Pi can be used to supply the temperature conversion current for the sensor. See [DS18B20 datasheet](data_sheets/DS18B20), page 4.)<br>

| Function |  RPi Pin No. | DS18B20 Pin No. |
| :---: | :--- | :--- |
| data  | 7 (GPIO4) | 2 |
| Vdd   | 1 | 3 |
| GND   | 6 | 1 |
_Table 1: Pin connections in our setup._<br>
<br>
<img src="readme_images/connect_DS18B20.jpg" width=450><br>
_Figure 3: Wiring setup for temperature measurement.<br>(Source: [Les Pounder: DS18B20 Temperature Sensor With Python (Raspberry Pi)](https://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/))_

## Author

**Elisabeth Strunk**<br>
<img src="readme_images/GitHub-Mark-32px.png" width=22> https://github.com/ElisabethStrunk<br>
<img src="readme_images/LI-In-Bug.png" width=22> https://www.linkedin.com/in/elisabeth-strunk/<br>
<br>

## Acknowledgments

* Huge thanks to [Les Pounder](https://bigl.es/author/les/) who authored an [article](https://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/) on how to use DS18B20 sensors with Rasperry Pi.
* Huge thanks to Scott Campbell from [Circuit Basics](http://www.circuitbasics.com/) who authored an [article](https://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/) on how to use DS18B20 sensors with Rasperry Pi.