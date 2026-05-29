# File made to test engine functionality with real FFmpeg metric extraction on .y4m files
import os
from experiments_engine.engine import Engine

ref_video = "experiments_engine/tests/test_data/akiyo_qcif.y4m"
test_video = "experiments_engine/tests/test_data/akiyo_qcif.y4m"

if not os.path.exists(ref_video) or not os.path.exists(test_video):
    print("Error: Missing reference or test .y4m files in test_data directory.")
    exit(1)

engine = Engine(store=None, encoder=None, output_store=None, decoder=None)

print("Starting FFmpeg metric extraction engine...")
print(f"Reference: {ref_video}")
print(f"Distorted: {test_video}\n")

try:
    metrics = engine._calculate_metrics(ref_video, test_video)
    
    print("Engine successfully parsed metrics:")
    print(f"PSNR Score: {metrics.get('psnr')}")
    print(f"SSIM Score: {metrics.get('ssim')}")

except Exception as e:
    print(f"Engine failed during execution: {e}")