"""
Quick test to verify GPU acceleration and RTX 5080 compatibility
"""
import torch
import warnings
import tempfile
import wave
import numpy as np

# Suppress RTX 50 series warning
warnings.filterwarnings('ignore', message='.*CUDA capability sm_120.*')

print("="*60)
print("🔍 GPU Detection Test")
print("="*60)

# Check CUDA
if torch.cuda.is_available():
    print(f"✅ CUDA is available")
    print(f"   GPU: {torch.cuda.get_device_name(0)}")
    print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    print(f"   PyTorch: {torch.__version__}")
    print(f"   Compute Capability: sm_{torch.cuda.get_device_capability()[0]}{torch.cuda.get_device_capability()[1]}")
else:
    print("❌ CUDA is not available")
    exit(1)

print("\n" + "="*60)
print("🧪 Testing faster-whisper with GPU")
print("="*60)

try:
    from faster_whisper import WhisperModel
    print("✅ faster-whisper imported successfully")
    
    # Try to load model
    print("\n⏳ Loading tiny model on GPU...")
    model = WhisperModel("tiny", device="cuda", compute_type="float16")
    print("✅ Model loaded successfully!")
    
    # Generate test audio
    print("\n🎵 Generating test audio (3 seconds of silence)...")
    sample_rate = 16000
    duration = 3
    audio = np.zeros(sample_rate * duration, dtype=np.int16)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with wave.open(temp_file.name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    
    print(f"✅ Test audio created: {temp_file.name}")
    
    # Test transcription
    print("\n⚡ Testing GPU transcription...")
    import time
    start = time.time()
    segments, info = model.transcribe(temp_file.name, beam_size=5)
    list(segments)  # Force evaluation
    elapsed = time.time() - start
    
    print(f"✅ Transcription completed in {elapsed:.3f}s")
    print(f"   Language: {info.language}")
    print(f"   Language probability: {info.language_probability:.2f}")
    
    # Check GPU usage
    print("\n💾 GPU Memory Usage:")
    print(f"   Allocated: {torch.cuda.memory_allocated() / 1024**2:.1f} MB")
    print(f"   Reserved: {torch.cuda.memory_reserved() / 1024**2:.1f} MB")
    
    print("\n" + "="*60)
    print("🎉 SUCCESS! GPU acceleration is working!")
    print("="*60)
    print("\n✨ Your RTX 5080 is ready for voice transcription!")
    print("   Despite the capability warning, the GPU works fine.")
    print("   You can now run: python voice_to_text_vr_gpu.py")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print("\n⚠️  GPU acceleration may not be working properly")
