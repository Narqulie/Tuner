# Real-time Audio Tuner

A simple real-time tuner that detects the pitch of an audio signal and matches it to the closest musical note.

## Features:
- Uses FFT (Fast Fourier Transform) to detect the peak frequency of an audio signal in real-time.
- Displays a tuning bar, with red indicating lower frequencies and green for higher frequencies.
- Continuously averages detected frequencies for smoother and more stable readings.
- Matches the detected frequency with the nearest musical note based on Western traditional tuning.

## Installation:
1. Clone this repository:
```bash
git clone https://github.com/Narqulie/Tuner.git
```
2. Install the required packages:
```bash
pip install sounddevice numpy
```
3. Run the script:
```bash
python AudioTuner.py
```

## Usage:
After running the script, play a musical note near your computer's microphone. The tuner will display the detected frequency, the closest musical note, and the difference in Hertz.

The tuning bar will provide a visual indication, turning red if you're below the correct pitch and green if you're above it.

To stop the tuner, press `Ctrl+C`.

## Dependencies:
- `sounddevice`: For capturing audio input in real-time.
- `numpy`: For numerical operations and FFT.

## Contributing:
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License:
[MIT](https://choosealicense.com/licenses/mit/)
