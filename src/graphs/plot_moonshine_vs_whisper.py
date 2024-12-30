import matplotlib.pyplot as plt

# Example WER% data for three models (replace with your actual data)
whisper_base_error = [0.0286, 0.0, 0.0606, 0.0811, 0.3333, 0.4848, 0.0455, 0.3333, 0.1389, 0.1556, 0.3, 0.25]
whisper_tiny_error = [0.1143, 0.0, 0.0909, 0.0811, 0.4333, 0.3333, 0.0682, 0.3333, 0.1944, 0.2, 0.4, 0.3333]
moonshine_error = [0.0571, 0.0, 0.1515, 0.0811, 0.3667, 0.303, 0.0455, 0.3846, 0.1667, 0.2, 0.4, 0.25]

# Convert to percentages
whisper_base_wer = [100*whisper_base_error[i] for i in range(12)]
whisper_tiny_wer = [100*whisper_tiny_error[i] for i in range(12)]
moonshine_wer = [100*moonshine_error[i] for i in range(12)]

# Trial indices
trials = list(range(1, len(moonshine_wer) + 1))

# Plotting
plt.figure(figsize=(10, 6))

plt.plot(trials, whisper_base_wer, marker='^', label='whisper-base.en')
plt.plot(trials, whisper_tiny_wer, marker='s', label='whisper-tiny.en')
plt.plot(trials, moonshine_wer, marker='o', label='moonshine')

# Customization
plt.title('STT Model WER% Comparison Across Trials')
plt.xlabel('Trial')
plt.ylabel('WER%')
plt.xticks(trials)  # Ensure x-axis matches trial indices
plt.legend()
plt.grid(True)

# Show the graph
plt.show()