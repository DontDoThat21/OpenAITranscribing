# Ctrl+- One-Time Dictation Feature

This document describes the new Ctrl+- one-time dictation feature added to OpenAITranscribing.

## Feature Overview

The Ctrl+- hotkey provides a quick way to perform a single voice transcription without entering continuous transcription mode. This is useful for:

- Quick dictation while gaming (without losing focus)
- One-off transcriptions in other applications
- Situations where you don't want continuous transcription

## How It Works

1. **Press Ctrl+- (Ctrl + numpad minus)** - This can be done from any application
2. **Start speaking immediately** - The system begins recording for up to 10 seconds
3. **The transcription is automatically pasted** - Text is copied to clipboard and pasted with Ctrl+V

## Key Features

- **Global hotkey**: Works even when the app is not focused
- **Non-intrusive**: Does not steal focus from games or other applications
- **One-time only**: Records for a limited time (10 seconds max) then stops
- **Independent**: Does not interfere with existing wake word functionality

## Installation Requirements

To use the global hotkey functionality, you need to install the `pynput` library:

```bash
pip install pynput
```

If `pynput` is not available, the application will still work but the global hotkey will be disabled.

## Usage Examples

### Gaming
While playing a game:
1. Press Ctrl+- (without alt-tabbing)
2. Say "Hello team, let's attack point B"
3. The text is automatically pasted in the game chat

### Quick Notes
While in any application:
1. Press Ctrl+-
2. Say "Remember to buy milk and eggs"
3. The text appears wherever your cursor is

## Technical Details

- **Recording Duration**: Maximum 10 seconds per activation
- **Audio Processing**: Uses the same high-quality Whisper model as continuous mode
- **Hotkey Detection**: Uses pynput library for global hotkey detection
- **Thread Safety**: Runs in separate thread to avoid blocking the main application

## Coexistence with Wake Words

The new Ctrl+- feature works alongside the existing wake word system:

- **"computer"** - Still starts continuous transcription mode
- **"terminator"** - Still stops continuous transcription mode  
- **Ctrl+-** - Performs one-time transcription regardless of current mode

## Troubleshooting

### Hotkey Not Working
- Ensure `pynput` is installed: `pip install pynput`
- Check if another application is using the same hotkey
- Try running the application as administrator (Windows) or with appropriate permissions (Linux)

### No Audio Detected
- Check your microphone settings
- Ensure the microphone is not muted
- Speak clearly and close to the microphone

### Permission Issues
On some systems, global hotkey detection may require additional permissions:
- **Windows**: Run as administrator for global hotkey access
- **Linux**: Ensure the user has access to input devices
- **macOS**: Grant accessibility permissions in System Preferences

## Implementation Notes

The feature is implemented with minimal changes to the existing codebase:

1. Added global hotkey detection using pynput
2. Created separate audio queue for one-time transcription
3. Implemented timeout mechanism for limited recording duration
4. Added graceful fallback when pynput is not available

The implementation maintains full backward compatibility with existing functionality.