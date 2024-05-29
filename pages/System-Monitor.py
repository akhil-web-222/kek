# import streamlit as st
# import psutil
# import pandas as pd
# try:
#     import gpustat
# except ModuleNotFoundError:
#     st.error("Please install the `gpustat` library using `pip install gpustat`.")
#     st.stop()

# def get_gpu_stats():
#     """Fetches GPU information using gpustat, handling potential exceptions."""
#     try:
#         gpu_stats = gpustat.GPUStatCollection.new_query()
#         return gpu_stats.gpus
#     except:
#         return None

# def display_gpu_info(gpus):
#     """Displays GPU information in a clear and formatted manner."""
#     if gpus is None:
#         st.warning("No GPUs found on this system.")
#         return

#     cols = ["Index", "Name", "Memory Used (MB)", "Memory Total (MB)"]
#     df = pd.DataFrame(columns=cols)
#     for gpu in gpus:
#         df = df.append({
#             "Index": gpu.index,
#             "Name": gpu.name,
#             "Memory Used (MB)": gpu.memory_used,
#             "Memory Total (MB)": gpu.memory_total,
#         }, ignore_index=True)

#     st.table(df)

# def display_system_info():
#     """Displays system information, including total memory."""
#     total_memory = psutil.virtual_memory().total
#     total_memory_gb = total_memory / (1024 * 1024 * 1024)
#     st.subheader("System Information")
#     st.write(f"Total Memory Capacity: {total_memory_gb:.2f} GB")

# def main():
#     """Main function to organize and display information."""
#     st.title("GPU and System Information Monitor")

#     gpus = get_gpu_stats()
#     display_gpu_info(gpus)
#     display_system_info()

# if __name__ == "__main__":
#     main()
# import streamlit as st
# import psutil
# import pandas as pd
# import time
# import matplotlib.pyplot as plt

# try:
#     import gpustat
# except ModuleNotFoundError:
#     st.error("Please install the `gpustat` library using `pip install gpustat`.")
#     st.stop()

# def get_cpu_stats():
#     """Fetches CPU usage."""
#     return psutil.cpu_percent()

# def get_memory_stats():
#     """Fetches memory usage in percentage."""
#     memory_usage = psutil.virtual_memory().percent
#     return memory_usage

# def get_gpu_stats():
#     """Fetches GPU information using gpustat, handling potential exceptions."""
#     try:
#         gpu_stats = gpustat.GPUStatCollection.new_query()
#         return gpu_stats.gpus
#     except:
#         return None

# def display_gpu_info(gpus):
#     """Displays GPU information in a clear and formatted manner."""
#     if gpus is None:
#         st.warning("No GPUs found on this system.")
#         return

#     cols = ["Index", "Name", "Memory Used (MB)", "Memory Total (MB)"]
#     df = pd.DataFrame(columns=cols)
#     for gpu in gpus:
#         df = df.append({
#             "Index": gpu.index,
#             "Name": gpu.name,
#             "Memory Used (MB)": gpu.memory_used,
#             "Memory Total (MB)": gpu.memory_total,
#         }, ignore_index=True)

#     st.table(df)

# def display_system_info():
#     """Displays system information, including total memory in GB."""
#     total_memory = psutil.virtual_memory().total
#     total_memory_gb = total_memory / (1024 * 1024 * 1024)
#     st.subheader("System Information")
#     st.write(f"Total Memory Capacity: {total_memory_gb:.2f} GB")

# def update_data():
#     """Updates data points for real-time monitoring."""
#     cpu_usage = get_cpu_stats()
#     memory_usage = get_memory_stats()
#     gpu_stats = get_gpu_stats()  # May be None if no GPUs

#     # Prepare data for plotting (consider appending to existing data)
#     data = {
#         "CPU Usage (%)": [cpu_usage],
#         "Memory Usage (%)": [memory_usage]
#     }
#     if gpu_stats is not None:
#         gpu_memory_usage = gpu_stats[0].memory_used  # Assuming single GPU
#         data["GPU Memory Usage (MB)"] = [gpu_memory_usage]

#     return data

# def plot_data(data):
#     """Generates real-time area charts using Matplotlib."""
#     fig, ax = plt.subplots()

#     for label, values in data.items():
#         ax.plot(values, label=label)

#     ax.set_xlabel("Time (seconds)")
#     ax.set_ylabel("Usage (%) or Memory Usage (MB)")
#     ax.set_title("Real-time System Usage")
#     ax.legend()

#     st.pyplot(fig)

# def main():
#     """Main function to organize and display information."""
#     st.title("Real-time System Usage Monitor")

#     # Initialize empty lists for data points (consider persistence)
#     data = {"CPU Usage (%)": [], "Memory Usage (%)": []}

#     update_interval = st.slider("Update Interval (seconds)", min_value=1, max_value=10, value=2)

#     chart = st.empty()  # Placeholder for the chart

#     while True:
#         new_data = update_data()
#         data.update(new_data)  # Update existing data (consider efficient update)

#         # Efficiently update chart with new data
#         chart.pyplot(plot_data(data))

#         time.sleep(update_interval)

# if __name__ == "__main__":
#     main()
#######################################################
# import streamlit as st
# import psutil
# import pandas as pd
# import time

