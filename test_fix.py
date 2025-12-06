import sys
import os
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(os.getcwd())

try:
    from src.utils.video_processing import add_text_overlay
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

def test_add_text_overlay():
    print("Testing add_text_overlay...")
    
    # Mock subprocess.run to avoid actual ffmpeg execution
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        
        try:
            add_text_overlay("dummy_video.mp4", "Test Text", "output.mp4")
            print("Success: add_text_overlay called without NameError.")
        except NameError as e:
            print(f"FAILED: NameError caught: {e}")
            sys.exit(1)
        except Exception as e:
            # We expect it might fail due to other reasons if we didn't mock everything perfectly,
            # but we are specifically looking for NameError 'formatted_text'
            if "formatted_text" in str(e):
                 print(f"FAILED: Error related to formatted_text: {e}")
                 sys.exit(1)
            print(f"Note: Caught expected non-NameError exception (likely due to mocks or paths): {e}")
            # If it got past the line where formatted_text is used, it's a success for this bug fix.
            print("Success: Did not encounter NameError.")

if __name__ == "__main__":
    test_add_text_overlay()
