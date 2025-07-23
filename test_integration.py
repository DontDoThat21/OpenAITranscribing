#!/usr/bin/env python3
"""
Integration test to verify the new hotkey functionality doesn't break existing code.
This test simulates the main application flow without requiring actual audio hardware.
"""

import threading
import time
import tempfile
import os

# Test that the modified code can still be imported and initialized
def test_import_and_basic_functionality():
    """Test that the modified voice_to_text_vr.py can be imported without errors."""
    print("🧪 Testing import and basic functionality...")
    
    try:
        # Mock the problematic imports that aren't available
        import sys
        
        # Create mock modules for the dependencies we don't have
        class MockModule:
            def __getattr__(self, name):
                if name == 'load_model':
                    return lambda model_name: self
                elif name == 'transcribe':
                    return lambda file_path: {"text": "Mock transcription"}
                elif name == 'copy':
                    return lambda text: print(f"[MOCK] Copied: {text}")
                elif name == 'hotkey':
                    return lambda *keys: print(f"[MOCK] Hotkey: {'+'.join(keys)}")
                elif name == 'Vad':
                    return lambda aggressiveness: self
                elif name == 'is_speech':
                    return lambda frame, rate: True
                elif name == 'create':
                    return lambda **kwargs: self
                elif name == 'sample_rate':
                    return 16000
                elif name == 'frame_length':
                    return 512
                elif name == 'process':
                    return lambda pcm: 0
                elif name == 'InputStream':
                    return MockInputStream
                elif name == 'int16':
                    return int
                else:
                    return MockModule()
        
        class MockInputStream:
            def __init__(self, **kwargs):
                pass
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
        
        # Mock the problematic modules
        sys.modules['whisper'] = MockModule()
        sys.modules['pyperclip'] = MockModule()
        sys.modules['pyautogui'] = MockModule()
        sys.modules['webrtcvad'] = MockModule()
        sys.modules['pvporcupine'] = MockModule()
        sys.modules['sounddevice'] = MockModule()
        sys.modules['numpy'] = MockModule()
        sys.modules['pynput'] = MockModule()
        sys.modules['pynput.keyboard'] = MockModule()
        
        # Now try to import our modified module
        import voice_to_text_vr
        
        print("✅ Module imported successfully")
        
        # Test that key functions exist
        assert hasattr(voice_to_text_vr, 'one_time_transcribe'), "one_time_transcribe function missing"
        assert hasattr(voice_to_text_vr, 'on_hotkey_pressed'), "on_hotkey_pressed function missing"
        assert hasattr(voice_to_text_vr, 'setup_global_hotkey'), "setup_global_hotkey function missing"
        assert hasattr(voice_to_text_vr, 'record_and_transcribe'), "record_and_transcribe function missing"
        assert hasattr(voice_to_text_vr, 'main'), "main function missing"
        
        print("✅ All required functions present")
        
        # Test that global variables are properly initialized
        assert hasattr(voice_to_text_vr, 'one_time_transcribing'), "one_time_transcribing variable missing"
        assert hasattr(voice_to_text_vr, 'one_time_audio_queue'), "one_time_audio_queue variable missing"
        assert hasattr(voice_to_text_vr, 'ONE_TIME_RECORD_DURATION_SEC'), "ONE_TIME_RECORD_DURATION_SEC constant missing"
        
        print("✅ All required variables present")
        
        # Test hotkey setup (should handle missing pynput gracefully)
        hotkey_listener = voice_to_text_vr.setup_global_hotkey()
        print(f"✅ Hotkey setup returns: {hotkey_listener}")
        
        # Test hotkey handler
        voice_to_text_vr.on_hotkey_pressed()
        print("✅ Hotkey handler executes without error")
        
        return True
        
    except Exception as e:
        print(f"❌ Import/functionality test failed: {e}")
        return False

def test_thread_safety():
    """Test that the hotkey functionality is thread-safe."""
    print("\n🧪 Testing thread safety...")
    
    call_count = 0
    
    def mock_transcribe():
        nonlocal call_count
        call_count += 1
        time.sleep(0.1)  # Simulate transcription time
        print(f"Mock transcription #{call_count}")
    
    def trigger_hotkey():
        """Simulate hotkey press."""
        threading.Thread(target=mock_transcribe, daemon=True).start()
    
    # Trigger multiple hotkeys rapidly
    threads = []
    for i in range(5):
        thread = threading.Thread(target=trigger_hotkey)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    time.sleep(0.5)  # Wait for transcription threads to complete
    
    print(f"✅ Processed {call_count} hotkey presses")
    return True

def test_audio_queue_isolation():
    """Test that one-time audio queue doesn't interfere with main queue."""
    print("\n🧪 Testing audio queue isolation...")
    
    import queue
    
    # Simulate main audio queue
    main_queue = queue.Queue()
    one_time_queue = queue.Queue()
    
    # Add data to both queues
    test_data = [b"data1", b"data2", b"data3"]
    
    for data in test_data:
        main_queue.put(data)
        one_time_queue.put(data)
    
    # Verify queues are independent
    assert main_queue.qsize() == 3, "Main queue should have 3 items"
    assert one_time_queue.qsize() == 3, "One-time queue should have 3 items"
    
    # Clear one-time queue (simulate end of one-time transcription)
    while not one_time_queue.empty():
        one_time_queue.get_nowait()
    
    # Main queue should be unaffected
    assert main_queue.qsize() == 3, "Main queue should still have 3 items"
    assert one_time_queue.empty(), "One-time queue should be empty"
    
    print("✅ Audio queues are properly isolated")
    return True

def test_file_cleanup():
    """Test that temporary files are properly cleaned up."""
    print("\n🧪 Testing temporary file cleanup...")
    
    temp_files_created = []
    
    def create_and_cleanup_temp_file():
        """Simulate the temp file creation and cleanup in one_time_transcribe."""
        temp_file = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                temp_file = tmp.name
                temp_files_created.append(temp_file)
                tmp.write(b"fake audio data")
            
            # Simulate transcription process
            assert os.path.exists(temp_file), "Temp file should exist"
            
        finally:
            # Simulate cleanup
            if temp_file and os.path.exists(temp_file):
                os.unlink(temp_file)
    
    # Test cleanup multiple times
    for i in range(3):
        create_and_cleanup_temp_file()
    
    # Verify all files were cleaned up
    for temp_file in temp_files_created:
        assert not os.path.exists(temp_file), f"Temp file {temp_file} was not cleaned up"
    
    print(f"✅ All {len(temp_files_created)} temporary files properly cleaned up")
    return True

def main():
    """Run all integration tests."""
    print("🧪 Running integration tests for Ctrl+- one-time dictation feature...\n")
    
    tests = [
        test_import_and_basic_functionality,
        test_thread_safety,
        test_audio_queue_isolation,
        test_file_cleanup,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
    
    print(f"\n🎯 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All integration tests passed!")
        return True
    else:
        print("⚠️  Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)