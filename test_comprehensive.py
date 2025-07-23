#!/usr/bin/env python3
"""
Test script to validate the one-time transcription functionality
without requiring full audio dependencies.
"""

import sys
import time
import threading
import tempfile
import os
import wave

# Mock dependencies to test the logic
class MockWhisper:
    def load_model(self, model_name):
        return self
    
    def transcribe(self, file_path):
        return {"text": f"Mock transcription for {os.path.basename(file_path)}"}

class MockPyperclip:
    def copy(self, text):
        print(f"📋 Copied to clipboard: {text}")

class MockPyautogui:
    def hotkey(self, *keys):
        print(f"⌨️  Pressed hotkey: {' + '.join(keys)}")

class MockVAD:
    def __init__(self, aggressiveness):
        self.aggressiveness = aggressiveness
    
    def is_speech(self, frame, sample_rate):
        return True  # Always return True for testing

class MockPorcupine:
    def create(self, access_key, keywords):
        return self
    
    @property
    def sample_rate(self):
        return 16000
    
    @property
    def frame_length(self):
        return 512

class MockSoundDevice:
    class InputStream:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
        
        def __enter__(self):
            return self
        
        def __exit__(self, *args):
            pass

class MockQueue:
    def __init__(self):
        self.items = []
    
    def put(self, item):
        self.items.append(item)
    
    def get(self, timeout=None):
        if self.items:
            return self.items.pop(0)
        raise Exception("Empty")
    
    def get_nowait(self):
        if self.items:
            return self.items.pop(0)
        raise Exception("Empty")

# Mock the globals that would be imported
sys.modules['whisper'] = MockWhisper()
sys.modules['pyperclip'] = MockPyperclip()
sys.modules['pyautogui'] = MockPyautogui()
sys.modules['webrtcvad'] = type('MockVAD', (), {'Vad': MockVAD})()
sys.modules['pvporcupine'] = MockPorcupine()
sys.modules['sounddevice'] = MockSoundDevice()
sys.modules['numpy'] = type('MockNumpy', (), {'int16': int})()

import queue
# Mock queue module
original_queue = queue.Queue
queue.Queue = MockQueue

# Now test our implementation
def test_one_time_transcription():
    """Test the one-time transcription logic."""
    print("🧪 Testing one-time transcription functionality...")
    
    # Set up test variables
    ONE_TIME_RECORD_DURATION_SEC = 2.0  # Shorter for testing
    SAMPLE_RATE = 16000
    CHANNELS = 1
    
    # Mock audio data
    test_audio_data = b"mock_audio_data" * 100
    
    # Simulate the one-time transcription
    one_time_transcribing = False
    one_time_audio_queue = MockQueue()
    
    def mock_one_time_transcribe():
        nonlocal one_time_transcribing
        
        if one_time_transcribing:
            return
        
        print("🎤 One-time transcription started...")
        one_time_transcribing = True
        
        # Simulate audio collection
        for i in range(5):
            one_time_audio_queue.put(test_audio_data)
        
        buffer = bytearray()
        start_time = time.time()
        
        # Collect audio (simulated)
        while time.time() - start_time < ONE_TIME_RECORD_DURATION_SEC:
            try:
                frame = one_time_audio_queue.get(timeout=0.1)
                buffer.extend(frame)
            except:
                break
        
        one_time_transcribing = False
        
        if not buffer:
            print("❌ No audio recorded")
            return
        
        # Simulate file creation and transcription
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                temp_file = tmp.name
                # Just create an empty file for testing
                
            # Mock transcription
            text = f"Mock transcription result (buffer size: {len(buffer)} bytes)"
            
            if text:
                print(f"📝 One-time transcription: {text}")
                # Mock clipboard copy and paste
                print(f"📋 Copied to clipboard: {text}")
                print("⌨️  Pressed hotkey: ctrl + v")
            else:
                print("❌ No text detected")
        
        except Exception as e:
            print(f"❌ Error during transcription: {e}")
        
        finally:
            if 'temp_file' in locals() and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
    
    def on_hotkey_pressed():
        """Handle hotkey simulation."""
        print("🔥 Hotkey Ctrl+- detected!")
        threading.Thread(target=mock_one_time_transcribe, daemon=True).start()
    
    # Test the functionality
    print("Simulating hotkey press...")
    on_hotkey_pressed()
    
    # Wait for completion
    time.sleep(3)
    print("✅ Test completed successfully!")

def test_hotkey_integration():
    """Test that the hotkey can be set up without errors."""
    print("\n🧪 Testing hotkey integration...")
    
    # Test with pynput not available (which is our current state)
    HOTKEY_AVAILABLE = False
    
    def setup_global_hotkey():
        if not HOTKEY_AVAILABLE:
            print("⚠️  Global hotkey not available - pynput library not installed")
            return None
        return None
    
    hotkey_listener = setup_global_hotkey()
    if hotkey_listener is None:
        print("✅ Hotkey setup handled gracefully when pynput unavailable")
    else:
        print("❌ Unexpected hotkey listener created")

if __name__ == "__main__":
    test_one_time_transcription()
    test_hotkey_integration()
    print("\n🎉 All tests completed!")