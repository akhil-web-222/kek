# For Running Locally
## Creating Virtual Environment

### For Windows
```bat
cd path\to\app
python -m pip install virtualenv
python -m virtualenv venv
venv\Scripts\activate
```
**Alternative: Batch File**

*Save with .bat extension and run*
```bat
@echo off

rem 1. Navigate to the desired directory
cd path\to\app

rem 2. Check if Python is installed
if "%PYTHON%"=="" (
  echo Error: Python is not installed. Please install Python 3 from https://www.python.org/downloads/windows/
  exit /b 1
)

rem 3. Check if virtualenv is installed (using pip)
%PYTHON%\Scripts\pip --version > NUL 2>&1 (
  echo Error: virtualenv is not installed. Installing using pip...
  %PYTHON%\Scripts\pip install virtualenv
)

rem 4. Create the virtual environment named "venv"
%PYTHON%\Scripts\virtualenv venv

rem 5. Activate the virtual environment
venv\Scripts\activate

rem Verification (optional):
where python  # Should show the path to the virtual environment's Python interpreter

rem 6. Install project dependencies (using pip within the activated virtual environment)
pip install -r requirements.txt  # Replace with your specific requirements file if needed

```
### For Linux
```shell
# 1. Navigate to the desired directory where you want to create the virtual environment
cd path/to/app

# 2. Install virtualenv if it's not already present (assuming Python 3 is installed)
python3 -m ensurepip --upgrade  # Installs or upgrades pip if necessary

# 3. Create the virtual environment named "venv"
python3 -m venv venv

# 4. Activate the virtual environment
source venv/bin/activate  # For bash or similar shells

# Verification (optional):
which python  # Should show the path to the virtual environment's Python interpreter

# 5. Install project dependencies (using pip within the activated virtual environment)
pip install -r requirements.txt  # Replace with your specific requirements file if needed

```
### For macOS
```bash
# 1. Navigate to the desired directory where you want to create the virtual environment
cd path/to/app

# 2. Check if pip is installed (Python 3 on macOS usually includes pip)
python3 -m pip --version  # Output indicates pip's presence

# 3. If pip is not installed, use `homebrew` (package manager)
if [ $? -ne 0 ]; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"  # Install Homebrew (if not present)
  brew install python  # Install Python 3 (if not present)
fi

# 4. Create the virtual environment named "venv"
python3 -m venv venv

# 5. Activate the virtual environment
source venv/bin/activate  # For bash or similar shells

# Verification (optional):
which python  # Should show the path to the virtual environment's Python interpreter

# 6. Install project dependencies (using pip within the activated virtual environment)
pip install -r requirements.txt  # Replace with your specific requirements file if needed
```
## Installing Dependencies

### For Windows
```bat
python -m pip install -r requirements.txt
```
### For Linux
```shell
pip3 install -r requirements.txt
```
### For macOS
```bash
pip3 install -r requirements.txt
```
## Configuring the access token

### For Windows
```bat
notepad .env
```
Inside the `.env` file, add a line in the following format
```
HF_TOKEN = your_hugging_face_token
```
Replace `your_hugging_face_token` with your actual Hugging Face access token. You can obtain your token by creating an account and following the instructions here: [User Access Tokens](https://huggingface.co/docs/hub/en/security-tokens)

## Running the Server

```shell
streamlit run Chat_Interface.py
```

# For Running on Google Colab


Open the notebook `notebook.ipynb` in *Google Colab Pro*

Set the environment to the following variables

Run the Localtunnel and copy the public IP address (`Ex: 192.0.2.0`)
# System Requirements

| Component |	Requirement |
|---|---|
Disk Space |	16 GB
GPU Memory (VRAM) |	20 GB (FP16)

## Recommended Hardware

**GPUs:**

| Category | Model | VRAM | FP16 Performance (TensorFlops) |
|---|---|---|---|
| High-End | NVIDIA A100 40GB | 40 GB | 6144 |
| High-End | NVIDIA H100 80GB | 80 GB | Not publicly available yet |
| Consumer Grade | NVIDIA RTX 3090 | 24 GB | 35.5 | 
| Consumer Grade | NVIDIA RTX 4090 | 24 GB | Not publicly available yet (estimated higher than 3090) |
| Alternative | AMD Radeon Instinct MI31KH  | 24 GB | Not widely benchmarked for LLaMA-3 yet |

**CPUs:**

| Brand | Series | Cores | Threads | Clock Speed |
|---|---|---|---|---|
| AMD | Ryzen Threadripper 5995WX  | 16 | 32 | 4.5 GHz (boost) |
| Intel | Core i9-12900K | 16 | 24 | 5.5 GHz (boost) |

**Notes:**

* FP16 performance refers to the theoretical performance in TensorFLOPS (trillions of floating-point operations per second) using 16-bit floating-point precision.
* Consumer grade options like RTX 3090/4090 offer good value but may not be the absolute fastest.
* AMD Radeon Instinct series is a powerful alternative, but compatibility with LLaMA-3 might be evolving. 
* CPU clock speeds are listed at boost speeds.

**Additional Considerations:**

* **RAM:** While 16GB is the minimum, 32GB or more is recommended for smoother performance.
* **System Memory Bandwidth:** Look for motherboards that support DDR5 memory for faster data transfer.
-----