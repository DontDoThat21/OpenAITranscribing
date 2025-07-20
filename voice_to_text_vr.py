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
PORCUPINE_ACCESS_KEY = ""  # ← Replace w/ key
WAKE_WORD = "computer"
SLEEP_WORD = "terminator"  # Using available keyword instead of "twizzlers"
# Storage optimization settings
MAX_BUFFER_SIZE_MB = 50  # Maximum audio buffer size in MB
BUFFER_CHECK_INTERVAL = 100  # Check buffer size every N frames
# ─────────────────────────────────────────────────────────────────────────────

# Load Whisper model once
model = whisper.load_model("base")

# VAD instance
vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)

# Queue to pass audio frames
audio_queue = queue.Queue()

# Global state for transcription mode
transcribing = False

# Wake-word and sleep-word detectors
porcupine = pvporcupine.create(
    access_key=PORCUPINE_ACCESS_KEY,
    keywords=[WAKE_WORD, SLEEP_WORD]
)

def wakeword_listener():
    """Wait for the wake word to begin or sleep word to stop transcription."""
    global transcribing
    
    if not transcribing:
        print("🎤 Say 'computer' to begin transcribing...")
    
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
            
            if result == 0:  # Wake word detected
                if not transcribing:
                    transcribing = True
                    print("✅ Wake word detected! Now transcribing...")
                    return
            elif result == 1:  # Sleep word detected
                if transcribing:
                    transcribing = False
                    print("💤 Sleep word detected! Stopping transcription...")
                    # Clear audio queue when sleep word is detected via wake word detection
                    try:
                        while True:
                            audio_queue.get_nowait()
                    except queue.Empty:
                        pass
                    return

def audio_callback(indata, frames, time_info, status):
    if status:
        print(f"[Warning] {status}")
    pcm_data = (indata[:, 0] * 32767).astype(np.int16).tobytes()
    audio_queue.put(pcm_data)

def record_and_transcribe():
    global transcribing
    buffer = bytearray()
    silence_start = None
    frame_count = 0

    while True:
        if not transcribing:
            # Clear any accumulated audio when not transcribing
            try:
                while True:
                    audio_queue.get_nowait()
            except queue.Empty:
                pass
            buffer.clear()
            silence_start = None
            frame_count = 0
            wakeword_listener()
            # Clear queue again after wake word detection to avoid processing old audio
            try:
                while True:
                    audio_queue.get_nowait()
            except queue.Empty:
                pass
            continue

        try:
            frame = audio_queue.get(timeout=0.1)
        except queue.Empty:
            continue

        is_speech = vad.is_speech(frame, SAMPLE_RATE)

        if is_speech:
            buffer.extend(frame)
            silence_start = None
            
            # Check buffer size periodically to prevent excessive memory usage
            frame_count += 1
            if frame_count % BUFFER_CHECK_INTERVAL == 0:
                buffer_size_mb = len(buffer) / (1024 * 1024)
                if buffer_size_mb > MAX_BUFFER_SIZE_MB:
                    print(f"⚠️  Buffer size ({buffer_size_mb:.1f}MB) exceeded limit. Processing current audio...")
                    # Force processing of current buffer to free memory
                    if buffer:
                        # Save audio to temporary file with proper cleanup
                        temp_file = None
                        try:
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                                temp_file = tmp.name
                                wf = wave.open(tmp.name, "wb")
                                wf.setnchannels(CHANNELS)
                                wf.setsampwidth(2)
                                wf.setframerate(SAMPLE_RATE)
                                wf.writeframes(buffer)
                                wf.close()

                            # Transcribe audio
                            result = model.transcribe(temp_file)
                            text = result["text"].strip()
                            
                            if text:
                                print(f"📝 You said: {text}")
                                pyperclip.copy(text)
                                pyautogui.hotkey("ctrl", "v")
                                time.sleep(0.2)
                        
                        except Exception as e:
                            print(f"❌ Error during transcription: {e}")
                        
                        finally:
                            # Ensure temp file is always cleaned up
                            if temp_file and os.path.exists(temp_file):
                                try:
                                    os.unlink(temp_file)
                                except OSError as e:
                                    print(f"⚠️  Warning: Could not delete temp file {temp_file}: {e}")
                        
                        buffer.clear()
                        frame_count = 0
        else:
            if buffer:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > SILENCE_DURATION_SEC:
                    # Save audio to temporary file with proper cleanup
                    temp_file = None
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                            temp_file = tmp.name
                            wf = wave.open(tmp.name, "wb")
                            wf.setnchannels(CHANNELS)
                            wf.setsampwidth(2)
                            wf.setframerate(SAMPLE_RATE)
                            wf.writeframes(buffer)
                            wf.close()

                        # Transcribe audio
                        result = model.transcribe(temp_file)
                        text = result["text"].strip()
                        
                        if text:
                            # Check if the transcribed text contains the sleep word
                            if SLEEP_WORD.lower() in text.lower():
                                print(f"📝 You said: {text}")
                                print("💤 Sleep word detected in transcription! Stopping...")
                                transcribing = False
                                # Clear the audio queue immediately when sleep word is detected
                                try:
                                    while True:
                                        audio_queue.get_nowait()
                                except queue.Empty:
                                    pass
                                buffer.clear()
                                frame_count = 0
                                continue
                            
                            print(f"📝 You said: {text}")
                            pyperclip.copy(text)
                            pyautogui.hotkey("ctrl", "v")
                            time.sleep(0.2)
                    
                    except Exception as e:
                        print(f"❌ Error during transcription: {e}")
                    
                    finally:
                        # Ensure temp file is always cleaned up
                        if temp_file and os.path.exists(temp_file):
                            try:
                                os.unlink(temp_file)
                            except OSError as e:
                                print(f"⚠️  Warning: Could not delete temp file {temp_file}: {e}")
                    
                    buffer.clear()
                    silence_start = None
                    frame_count = 0

def main():
    global transcribing
    
    print("🔊 Starting voice system with wake/sleep words...")
    print("🎤 Wake word: 'computer' (starts transcribing)")
    print("💤 Sleep word: 'terminator' (stops transcribing)")
    
    # Start with transcription off
    transcribing = False
    
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        blocksize=int(SAMPLE_RATE * FRAME_MS / 1000),
        callback=audio_callback
    ):
        record_and_transcribe()

if __name__ == "__main__":
    main()