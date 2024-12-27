import matplotlib.pyplot as plt

# Example WER% data for three models (replace with your actual data)
whisper_base_wer = [0.0455, 0.3333, 0.1389, 0.1556, 0.3, 0.25, 0.1899]
whisper_asr_wer = [0.0909, 0.0417, 0.1622, 0.3182, 0.00, 0.0769, 0.2065]

# Convert to percentages
whisper_base_wer = [100*whisper_base_wer[i] for i in range(7)]
whisper_asr_wer = [100*whisper_asr_wer[i] for i in range(7)]

# Trial indices
trials = list(range(1, len(whisper_base_wer) + 1))

# Plotting
plt.figure(figsize=(10, 6))

plt.plot(trials, whisper_base_wer, marker='o', label='whisper-base.en')
plt.plot(trials, whisper_asr_wer, marker='^', label='whisper-asr')

# Customization
plt.title('STT Model WER% Comparison Across Trials')
plt.xlabel('Trial')
plt.ylabel('WER%')
plt.xticks(trials)  # Ensure x-axis matches trial indices
plt.legend()
plt.grid(True)

# Show the graph
plt.show()