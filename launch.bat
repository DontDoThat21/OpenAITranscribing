@echo off
echo ========================================
echo  Voice-to-Text GPU (RTX 5080 Optimized)
echo ========================================
echo.

REM Activate conda environment if needed
REM call conda activate your_env_name

echo Starting GPU-accelerated voice transcription...
echo.

python voice_to_text_vr_gpu.py ada4c3a185594ddbb8cf5788c5442e74=True

echo.
echo ========================================
echo  Application closed
echo ========================================
pause
