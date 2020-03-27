# ThinkGear Visualizer
Very compact NeuroSky ThinkGear (Force Trainer II, MindFlex,...) interface and raw EEG signal visualizer for Python 3

## Requirements
- Python 3.x with pySerial and Pygame

## Usage
To use the built-in EEG signal visualization tool, just adjust the serial port to your configuration, connect your EEG device and launch the script.
To use the device interface only, just copy and paste the class into your own code and use it as follows:
 <b>1. Initialize:</b> my_device = ThinkGear(port, [baudrate])
 <b>2. Fetch data:</b> my_device.fetch_data()
 <b>3. Use data:</b> my_device.data["quality"/"heartrate"/"attention"/"meditation"/"8bit_raw"/"eeg_raw"/"eeg_asic"]
        "eeg_asic" => eeg["delta"/"theta"/"low-alpha"/"high-alpha"/"low-beta"/"high-beta"/"low-gamma"/"mid-gamma"]
