import os

# The Root Directory of the project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT_DIR, "output/")
RECORDING_DIR = os.path.join(OUT_DIR, "recording")

DURATION = 3
DEFAULT_SAMPLE_RATE = 22050
MAX_INPUT_CHANNELS = 1
WAVE_OUTPUT_FILE = os.path.join(RECORDING_DIR, "recorded.wav")
INPUT_DEVICE = 0
CHUNK_SIZE = 1024
