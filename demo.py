#!/usr/bin/env python3
"""
Example demonstrating the Ctrl+- one-time dictation feature usage.
This example shows how to trigger one-time transcription programmatically.
"""

import time
import threading

def demo_one_time_dictation():
    """
    Demonstrate the one-time dictation feature flow.
    This simulates what happens when Ctrl+- is pressed.
    """
    print("🎤 Demo: One-Time Dictation Feature")
    print("=" * 50)
    
    print("\n1. User presses Ctrl+- while in any application")
    print("   (e.g., while gaming, writing emails, chatting)")
    
    print("\n2. Application detects global hotkey")
    print("   ✅ Hotkey detected: Ctrl+-")
    
    print("\n3. One-time transcription starts (max 10 seconds)")
    print("   🎤 Recording started...")
    
    # Simulate recording time
    for i in range(3):
        print(f"   📡 Recording... {i+1}/3 seconds")
        time.sleep(1)
    
    print("   🔍 Processing audio...")
    time.sleep(0.5)
    
    print("\n4. Transcription completed")
    example_text = "Hello team, let's group up and push the objective!"
    print(f"   📝 Transcribed: \"{example_text}\"")
    
    print("\n5. Text automatically pasted")
    print("   📋 Copied to clipboard")
    print("   ⌨️  Pressed Ctrl+V (auto-paste)")
    
    print("\n6. User continues with their application")
    print("   🎮 Game/application remains focused")
    print("   ✅ Text appears where the cursor was")
    
    print("\n" + "=" * 50)
    print("🎉 One-time dictation complete!")

def demo_wake_word_mode():
    """
    Demonstrate the traditional wake word mode for comparison.
    """
    print("\n🗣️  Demo: Wake Word Mode (Continuous)")
    print("=" * 50)
    
    print("\n1. User says 'computer'")
    print("   ✅ Wake word detected - continuous mode activated")
    
    print("\n2. Continuous transcription active")
    print("   🎤 Say anything... (transcribing continuously)")
    
    example_phrases = [
        "This is my first sentence.",
        "Here's another thought.",
        "And one more idea."
    ]
    
    for i, phrase in enumerate(example_phrases, 1):
        time.sleep(1)
        print(f"   📝 Transcribed #{i}: \"{phrase}\"")
        print(f"   ⌨️  Auto-pasted: \"{phrase}\"")
    
    print("\n3. User says 'terminator'")
    print("   🛑 Sleep word detected - continuous mode stopped")
    
    print("\n" + "=" * 50)
    print("✅ Wake word mode complete!")

def demo_integration():
    """
    Show how both modes work together.
    """
    print("\n🔄 Demo: Integration of Both Modes")
    print("=" * 50)
    
    print("\n✅ Both modes can be used simultaneously:")
    print("   • Wake word mode: For long conversations/dictation")
    print("   • Ctrl+- hotkey: For quick, one-off transcriptions")
    
    print("\n📋 Example scenarios:")
    print("   🎮 Gaming: Use Ctrl+- for quick team communication")
    print("   📝 Writing: Use wake words for continuous dictation")
    print("   💬 Chat: Use Ctrl+- for quick responses")
    print("   📊 Meetings: Use wake words for note-taking")
    
    print("\n🔒 Key benefits:")
    print("   • No focus stealing (great for games)")
    print("   • Works from any application")
    print("   • Doesn't interfere with existing functionality")
    print("   • Gracefully handles missing dependencies")

def main():
    """Run all demonstrations."""
    print("🎯 OpenAI Transcribing - Feature Demonstration")
    print("=" * 60)
    
    # Run demos
    demo_one_time_dictation()
    time.sleep(1)
    
    demo_wake_word_mode()
    time.sleep(1)
    
    demo_integration()
    
    print("\n🎉 All demonstrations complete!")
    print("\nTo use the actual feature:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set up your Porcupine API key in voice_to_text_vr.py")
    print("3. Run: python voice_to_text_vr.py")
    print("4. Press Ctrl+- from anywhere for one-time dictation!")

if __name__ == "__main__":
    main()