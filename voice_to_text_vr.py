import os
import queue
import threading
import webrtcvad
import whisper
import sounddevice as sd
import numpy as np
import pyperclip
import pyautogui
import time
import tempfile
import wave
import pvporcupine

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
SAMPLE_RATE = 16000
CHANNELS = 1
FRAME_MS = 30
VAD_AGGRESSIVENESS = 2
SILENCE_DURATION_SEC = 1.0
PORCUPINE_ACCESS_KEY =                                                              ""  # ← Replace with your actual key                                         //
WAKE_WORD = "computer"  # Can be: "jarvis", "terminator", etc.
# ─────────────────────────────────────────────────────────────────────────────

# Load Whisper model once
model = whisper.load_model("base")

# VAD instance
vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)

# Queue to pass audio frames
audio_queue = queue.Queue()

# Wake-word detector
porcupine = pvporcupine.create(
    access_key=PORCUPINE_ACCESS_KEY,
    keywords=[WAKE_WORD]
)

def wakeword_listener():
    """Wait for the wake word before allowing transcription."""
    print("🎤 Say the wake word to begin (e.g. 'Hey Computer')...")

    with sd.InputStream(
        samplerate=porcupine.sample_rate,
        blocksize=porcupine.frame_length,
        dtype='int16',
        channels=1,
        callback=None
    ) as stream:
        while True:
            pcm = stream.read(porcupine.frame_length)[0].flatten()
            result = porcupine.process(pcm)
            if result >= 0:
                print("✅ Wake word detected!")
                break

def audio_callback(indata, frames, time_info, status):
    if status:
        print(f"[Warning] {status}")
    pcm_data = (indata[:, 0] * 32767).astype(np.int16).tobytes()
    audio_queue.put(pcm_data)

def record_and_transcribe():
    buffer = bytearray()
    silence_start = None

    while True:
        frame = audio_queue.get()
        is_speech = vad.is_speech(frame, SAMPLE_RATE)

        if is_speech:
            buffer.extend(frame)
            silence_start = None
        else:
            if buffer:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > SILENCE_DURATION_SEC:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                        wf = wave.open(tmp.name, "wb")
                        wf.setnchannels(CHANNELS)
                        wf.setsampwidth(2)
                        wf.setframerate(SAMPLE_RATE)
                        wf.writeframes(buffer)
                        wf.close()

                    result = model.transcribe(tmp.name)
                    os.unlink(tmp.name)
                    text = result["text"].strip()
                    buffer.clear()
                    silence_start = None

                    if text:
                        print(f"📝 You said: {text}")
                        pyperclip.copy(text)
                        pyautogui.hotkey("ctrl", "v")
                        time.sleep(0.2)
                    
                    # Listen for wake word again after each transcription
                    print("👂 Awaiting new wake word…")
                    wakeword_listener()

def main():
    print("🔊 Starting voice system with wake word...")
    wakeword_listener()

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        blocksize=int(SAMPLE_RATE * FRAME_MS / 1000),
        callback=audio_callback
    ):
        record_and_transcribe()

if __name__ == "__main__":
    main()