# try:
#     import gpustat
# except ModuleNotFoundError:
#     st.error("Please install the `gpustat` library using `pip install gpustat`.")
#     st.stop()

# def get_cpu_stats():
#     """Fetches CPU usage."""
#     return psutil.cpu_percent()

# def get_memory_stats():
#     """Fetches memory usage in percentage."""
#     memory_usage = psutil.virtual_memory().percent
#     return memory_usage

# def get_gpu_stats():
#     """Fetches GPU information using gpustat, handling potential exceptions."""
#     try:
#         gpu_stats = gpustat.GPUStatCollection.new_query()
#         return gpu_stats.gpus
#     except:
#         return None

# def display_gpu_info(gpus):
#     """Displays GPU information in a clear and formatted manner."""
#     if gpus is None:
#         st.warning("No GPUs found on this system.")
#         return

#     cols = ["Index", "Name", "Memory Used (MB)", "Memory Total (MB)"]
#     df = pd.DataFrame(columns=cols)
#     for gpu in gpus:
#         df = df.append({
#             "Index": gpu.index,
#             "Name": gpu.name,
#             "Memory Used (MB)": gpu.memory_used,
#             "Memory Total (MB)": gpu.memory_total,
#         }, ignore_index=True)

#     st.table(df)

# def display_system_info():
#     """Displays system information, including total memory in GB."""
#     total_memory = psutil.virtual_memory().total
#     total_memory_gb = total_memory / (1024 * 1024 * 1024)
#     st.subheader("System Information")
#     st.write(f"Total Memory Capacity: {total_memory_gb:.2f} GB")

# def update_data():
#     """Updates data points for real-time monitoring."""
#     cpu_usage = get_cpu_stats()
#     memory_usage = get_memory_stats()
#     gpu_stats = get_gpu_stats()  # May be None if no GPUs

#     # Prepare data for plotting
#     data = pd.DataFrame({
#         "Time (s)": [time.time()],  # Add timestamp for x-axis
#         "CPU Usage (%)": [cpu_usage],
#         "Memory Usage (%)": [memory_usage]
#     })
#     print(data)
#     if gpu_stats is not None:
#         gpu_memory_usage = gpu_stats[0].memory_used  # Assuming single GPU
#         data["GPU Memory Usage (MB)"] = [gpu_memory_usage]

#     return data

# def main():
#     """Main function to organize and display information."""
#     st.title("Real-time System Usage Monitor")

#     # Initialize empty DataFrame for data (consider persistence)
#     data = pd.DataFrame(columns=["Time (s)", "CPU Usage (%)", "Memory Usage (%)"])

#     update_interval = st.slider("Update Interval (seconds)", min_value=1, max_value=10, value=2)

#     chart = st.empty()  # Placeholder for the chart

#     while True:
#         new_data = update_data()
#         data = pd.concat([data, new_data], ignore_index=True)  # Efficiently append data

#         # Update chart with new data
#         chart.area_chart(data, x="Time (s)")

#         time.sleep(update_interval)

# if __name__ == "__main__":
#     main()
#############################################################
import streamlit as st
import psutil
import pandas as pd
import time

try:
  import gpustat
except ModuleNotFoundError:
  st.error("Please install the `gpustat` library using `pip install gpustat`.")
  st.stop()

def get_cpu_stats():
  """Fetches CPU usage."""
  return psutil.cpu_percent()

def get_memory_stats():
  """Fetches memory usage in percentage."""
  memory_usage = psutil.virtual_memory().percent
  return memory_usage

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
  """Displays system information, including total memory in GB."""
  total_memory = psutil.virtual_memory().total
  total_memory_gb = total_memory / (1024 * 1024 * 1024)
  st.subheader("System Information")
  st.write(f"Total Memory Capacity: {total_memory_gb:.2f} GB")

def update_data(data, max_data_points):
  """Updates data points for real-time monitoring and keeps a limited history."""
  cpu_usage = get_cpu_stats()
  memory_usage = get_memory_stats()
  gpu_stats = get_gpu_stats()  # May be None if no GPUs

  new_data = pd.DataFrame({
    "Time (s)": [time.time()],  # Add timestamp for x-axis
    "CPU Usage (%)": [cpu_usage],
    "Memory Usage (%)": [memory_usage]
  })

  if gpu_stats is not None:
    gpu_memory_usage = gpu_stats[0].memory_used  # Assuming single GPU
    new_data["GPU Memory Usage (MB)"] = [gpu_memory_usage]

  # Efficiently append new data and keep only the last `max_data_points` entries
  data = pd.concat([data, new_data], ignore_index=True)
  return data.tail(max_data_points)

def main():
  """Main function to organize and display information."""
  st.title("Real-time System Usage Monitor")

  # Initialize empty DataFrame for data
  update_interval = st.slider("Update Interval (seconds)", min_value=1, max_value=10, value=2)
  data = pd.DataFrame(columns=["Time (s)", "CPU Usage (%)", "Memory Usage (%)"])
  max_data_points = st.slider("Max Data Points in Chart", min_value=10, max_value=100, value=50)
  
  chart = st.empty()  # Placeholder for the chart

  while True:
    new_data = update_data(data.copy(), max_data_points)  # Avoid modifying original data
    data = new_data

    # Update chart with new data
    chart.area_chart(data, x="Time (s)")

    time.sleep(update_interval)

if __name__ == "__main__":
  main()
