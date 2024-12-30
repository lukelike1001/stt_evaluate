import matplotlib.pyplot as plt

# Example WER% data for three models (replace with your actual data)
moonshine_wer = [0.05714285714285714, 0.0, 0.15151515151515152, 0.08108108108108109, 0.36666666666666664, 0.30303030303030304, 0.045454545454545456, 0.38461538461538464, 0.16666666666666666, 0.2, 0.4, 0.25]
whisper_tiny_wer = [0.11428571428571428, 0.0, 0.09090909090909091, 0.08108108108108109, 0.43333333333333335, 0.3333333333333333, 0.06818181818181818, 0.3333333333333333, 0.19444444444444445, 0.2, 0.4, 0.3333333333333333]
whisper_base_wer = [0.02857142857142857, 0.0, 0.06060606060606061, 0.08108108108108109, 0.3333333333333333, 0.48484848484848486, 0.045454545454545456, 0.3333333333333333, 0.1388888888888889, 0.15555555555555556, 0.3, 0.25]

# Convert to percentages
moonshine_wer = [100*moonshine_wer[i] for i in range(12)]
whisper_tiny_wer = [100*whisper_tiny_wer[i] for i in range(12)]
whisper_base_wer = [100*whisper_base_wer[i] for i in range(12)]

# Trial indices
trials = list(range(1, len(moonshine_wer) + 1))

# Plotting
plt.figure(figsize=(10, 6))

plt.plot(trials, moonshine_wer, marker='o', label='moonshine')
plt.plot(trials, whisper_tiny_wer, marker='s', label='whisper-tiny.en')
plt.plot(trials, whisper_base_wer, marker='^', label='whisper-base.en')

# Customization
plt.title('STT Model WER% Comparison Across Trials')
plt.xlabel('Trial')
plt.ylabel('WER%')
plt.xticks(trials)  # Ensure x-axis matches trial indices
plt.legend()
plt.grid(True)

# Show the graph
plt.show()