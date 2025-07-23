#!/usr/bin/env python3
"""
Simple test script to validate the hotkey functionality without full dependencies.
"""

import time
import threading

# Mock the dependencies for testing
class MockWhisper:
    def transcribe(self, file_path):
        return {"text": "Mock transcription result"}

class MockPyperclip:
    def copy(self, text):
        print(f"[MOCK] Copied to clipboard: {text}")

class MockPyautogui:
    def hotkey(self, *keys):
        print(f"[MOCK] Pressed hotkey: {' + '.join(keys)}")

# Mock modules
model = MockWhisper()
pyperclip = MockPyperclip()
pyautogui = MockPyautogui()

# Global state
one_time_transcribing = False

def one_time_transcribe():
    """Mock one-time transcription for testing."""
    global one_time_transcribing
    
    if one_time_transcribing:
        return
    
    print("🎤 One-time transcription started...")
    one_time_transcribing = True
    
    # Simulate recording and transcription
    time.sleep(2)  # Simulate recording time
    
    # Mock transcription
    text = "This is a test transcription"
    print(f"📝 One-time transcription: {text}")
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    
    one_time_transcribing = False
    print("✅ One-time transcription completed")

def on_hotkey_pressed():
    """Handle the hotkey press."""
    print("🔥 Hotkey detected!")
    threading.Thread(target=one_time_transcribe, daemon=True).start()

def test_hotkey_simulation():
    """Test the hotkey functionality with manual simulation."""
    print("Testing hotkey functionality...")
    print("Simulating Ctrl+- press in 3 seconds...")
    
    time.sleep(3)
    on_hotkey_pressed()
    
    time.sleep(5)  # Wait for transcription to complete
    print("Test completed!")

if __name__ == "__main__":
    test_hotkey_simulation()