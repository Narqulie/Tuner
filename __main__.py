import sounddevice as sounddevice
import numpy as numpy
import sys

# Setup of variables and constants:
rate = 44100
chunk = 11025
peak_buffer = []
average_ready = False
# This defines the buffer size for averaging readings for a smoother reading
average_buffer_size = 5

# Setting up known frequencies, assuming western traditional tuning as a base:
# Define the notes and their positions relative to A4
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
relative_positions = [-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2]  # Relative half-steps from A4 for each note in the scale

A4_frequency = 440.0
west_std = {
    note + str(octave): A4_frequency * 2 ** (((octave - 4) * 12 + position) / 12)
    for octave in range(1, 8)
    for note, position in zip(note_names, relative_positions)
}


# Function definitions:
def display_tuning_bar(difference, max_difference=50.0):
    # Display a tuning bar based on the frequency difference.
    bar_length = 51
    # Calculate the position in the bar where the color changes
    position = int((difference / max_difference) * (bar_length / 2))
    position = min(max(position, -bar_length//2), bar_length//2) + bar_length//2
    bar = [' '] * bar_length
    # Red for lower, Green for higher frequencies
    for i in range(position):
        bar[i] = '\033[91m█\033[0m'  # Red block
    for i in range(position, bar_length):
        bar[i] = '\033[92m█\033[0m'  # Green block
    print(''.join(bar))


def move_cursor_up(lines):
    for _ in range(lines):
        sys.stdout.write("\033[F")  # move the cursor up
        sys.stdout.write("\033[K")  # clear the line


def get_frequency_from_signal(signal):
    # Convert a signal to its frequency representation and find the peak.
    window = numpy.hanning(chunk)
    spectrum = numpy.fft.rfft(signal * window)
    freqs = numpy.fft.rfftfreq(len(signal), d=1/rate)
    peak_index = numpy.argmax(numpy.abs(spectrum))
    peak_frequency = freqs[peak_index]

    global peak_buffer, average_ready
    if len(peak_buffer) < average_buffer_size:
        average_ready = False
        peak_buffer.append(peak_frequency)
        # return peak_frequency
    else:
        average_frequency = sum(peak_buffer) / len(peak_buffer)
        peak_buffer = []
        average_ready = True
        return average_frequency


def find_nearest_note(frequency):
    # Find the nearest note for a given frequency and the difference to that note.
    # Calculate the differences for all notes
    differences = {note: abs(freq - frequency) for note, freq in west_std.items()}
    # Find the note with the smallest difference
    nearest_note = min(differences, key=differences.get)
    # Calculate the actual frequency difference
    exact_frequency_of_nearest_note = west_std[nearest_note]
    frequency_difference = frequency - exact_frequency_of_nearest_note
    return nearest_note, frequency_difference, exact_frequency_of_nearest_note


def callback(indata, frames, time, status):
    # This will be called for each audio chunk.
    data = numpy.frombuffer(indata, dtype=numpy.int16)
    # Find peak frequency
    frequency = get_frequency_from_signal(data)

    if not average_ready:
        return
    # Apply exponential smoothing
    nearest_note, frequency_difference, exact_frequency_of_nearest_note = find_nearest_note(frequency)
    # Display note to user
    move_cursor_up(4)
    print(f"Detected Frequency: {frequency:.2f} Hz")
    print(f"Nearest Note: {nearest_note} - {exact_frequency_of_nearest_note:.2f}, Difference: {frequency_difference:.2f}")
    display_tuning_bar(frequency_difference)


def main():
    with sounddevice.InputStream(samplerate=rate, channels=1, dtype=numpy.int16, blocksize=chunk, callback=callback):
        print("Press Ctrl+C to stop")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\nTuner stopped. Goodbye!")


if __name__ == "__main__":
    main()
