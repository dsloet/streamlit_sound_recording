import os
from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave

from datetime import datetime

from settings import (
    SAMPLE_RATE,
    MAX_INPUT_CHANNELS,
    CHUNK_SIZE,
    THRESHOLD,
    RECORDING_DIR,
)

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Recorder:
    def __init__(self) -> None:
        self.title = "test"
        self.format = pyaudio.paInt16
        self.rate = SAMPLE_RATE  # 22050
        self.chunk_size = CHUNK_SIZE  # 1024
        self.threshold = THRESHOLD  # 500
        self.channels = MAX_INPUT_CHANNELS  # 1
        self.fileloc = RECORDING_DIR

    def _is_silent(self, snd_data):
        "Returns 'True' if below the 'silent' threshold"
        print(max(snd_data))
        return max(snd_data) < self.threshold

    @staticmethod
    def _normalize(snd_data):
        "Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM) / max(abs(i) for i in snd_data)

        r = array("h")
        for i in snd_data:
            r.append(int(i * times))
        return r

    def trim(self, snd_data):
        "Trim the blank spots at the start and end"

        def _trim(snd_data):
            snd_started = False
            r = array("h")

            for i in snd_data:
                if not snd_started and abs(i) > self.threshold:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    def add_silence(self, snd_data, seconds):
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        silence = [0] * int(seconds * self.rate)
        r = array("h", silence)
        r.extend(snd_data)
        r.extend(silence)
        return r

    def record(self) -> None:
        """
         Record a word or words from the microphone and
        return the data as an array of signed shorts.

        Normalizes the audio, trims silence from the
        start and end, and pads with 0.5 seconds of
        blank sound to make sure VLC et al can play
        it without getting chopped off.

        """
        logger.info("start recording")
        p = pyaudio.PyAudio()
        stream = p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            output=True,
            frames_per_buffer=self.chunk_size,
        )

        num_silent = 0
        snd_started = False

        r = array("h")

        while True:
            snd_data = array("h", stream.read(self.chunk_size))
            if byteorder == "big":
                snd_data.byteswap()
            r.extend(snd_data)

            silent = self._is_silent(snd_data)

            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True

            if snd_started and num_silent > 50:
                break

        sample_width = p.get_sample_size(self.format)
        stream.stop_stream()
        stream.close()
        p.terminate()

        r = self._normalize(r)
        r = self.trim(r)
        r = self.add_silence(r, 0.5)

        return sample_width, r

    def record_to_file(self, counter) -> None:
        sample_width, data = self.record()
        data = pack("<" + ("h" * len(data)), *data)

        # current date and time
        now = datetime.now().strftime("%d-%m-%Y")
        name = f"{now}_DS_test_{counter}.wav"
        filename = os.path.join(self.fileloc, name)
        logger.info(filename)
        wf = wave.open(filename, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.rate)
        wf.writeframes(data)
        wf.close
        return name
