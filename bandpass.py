import numpy as np
from scipy.io.wavfile import read, write
from scipy.signal import butter, lfilter
import os

def band_pass_filter(data, low_cutoff, high_cutoff, sample_rate):
    # Design the band-pass filter
    nyquist = 0.5 * sample_rate
    low = low_cutoff / nyquist
    high = high_cutoff / nyquist
    b, a = butter(4, [low, high], btype='band', analog=False)
    
    # Apply the filter to the data
    filtered_data = lfilter(b, a, data)
    return filtered_data

def process_wav_file(input_file, output_file, low_cutoff, high_cutoff):
    # Read the WAV file
    sample_rate, data = read(input_file)
    
    # Ensure data is mono (single channel) for processing
    if len(data.shape) > 1:
        data = data[:, 0]
    
    # Apply the band-pass filter
    filtered_data = band_pass_filter(data, low_cutoff, high_cutoff, sample_rate)
    
    # Normalize the filtered data to avoid clipping when saving
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    
    # Write the filtered data to a new WAV file
    write(output_file, sample_rate, filtered_data)
    print(f"Filtered WAV file saved as: {output_file}")

# Example usage
if __name__ == "__main__":
    # Input and output file paths
    input_file = "demodulated_signal_with_new_carrier.wav"  # Change this to your input file path
    output_file = "output_bandpass.wav"  # Change this to your desired output file name
    
    # Band-pass filter cutoff frequencies (in Hz)
    low_cutoff = 1000  # Low frequency cutoff
    high_cutoff = 5000  # High frequency cutoff
    
    # Ensure the input file exists
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
    else:
        process_wav_file(input_file, output_file, low_cutoff, high_cutoff)