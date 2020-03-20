# ThinkGear Visualizer
Very compact NeuroSky ThinkGear (Force Trainer II, MindFlex,...) interface and raw EEG signal visualizer for Python 3

## Requirements
- Python 3.x with pySerial and Pygame

## Usage
To use the built-in EEG signal visualization tool, just adjust the serial port to your configuration, connect your EEG device and launch the script.
To use the device interface only, just copy and paste the class into your own code and use it as follows:<br>
&nbsp;**1. Initialize:** my_device = ThinkGear(port, [baudrate])<br>
&nbsp;**2. Fetch data:** my_device.fetch_data()<br>
&nbsp;**3. Use data:** my_device.data["quality"/"heartrate"/"attention"/"meditation"/"8bit_raw"/"eeg_raw"/"eeg"]<br>
&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;"eeg" => eeg["delta"/"theta"/"low-alpha"/"high-alpha"/"low-beta"/"high-beta"/"low-gamma"/"mid-gamma"]
