import streamlit as st
import psutil
import pandas as pd
try:
    import gpustat
except ModuleNotFoundError:
    st.error("Please install the `gpustat` library using `pip install gpustat`.")
    st.stop()

def get_gpu_stats():
    """Fetches GPU information using gpustat, handling potential exceptions."""
    try:
        gpu_stats = gpustat.GPUStatCollection.new_query()
        return gpu_stats.gpus
    except:
        return None

def display_gpu_info(gpus):
    """Displays GPU information in a clear and formatted manner."""
    if gpus is None:
        st.warning("No GPUs found on this system.")
        return

    cols = ["Index", "Name", "Memory Used (MB)", "Memory Total (MB)"]
    df = pd.DataFrame(columns=cols)
    for gpu in gpus:
        df = df.append({
            "Index": gpu.index,
            "Name": gpu.name,
            "Memory Used (MB)": gpu.memory_used,
            "Memory Total (MB)": gpu.memory_total,
        }, ignore_index=True)

    st.table(df)

def display_system_info():
    """Displays system information, including total memory."""
    total_memory = psutil.virtual_memory().total
    total_memory_gb = total_memory / (1024 * 1024 * 1024)
    st.subheader("System Information")
    st.write(f"Total Memory Capacity: {total_memory_gb:.2f} GB")

def main():
    """Main function to organize and display information."""
    st.title("GPU and System Information Monitor")

    gpus = get_gpu_stats()
    display_gpu_info(gpus)
    display_system_info()

if __name__ == "__main__":
    main()
