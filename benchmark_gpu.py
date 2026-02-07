"""
Benchmark script to compare different Whisper models on your RTX 5080
Tests speed and shows GPU utilization
"""

import torch
import time
import tempfile
import wave
import numpy as np
from faster_whisper import WhisperModel

def generate_test_audio(duration_sec=10):
    """Generate a test audio file with silence + tone"""
    sample_rate = 16000
    samples = int(sample_rate * duration_sec)
    
    # Generate a simple tone
    frequency = 440  # A4 note
    audio = np.sin(2 * np.pi * frequency * np.linspace(0, duration_sec, samples))
    audio = (audio * 32767 * 0.5).astype(np.int16)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with wave.open(temp_file.name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    
    return temp_file.name

def benchmark_model(model_size, device, compute_type, audio_file):
    """Benchmark a specific model configuration"""
    print(f"\n{'='*60}")
    print(f"Testing: {model_size} ({compute_type}) on {device.upper()}")
    print(f"{'='*60}")
    
    try:
        # Load model
        print("⏳ Loading model...")
        load_start = time.time()
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        load_time = time.time() - load_start
        print(f"✅ Model loaded in {load_time:.2f}s")
        
        # Warm-up run
        print("🔥 Warming up...")
        model.transcribe(audio_file, beam_size=5)
        
        # Benchmark runs
        num_runs = 3
        times = []
        print(f"🏃 Running {num_runs} benchmark iterations...")
        
        for i in range(num_runs):
            start = time.time()
            segments, info = model.transcribe(audio_file, beam_size=5)
            # Force evaluation of generator
            list(segments)
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"  Run {i+1}: {elapsed:.3f}s")
        
        avg_time = sum(times) / len(times)
        print(f"\n📊 Average transcription time: {avg_time:.3f}s")
        print(f"⚡ Real-time factor: {10.0 / avg_time:.2f}x")
        
        if device == "cuda":
            vram_allocated = torch.cuda.memory_allocated() / 1024**3
            vram_reserved = torch.cuda.memory_reserved() / 1024**3
            print(f"💾 VRAM Used: {vram_allocated:.2f}GB (Reserved: {vram_reserved:.2f}GB)")
        
        return {
            "model": model_size,
            "device": device,
            "compute_type": compute_type,
            "load_time": load_time,
            "avg_time": avg_time,
            "realtime_factor": 10.0 / avg_time
        }
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🎮 GPU-Accelerated Whisper Benchmark Tool")
    print("=" * 60)
    
    # Check CUDA availability
    if torch.cuda.is_available():
        print(f"✅ CUDA Available")
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
        print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f}GB")
    else:
        print("❌ CUDA not available - will test CPU only")
    
    # Generate test audio
    print("\n🎵 Generating 10-second test audio...")
    audio_file = generate_test_audio(10)
    print(f"✅ Test audio created: {audio_file}")
    
    # Test configurations
    results = []
    
    if torch.cuda.is_available():
        # Test different models on GPU with FP16
        models_to_test = ["tiny", "base", "small", "medium"]
        
        for model_size in models_to_test:
            result = benchmark_model(model_size, "cuda", "float16", audio_file)
            if result:
                results.append(result)
        
        # Optionally test large-v2 if user has enough VRAM
        print("\n" + "="*60)
        test_large = input("Test large-v2 model? (requires ~10GB VRAM) [y/N]: ")
        if test_large.lower() == 'y':
            result = benchmark_model("large-v2", "cuda", "float16", audio_file)
            if result:
                results.append(result)
    
    # Test base model on CPU for comparison
    print("\n" + "="*60)
    test_cpu = input("Test CPU performance for comparison? [y/N]: ")
    if test_cpu.lower() == 'y':
        result = benchmark_model("base", "cpu", "int8", audio_file)
        if result:
            results.append(result)
    
    # Summary
    print("\n" + "="*60)
    print("📊 BENCHMARK SUMMARY")
    print("="*60)
    print(f"{'Model':<15} {'Device':<8} {'Load Time':<12} {'Avg Time':<12} {'RT Factor':<12}")
    print("-"*60)
    
    for r in results:
        print(f"{r['model']:<15} {r['device']:<8} {r['load_time']:.2f}s{'':<7} {r['avg_time']:.3f}s{'':<7} {r['realtime_factor']:.2f}x")
    
    print("\n💡 Recommendations:")
    if results:
        fastest = min(results, key=lambda x: x['avg_time'])
        print(f"   Fastest: {fastest['model']} ({fastest['avg_time']:.3f}s, {fastest['realtime_factor']:.1f}x realtime)")
        
        # Find best balance
        balanced = [r for r in results if r['realtime_factor'] > 5 and r['model'] in ['base', 'small', 'medium']]
        if balanced:
            best = max(balanced, key=lambda x: x['model'])
            print(f"   Recommended: {best['model']} (good balance of speed and accuracy)")
    
    print("\n✅ Benchmark complete!")

if __name__ == "__main__":
    main()
