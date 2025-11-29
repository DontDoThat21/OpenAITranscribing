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

# Try to import pynput for global hotkeys, fallback if not available
try:
    from pynput import keyboard
    HOTKEY_AVAILABLE = True
except ImportError:
    print("⚠️  pynput not available - global hotkey functionality disabled")
    HOTKEY_AVAILABLE = False

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
SAMPLE_RATE = 16000
CHANNELS = 1
FRAME_MS = 30
VAD_AGGRESSIVENESS = 2
SILENCE_DURATION_SEC = 1.0
ONE_TIME_RECORD_DURATION_SEC = 10.0  # Maximum recording time for one-time transcription
PORCUPINE_ACCESS_KEY = "your_key"  # ← Replace w/ key
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
one_time_transcribing = False
one_time_audio_queue = queue.Queue()

# Wake-word and sleep-word detectors
porcupine = pvporcupine.create(
    access_key=PORCUPINE_ACCESS_KEY,
    keywords=[WAKE_WORD, SLEEP_WORD]
)

def transcribe_audio_buffer(buffer, message_prefix="📝 You said", check_sleep_word=False):
    """Transcribe audio buffer with temp file handling and text output."""
    global transcribing
    
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            temp_file = tmp.name
            with wave.open(tmp.name, "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(buffer)

        result = model.transcribe(temp_file)
        text = result["text"].strip()
        
        if text:
            if check_sleep_word and SLEEP_WORD.lower() in text.lower():
                print(f"{message_prefix}: {text}")
                print("💤 Sleep word detected in transcription! Stopping...")
                transcribing = False
                clear_queue_fast(audio_queue)
                return True  # Sleep word detected
            
            print(f"{message_prefix}: {text}")
            pyperclip.copy(text)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.2)
        else:
            if "one-time" in message_prefix.lower():
                print("❌ No text detected in one-time transcription")
    
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
    
    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except OSError as e:
                print(f"⚠️  Warning: Could not delete temp file {temp_file}: {e}")
    
    return False  # No sleep word detected

def reset_audio_state(buffer, silence_start_ref=None, frame_count_ref=None):
    """Reset audio processing state variables."""
    buffer.clear()
    if hasattr(reset_audio_state, '_frame_count_container'):
        reset_audio_state._frame_count_container[0] = 0
    if hasattr(reset_audio_state, '_silence_start_container'):
        reset_audio_state._silence_start_container[0] = None

def clear_queue_fast(q):
    """Fast queue clearing using collections.deque for better performance."""
    import collections
    temp_items = collections.deque()
    try:
        while True:
            temp_items.append(q.get_nowait())
    except queue.Empty:
        pass
    temp_items.clear()

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
                    clear_queue_fast(audio_queue)
                    return

def audio_callback(indata, frames, time_info, status):
    global one_time_transcribing
    if status:
        print(f"[Warning] {status}")
    pcm_data = (indata[:, 0] * 32767).astype(np.int16).tobytes()
    audio_queue.put(pcm_data)
    
    # Also put in one-time queue if one-time transcription is active
    if one_time_transcribing:
        one_time_audio_queue.put(pcm_data)

def one_time_transcribe():
    """Perform one-time transcription triggered by hotkey."""
    global one_time_transcribing
    
    if one_time_transcribing:
        return  # Already in progress
    
    print("🎤 One-time transcription started...")
    one_time_transcribing = True
    
    # Clear the one-time queue
    clear_queue_fast(one_time_audio_queue)
    
    buffer = bytearray()
    start_time = time.time()
    
    # Record for up to ONE_TIME_RECORD_DURATION_SEC seconds
    while time.time() - start_time < ONE_TIME_RECORD_DURATION_SEC:
        try:
            frame = one_time_audio_queue.get(timeout=0.1)
            buffer.extend(frame)
        except queue.Empty:
            continue
    
    one_time_transcribing = False
    
    if not buffer:
        print("❌ No audio recorded for one-time transcription")
        return
    
    # Transcribe the recorded audio
    transcribe_audio_buffer(buffer, "📝 One-time transcription")

def on_hotkey_pressed():
    """Handle the Ctrl+- hotkey press."""
    # Run one-time transcription in a separate thread to avoid blocking
    threading.Thread(target=one_time_transcribe, daemon=True).start()

def setup_global_hotkey():
    """Set up global hotkey listener for Ctrl+- (Ctrl + numpad minus)."""
    if not HOTKEY_AVAILABLE:
        print("⚠️  Global hotkey not available - pynput library not installed")
        return None
    
    try:
        # Alternative hotkey detection using pynput's hotkey functionality
        def hotkey_handler():
            on_hotkey_pressed()
        
        # Register the hotkey combination
        hotkey_listener = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+t': hotkey_handler  # Ctrl + Alt + T
        })
        
        hotkey_listener.start()
        return hotkey_listener
    except Exception as e:
        print(f"⚠️  Failed to set up global hotkey: {e}")
        return None


def record_and_transcribe():
    global transcribing
    buffer = bytearray()
    silence_start = None
    frame_count = 0

    while True:
        if not transcribing:
            # Clear any accumulated audio when not transcribing
            clear_queue_fast(audio_queue)
            buffer.clear()
            silence_start = None
            frame_count = 0
            wakeword_listener()
            # Clear queue again after wake word detection to avoid processing old audio
            clear_queue_fast(audio_queue)
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
                        transcribe_audio_buffer(buffer)
                        buffer.clear()
                        frame_count = 0
        else:
            if buffer:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > SILENCE_DURATION_SEC:
                    # Transcribe audio and check for sleep word
                    if transcribe_audio_buffer(buffer, check_sleep_word=True):
                        buffer.clear()
                        frame_count = 0
                        continue
                    
                    buffer.clear()
                    silence_start = None
                    frame_count = 0

def main():
    global transcribing
    
    print("🔊 Starting voice system with wake/sleep words...")
    print("🎤 Wake word: 'computer' (starts transcribing)")
    print("💤 Sleep word: 'terminator' (stops transcribing)")
    
    # Set up global hotkey listener
    hotkey_listener = setup_global_hotkey()
    if hotkey_listener:
        print("✅ Global hotkey: Ctrl+- (one-time transcription)")
    else:
        print("❌ Global hotkey not available")
    
    # Start with transcription off
    transcribing = False
    
    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            blocksize=int(SAMPLE_RATE * FRAME_MS / 1000),
            callback=audio_callback
        ):
            record_and_transcribe()
    except KeyboardInterrupt:
        print("\n🛑 Stopping voice system...")
    finally:
        # Clean up hotkey listener
        if hotkey_listener:
            hotkey_listener.stop()

if __name__ == "__main__":
    main()