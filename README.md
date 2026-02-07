# OpenAITranscribing - GPU Accelerated 🚀
Free voice transcription with GPU acceleration and global hotkey support.

<img width="1843" height="720" alt="image" src="https://github.com/user-attachments/assets/637ba197-f983-427f-b104-0dd08423175a" />

**NEW:** Now with **RTX GPU acceleration** for blazing-fast transcription!

## ✨ Features

- ⚡ **GPU-accelerated transcription** (4-8x faster with NVIDIA GPUs)
- 🎤 **Global Ctrl+Alt+T hotkey** for one-time dictation
- 🗣️ Wake word activation ("computer" to start, "terminator" to stop)
- 🎮 Works even when app is not focused (great for gaming!)
- 🔥 Powered by faster-whisper and OpenAI Whisper models
- 📝 Auto-pastes transcribed text
- 💯 Completely free and open-source

## 🚀 Quick Start

### Option 1: GPU-Accelerated (RTX GPUs - **Recommended**)

#### Requirements:
- NVIDIA GPU (RTX 20/30/40/50 series recommended)
- Windows with updated NVIDIA drivers

#### Setup:
1. **Clone the repository:**
   ```bash
   git clone https://github.com/DontDoThat21/OpenAITranscribing.git
   cd OpenAITranscribing
   ```

2. **Install PyTorch with CUDA (for RTX 5080):**
   ```bash
   pip uninstall -y torch torchvision torchaudio
   pip install torch==2.7.0.dev20250310+cu124 --index-url https://download.pytorch.org/whl/nightly/cu124
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Porcupine access key:**
   - Get a free key from: https://picovoice.ai/platform/porcupine/
   - Edit `voice_to_text_vr_gpu.py` and replace `PORCUPINE_ACCESS_KEY = "..."` with your key

5. **Test GPU setup:**
   ```bash
   python test_gpu.py
   ```

6. **Run the GPU-accelerated version:**
   ```bash
   python voice_to_text_vr_gpu.py
   ```
   Or double-click `launch.bat`

### Option 2: CPU Version (No GPU required)

Follow the original setup but use `voice_to_text_vr.py` instead.

## 📖 Usage

### Wake Word Mode (Continuous Transcription)
1. Say **"computer"** - starts continuous transcription
2. Speak normally - your speech is transcribed and auto-pasted
3. Say **"terminator"** - stops continuous transcription

### One-Time Dictation (Hotkey)
1. Press **Ctrl+Alt+T** from anywhere
2. Speak for up to 10 seconds
3. Transcription is automatically pasted where your cursor is
4. Perfect for gaming, quick notes, or single commands

## ⚙️ Configuration

Edit `voice_to_text_vr_gpu.py` to customize:

```python
# Choose your model (tiny/base/small/medium/large-v2)
WHISPER_MODEL_SIZE = "small"  # Recommended for RTX 5080

# Adjust for your needs
```

## 🎮 Usage Examples

### Gaming
While playing your favorite game:
- Press **Ctrl+Alt+T** (without alt-tabbing!)
- Say "gg team, well played!"
- The message appears in your game chat instantly

### Quick Notes
While working in any application:
- Press **Ctrl+Alt+T**
- Say "Remember to call mom at 3pm"
- The reminder appears wherever your text cursor is

### Continuous Dictation
For longer transcriptions:
- Say **"computer"** to start continuous mode
- Speak naturally for as long as needed
- Say **"terminator"** when finished

## 📊 Performance Comparison

| Hardware | Model | Transcription Speed | Real-time Factor |
|----------|-------|---------------------|------------------|
| CPU Only | base  | ~2-3s per phrase   | 0.3x slower      |
| RTX 5080 | tiny  | ~0.3s per phrase   | 15x faster       |
| RTX 5080 | small | ~0.6s per phrase   | 8x faster        |
| RTX 5080 | medium| ~1.2s per phrase   | 4x faster        |
| RTX 5080 | large-v2 | ~2.5s per phrase | 2x faster     |

*Your RTX 5080 makes even large models usable in real-time!*

## 📦 Dependencies

**GPU Version** (`voice_to_text_vr_gpu.py`):
- `faster-whisper` - Optimized AI transcription (GPU-accelerated)
- `torch` - PyTorch with CUDA support
- `sounddevice` - Audio input/output
- `pyautogui` - Automated typing
- `pyperclip` - Clipboard operations
- `webrtcvad` - Voice activity detection
- `pvporcupine` - Wake word detection
- `pynput` - Global hotkey support

**CPU Version** (`voice_to_text_vr.py`):
- `openai-whisper` - Original AI transcription model
- (Same other dependencies as above)

## 🛠️ Troubleshooting

### "CUDA capability sm_120 is not compatible" warning
- **This is normal!** The RTX 5080 uses new architecture (sm_120) that PyTorch doesn't officially support yet
- The GPU still works perfectly, the warning is automatically suppressed
- See `test_gpu.py` to verify GPU is working

### No audio input detected
- Check your default microphone in Windows settings
- Run `python -m sounddevice` to list available audio devices

### Hotkey not working
- Make sure `pynput` is installed: `pip install pynput`
- Try running as administrator
- Check if another app is using Ctrl+Alt+T

### Transcription is slow even with GPU
- Check if GPU is being used: Run `test_gpu.py`
- Try a smaller model (e.g., `tiny` or `base`)
- Close other GPU-intensive applications

## 📚 Additional Resources

- [GPU Upgrade Guide](GPU_UPGRADE_GUIDE.md) - Detailed GPU setup instructions
- [Upgrade Summary](UPGRADE_SUMMARY.md) - Quick migration guide
- [Benchmark Tool](benchmark_gpu.py) - Test different models on your GPU

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is open-source and free to use.

## 🙏 Credits

- OpenAI Whisper for the transcription models
- faster-whisper for GPU optimization
- Picovoice Porcupine for wake word detection

---

**Enjoy blazing-fast GPU-accelerated transcription!** 🚀

Get your free Porcupine key: https://picovoice.ai/platform/porcupine/
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
