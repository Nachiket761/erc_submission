import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from scipy.io import wavfile
import soundfile as sf

# Load the .wav file
filename = "in1.wav"  # Replace with the path to your .wav file
sample_rate, data = wavfile.read(filename)

# Normalize the signal if necessary
if data.dtype == np.int16:  # Assuming 16-bit audio
    data = data / 32768.0
elif data.dtype == np.int32:  # Assuming 32-bit audio
    data = data / 2147483648.0

# Carrier frequency you want to use (in Hz)
new_carrier_freq = 10000 # Replace with your desired carrier frequency

# Generate a time vector for the signal
time = np.linspace(0, len(data) / sample_rate, len(data))

# Multiply the signal with the new carrier (simulate a local oscillator)
baseband_signal = data * np.cos(2 * np.pi * new_carrier_freq * time)

# Demodulation using envelope detection
analytic_signal = hilbert(baseband_signal)  # Hilbert transform
envelope = np.abs(analytic_signal)  # Extract envelope

# Scale envelope back to the original data range
envelope = envelope / np.max(envelope)  # Normalize between 0 and 1
envelope = envelope * 32767  # Convert to 16-bit integer range
envelope = envelope.astype(np.int16)  # Ensure 16-bit format

# Write the demodulated signal to a .wav file
output_filename = "demodulated_signal_with_new_carrier.wav"
wavfile.write(output_filename, sample_rate, envelope)
print(f"Demodulated signal written to {output_filename}")

# Plot signals
# plt.figure(figsize=(10, 6))
# plt.subplot(2, 1, 1)
# plt.plot(time, data, label="Original AM Signal")
# plt.title("Original AM Signal")
# plt.xlabel("Time (s)")
# plt.ylabel("Amplitude")
# plt.grid(True)

# plt.subplot(2, 1, 2)
# plt.plot(time, envelope, label="Demodulated Signal", color="orange")
# plt.title("Demodulated Signal (New Carrier)")
# plt.xlabel("Time (s)")
# plt.ylabel("Amplitude")
# plt.grid(True)

#plt.tight_layout()
#plt.show()