# OpenAITranscribing
Free transcribing with global hotkey support.
<img width="1843" height="720" alt="image" src="https://github.com/user-attachments/assets/637ba197-f983-427f-b104-0dd08423175a" />

Enjoy.
Register your free key, and you're ready to rock'n'roll: https://picovoice.ai/platform/porcupine/
OpenAITranscribing is a free and open-source tool for effortless voice transcription powered by Python and OpenAI.

## Features

- Fast and accurate voice-to-text transcription
- Powered by OpenAI Whisper models
- **NEW: Global Ctrl+- hotkey for one-time dictation** 🎤
- Wake word activation ("computer" to start, "terminator" to stop)
- Easy to use interface
- Works even when app is not focused (great for gaming!)
- Completely free and open-source
- Written in Python

## Quick Start

### Wake Word Mode (Continuous)
1. Say **"computer"** - starts continuous transcription
2. Speak normally - your speech is transcribed and pasted automatically
3. Say **"terminator"** - stops continuous transcription

### One-Time Dictation (New!)
1. Press **Ctrl+- (Ctrl + numpad minus)** from anywhere
2. Speak for up to 10 seconds
3. Transcription is automatically pasted where your cursor is
4. Perfect for gaming, quick notes, or any situation where you need just one transcription

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DontDoThat21/OpenAITranscribing.git
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Porcupine access key:**
   - Get a free key from: https://picovoice.ai/platform/porcupine/
   - Edit `voice_to_text_vr.py` and replace `PORCUPINE_ACCESS_KEY = ""` with your key

4. **Run the application:**
   ```bash
   python voice_to_text_vr.py
   ```

## Usage Examples

### Gaming 🎮
While playing your favorite game:
- Press **Ctrl+-** (without alt-tabbing!)
- Say "gg team, well played!"
- The message appears in your game chat instantly

### Quick Notes 📝
While working in any application:
- Press **Ctrl+-**
- Say "Remember to call mom at 3pm"
- The reminder appears wherever your text cursor is

### Continuous Dictation 🗣️
For longer transcriptions:
- Say **"computer"** to start continuous mode
- Speak naturally for as long as needed
- Say **"terminator"** when finished

## Dependencies

Core dependencies (automatically installed):
- `openai-whisper` - AI transcription model
- `sounddevice` - Audio input/output
- `pyautogui` - Automated typing
- `pyperclip` - Clipboard operations
- `webrtcvad` - Voice activity detection
- `pvporcupine` - Wake word detection

Optional dependencies:
- `pynput` - Global hotkey support (for Ctrl+- feature)

**Note:** If `pynput` is not installed, the application will work normally but the global Ctrl+- hotkey will be disabled.

## Troubleshooting

### Global Hotkey Not Working
- Install pynput: `pip install pynput`
- On Windows: Run as administrator for global hotkey access
- On Linux: Ensure user has access to input devices
- On macOS: Grant accessibility permissions in System Preferences

### Audio Issues
- Check microphone permissions
- Verify microphone is not muted
- Test with other audio applications first

### Permission Issues
Some systems require additional permissions for global hotkey detection:
- **Windows**: Run Command Prompt as Administrator, then run the application
- **Linux**: Add user to `input` group: `sudo usermod -a -G input $USER`
- **macOS**: System Preferences → Security & Privacy → Accessibility → Add Python/Terminal

## How It Works

The application uses:
- **OpenAI Whisper** for accurate speech-to-text transcription
- **Porcupine** for wake word detection ("computer"/"terminator")
- **pynput** for global hotkey detection (Ctrl+-)
- **WebRTC VAD** for voice activity detection
- **Auto-paste** functionality to insert transcribed text

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

### Recent Updates
- ✅ Added global Ctrl+- hotkey for one-time dictation
- ✅ Improved game compatibility (no focus stealing)
- ✅ Better error handling and graceful degradation
- ✅ Comprehensive test suite

---

Free voice transcribing with global hotkey support.
Copilot was heavily utilized for this project.
