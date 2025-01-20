import streamlit as st
import matplotlib.pyplot as plt
import random
import numpy as np

# Mock-up maintenance insights generation
EXPLANATIONS = {
    "Pump": "The pump's health indicator reflects gradual wear initially, followed by accelerated degradation. This trend is represented in the graph, where the health remains stable for the first third of the timeline before dropping sharply. Regular inspection is critical to ensure optimal performance and prevent failures.",
    "Bearing": "The bearing shows a steady decay in health with increasing vibration toward the end. The graph depicts an initial plateau in performance, followed by a steep decline, signaling the need for lubrication or replacement during the later stages.",
    "Belts": "The belts experience minimal wear at the start but degrade rapidly after extended use. The plotted data highlights early stability, with a sudden drop in health due to tension or misalignment, emphasizing timely adjustment or replacement.",
    "Motor": "The motor's health trend indicates stable operation initially, with a rapid decline due to overheating or electrical faults. In the graph, this is shown as a flat initial phase that transitions into a steep drop, underscoring the importance of thermal management.",
    "Compressor": "The compressor demonstrates a slow decline early on, followed by a sharp drop. This pattern, visible in the graph, highlights potential issues with pressure or seals, necessitating proactive maintenance before the sharp degradation phase.",
    "Valve": "The valve maintains health initially but deteriorates quickly later, often due to corrosion or mechanical fatigue. The graph illustrates a plateau in the beginning, transitioning to a rapid decline, reflecting the need for regular checks to avoid failures."
}

def generate_maintenance_insights(part):
    # Generate decaying maintenance graph data with multiple lines and noise
    time = np.linspace(0, 350, 100)  # Mock time scale
    fig, ax = plt.subplots()
    decay_rate = random.uniform(2, 5)  # Random decay rate for each line

    for i in range(5):  # Generate 5 curves with different end points
        initial_health = 1
        rul = random.randint(250, 350)  # Random RUL between 250 to 350
        noise = np.random.normal(0, 0.02, size=time.shape)  # Add minor noise

        # Create a curve that stays flat initially, then drops to 0 at the RUL point
        health = np.piecewise(
            time,
            [time <= rul, time > rul],
            [lambda t: initial_health * (1 - (t / rul) ** decay_rate), 0]
        ) + noise
        health = np.clip(health, 0, 1)  # Ensure health stays within [0, 1]
        time_clip = np.clip(time, 0, rul)
        ax.plot(time_clip, health, label=f'Curve {i+1} (RUL={rul})')

    # Add a fitted line (black, dotted, not identical to any drawn lines)
    sampled_time = np.linspace(0, 350, 10)
    sampled_rul = random.randint(280, 320)
    sampled_time_clip = np.clip(sampled_time, 0, sampled_rul)
    sampled_health = np.clip(1 - (sampled_time / sampled_rul) ** decay_rate, 0, 1)
    ax.plot(sampled_time_clip, sampled_health, '--', color='black', label='Fitted Line')

    # Highlight 3 random points on the fitted line within the first 1/3 of the sampled RUL
    max_index = len(sampled_time_clip) // 3
    random_indices = random.sample(range(max_index), 3)
    for idx in random_indices:
        ax.plot(sampled_time_clip[idx], sampled_health[idx], '*', color='black')

    ax.set_title(f'Training Data for {part}')
    ax.set_xlabel('Time')
    ax.set_ylabel('Health Indicator')
    ax.legend()

    # Save graph as an image
    fig_path = f"{part}_maintenance_trend.png"
    fig.savefig(fig_path)
    plt.close(fig)

    # Randomized explanation for the selected part
    explanation = EXPLANATIONS.get(part, "No explanation available for this part.")

    return fig_path, explanation

# Main Tabs
st.title("Machine Maintenance Application")

# Create tabs
tab1, tab2 = st.tabs(["Maintenance Insights", "RUL Models"])

with tab1:
    st.header("Machine Maintenance Insights")
    
    # Create two columns
    col1, col2 = st.columns(2)

    # Column 1: Show machine image
    with col1:
        st.image("machine-drawing.svg", caption="Machine Diagram", use_container_width=True)

    # Column 2: Radial list to select machine parts
    with col2:
        # Radial list for selecting a single part
        parts = ["Pump", "Bearing", "Belts", "Motor", "Compressor", "Valve"]
        selected_part = st.radio("Select a Machine Part", parts, key="selected_part")
        uploaded_file = st.file_uploader(f"Upload Sensor Data for {selected_part}", type=["csv", "txt"], key=f"file_{selected_part}")
        if uploaded_file:
            st.write(f"Uploaded File for {selected_part}: {uploaded_file.name}")
    
        # Display information for the selected part
    if selected_part:
        st.subheader(f"Insights for {selected_part}")
    
        # Generate and display maintenance insights
        fig_path, explanation = generate_maintenance_insights(selected_part)
        st.image(fig_path, caption=f"Generated Maintenance Trend for {selected_part}", use_container_width=True)
        st.write(explanation)

with tab2:
    st.header("RUL Models for Machine Parts")

    st.write("Select a machine part and corresponding sensor type to estimate Remaining Useful Life (RUL):")


    # Create two columns
    col1, col2 = st.columns(2)

    # Column 1: Dropdown hierarchy for machine part and sensor type
    with col1:
        # Dropdown hierarchy for machine part and sensor type
        selected_part = st.selectbox("Select Machine Part", parts, key="dropdown_part")
        sensors = ["Temperature", "Acceleration", "Vibration", "Fluid Speed", "Pressure", "Current"]
        selected_sensor = st.selectbox("Select Sensor Type", sensors, key="dropdown_sensor")

    # Column 2: Radial list to select machine parts
    with col2:
        selected_model = st.radio(
            "Select a machine learning model:",
            ["Linear Regression", "Random Forest", "Neural Network", "Support Vector Machine"],
            key="model_selection"
        )

    st.write(f"You selected {selected_part} with {selected_sensor} sensor, modeled using {selected_model}")

    # Mock-up performance chart
    if selected_model:
        st.write(f"Performance of {selected_model} for {selected_part} with {selected_sensor} sensor:")

        # Generate a performance chart
        metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]
        values = [random.uniform(0.7, 1.0) for _ in metrics]
        fig, ax = plt.subplots()
        ax.bar(metrics, values, color='skyblue')
        ax.set_ylim(0, 1)
        ax.set_ylabel("Score")
        ax.set_title("Model Performance Metrics")

        st.pyplot(fig)
