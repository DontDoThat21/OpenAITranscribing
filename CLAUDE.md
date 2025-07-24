# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenAITranscribing is a Python-based voice-to-text transcription tool with two main modes:
1. **Wake word mode**: Continuous transcription activated by saying "computer" and stopped by "terminator"
2. **One-time dictation**: Global hotkey (Ctrl+-) for single transcriptions without entering continuous mode

The application uses OpenAI Whisper for transcription, Porcupine for wake word detection, and automatically pastes transcribed text using clipboard operations.

## Key Architecture

### Core Components
- `voice_to_text_vr.py` - Main application with all functionality
- Wake word detection using Porcupine with configurable keywords
- Voice Activity Detection (VAD) using webrtcvad for speech detection
- Dual audio queues: one for continuous mode, one for one-time transcription
- Global hotkey system using pynput (optional dependency with graceful fallback)

### Audio Processing Flow
1. Audio input captured via sounddevice
2. VAD determines speech vs silence
3. Audio buffered until silence threshold reached
4. Whisper model transcribes audio from temporary WAV files
5. Text copied to clipboard and auto-pasted with Ctrl+V

### Configuration (voice_to_text_vr.py:24-36)
Key settings at top of main file:
- `SAMPLE_RATE = 16000` - Audio sample rate
- `VAD_AGGRESSIVENESS = 2` - Voice activity detection sensitivity
- `SILENCE_DURATION_SEC = 1.0` - Silence threshold for transcription trigger
- `ONE_TIME_RECORD_DURATION_SEC = 10.0` - Max recording time for hotkey mode
- `PORCUPINE_ACCESS_KEY` - Required API key for wake word detection
- Buffer size limits to prevent memory issues

## Common Commands

### Running the Application
```bash
python voice_to_text_vr.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Testing
Run the comprehensive test suite:
```bash
python test_comprehensive.py
```

For hotkey-specific testing:
```bash
python test_hotkey.py
```

For integration testing:
```bash
python test_integration.py
```

## Development Notes

### Required Setup
1. Porcupine API key must be set in `PORCUPINE_ACCESS_KEY` constant
2. Microphone permissions required for audio input
3. Optional: pynput for global hotkey (gracefully degrades without it)

### Key Functions
- `transcribe_audio_buffer()` - Core transcription with temp file handling
- `wakeword_listener()` - Porcupine wake word detection loop
- `one_time_transcribe()` - Hotkey-triggered single transcription
- `record_and_transcribe()` - Main continuous recording loop
- `audio_callback()` - Audio stream callback that feeds both queues

### Global State Management
- `transcribing` - Boolean for continuous mode state
- `one_time_transcribing` - Boolean for hotkey mode state
- `audio_queue` - Queue for continuous mode audio
- `one_time_audio_queue` - Separate queue for hotkey mode

### Memory Management
- Automatic buffer size monitoring with `MAX_BUFFER_SIZE_MB` limit
- Fast queue clearing using collections.deque
- Temporary file cleanup after transcription
- Audio state reset functions to prevent memory leaks

## Testing Architecture

The project includes comprehensive tests with mock objects for all external dependencies:
- Mock implementations for Whisper, sounddevice, pynput, etc.
- Tests cover both continuous and one-time transcription modes
- Hotkey functionality testing with simulated key presses
- Integration tests for full workflow validation