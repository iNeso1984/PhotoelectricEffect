# Install required libraries: pip install streamlit matplotlib numpy pillow

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# Constants for the photoelectric effect
h = 6.626e-34  # Planck's constant (J·s)
e = 1.602e-19  # Electron charge (C)
work_function = 2.14 * e  # Work function (J)

# Frequency range (10^14 Hz to 10^15 Hz)
min_frequency = 1e14
max_frequency = 1e15

# Generate RGB color smoothly across the visible spectrum
def frequency_to_smooth_color(frequency):
    normalized_freq = 1 - (frequency - min_frequency) / (max_frequency - min_frequency)
    # Map normalized frequency to a wavelength range (400-700 nm for visible light)
    wavelength = 400 + normalized_freq * 300  # 400-700 nm spectrum range

    # Convert wavelength to RGB (simple approximation)
    if 380 <= wavelength < 440:
        r, g, b = -(wavelength - 440) / (440 - 380), 0, 1
    elif 440 <= wavelength < 490:
        r, g, b = 0, (wavelength - 440) / (490 - 440), 1
    elif 490 <= wavelength < 510:
        r, g, b = 0, 1, -(wavelength - 510) / (510 - 490)
    elif 510 <= wavelength < 580:
        r, g, b = (wavelength - 510) / (580 - 510), 1, 0
    elif 580 <= wavelength < 645:
        r, g, b = 1, -(wavelength - 645) / (645 - 580), 0
    elif 645 <= wavelength <= 780:
        r, g, b = 1, 0, 0
    else:
        r, g, b = 0, 0, 0  # Outside visible range

    # Scale RGB to 0-255
    r, g, b = [int(255 * np.clip(c, 0, 1)) for c in (r, g, b)]
    return f"#{r:02x}{g:02x}{b:02x}"

# Create a smooth rainbow spectrum image
def create_smooth_rainbow_image(width=600, height=50):
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    for i in range(width):
        frequency = min_frequency + (i / width) * (max_frequency - min_frequency)
        color = frequency_to_smooth_color(frequency)
        draw.line([(i, 0), (i, height)], fill=color)
    return img

# Title and description
st.title("Interactive Photoelectric Effect Simulation")
st.markdown("""
The **Photoelectric Effect** was discovered when scientists observed that shining light on certain metals could eject electrons. 
However, the brightness of the light wasn't the deciding factor—only light with high enough frequency (like blue or ultraviolet) could eject electrons. 
This led to the understanding that light behaves like discrete packets of energy, or photons, which was a pivotal step in the development of quantum mechanics.
""")

# Display an image of the effect (replace with desired URL)
image_url = "https://vanessawithun.com/wp-content/uploads/2024/10/example.jpg"
st.image(image_url, caption="Photoelectric Effect", use_column_width=True)

st.markdown("""
### Instructions:
- **Adjust the frequency** by moving the slider or clicking on the **rainbow spectrum**.
- **See the color change smoothly** across the visible spectrum.
- Observe how **stopping voltage** varies with frequency and is displayed next to the red dot on the graph.
""")

# Display the smooth rainbow spectrum
rainbow_img = create_smooth_rainbow_image()
st.image(rainbow_img, caption="Visible Spectrum (Hz Range)", use_column_width=True)

# Frequency slider for light frequency adjustment
frequency = st.slider(
    "Select the Frequency of Light (in Hz)",
    min_value=min_frequency,
    max_value=max_frequency,
    step=1e13,
    value=5e14
)

# Calculate stopping voltage
if frequency * h > work_function:
    stopping_voltage = (h * frequency - work_function) / e
else:
    stopping_voltage = 0

# Display the selected frequency and corresponding color
current_color = frequency_to_smooth_color(frequency)
st.write(f"**Frequency:** {frequency:.2e} Hz")
st.write(f"**Stopping Voltage:** {stopping_voltage:.2f} V")
st.markdown(
    f"<div style='background-color: {current_color}; height: 50px; width: 100%;'></div>",
    unsafe_allow_html=True,
)

# Generate data for plotting the graph
frequencies = np.linspace(min_frequency, max_frequency, 100)
voltages = np.maximum((h * frequencies - work_function) / e, 0)

# Plot the graph with a red dot and voltage label
fig, ax = plt.subplots()
ax.plot(frequencies, voltages, color='blue', linewidth=2)
ax.plot(frequency, stopping_voltage, 'ro')  # Red marker for selected frequency

# Add a voltage label next to the red dot
ax.text(
    frequency, stopping_voltage, f"{stopping_voltage:.2f} V",
    fontsize=9, ha='left', va='bottom', color='red', fontweight='bold'
)

# Set plot labels and title
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Stopping Voltage (V)")
ax.set_title("Stopping Voltage vs Frequency")
ax.grid(True)

# Display the graph
st.pyplot(fig)

# Footer with explanation
st.markdown("""
#### How This Simulation Works:
1. **Move the slider** to adjust the frequency of light.
2. Observe how **higher frequencies** (e.g., blue or violet) lead to higher stopping voltages.
3. If the frequency is **too low** (e.g., red light), no electrons are ejected, and the voltage remains **0 V**.
4. Notice the **smooth color transitions** representing the visible spectrum.
""")
