import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Scale, Label, HORIZONTAL

def update_fft(val):
    global data, sample_rate
    time_instant = slider.get()  # Get the current slider value
    num_samples = 10000  # Number of samples for FFT
    start_sample = int(time_instant * sample_rate)
    end_sample = start_sample + num_samples

    # Check if the selected range is valid
    if end_sample > len(data) or start_sample < 0:
        print("Selected time exceeds the file length!")
        return

    # Extract the samples and perform FFT
    segment = data[start_sample:end_sample]
    fft_result = np.fft.fft(segment)
    freq_axis = np.fft.fftfreq(num_samples, d=1/sample_rate)
    magnitude = np.abs(fft_result)

    # Update the plot
    plt.cla()
    plt.plot(freq_axis[:num_samples//2], magnitude[:num_samples//2])  # Plot only positive frequencies
    plt.title("FFT of Selected Segment")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.draw()

# Load WAV file
root = Tk()
root.withdraw()  # Hide the main Tkinter window
file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")], title="Select a WAV file")

if not file_path:
    print("No file selected.")
    exit()

sample_rate, data = wav.read(file_path)

# Ensure data is single channel (mono)
if len(data.shape) > 1:
    data = data[:, 0]

# Create GUI
root = Tk()
root.title("FFT of WAV File Segment")
slider = Scale(root, from_=0, to=len(data)/sample_rate, resolution=0.01, length=400, orient=HORIZONTAL, command=update_fft)
slider.pack()
label = Label(root, text="Use the slider to select a time instant")
label.pack()

# Plot initialization
plt.ion()
plt.figure()
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.show()

root.mainloop()