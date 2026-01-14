import os
from pathlib import Path
from typing import Tuple
from PIL import Image, ImageChops
from qa_framework.core.drivers.abstract_driver import AbstractDriver
from qa_framework.core.logger import get_logger

logger = get_logger("visual_manager")

class VisualManager:
    """
    Manager for Visual Regression Testing (Snapshot Testing).
    """

    def __init__(self, driver: AbstractDriver, baseline_dir: str = "tests/visual/baselines", failure_dir: str = "tests/visual/failures"):
        self.driver = driver
        self.baseline_dir = Path(baseline_dir)
        self.failure_dir = Path(failure_dir)
        
        # Ensure directories exist
        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        self.failure_dir.mkdir(parents=True, exist_ok=True)

    def capture_screenshot(self, name: str) -> Path:
        """Captures a screenshot and returns the path."""
        path = self.failure_dir / f"{name}_current.png"
        self.driver.screenshot(str(path))
        return path

    def compare(self, name: str, threshold: float = 0.0) -> bool:
        """
        Compares the current view against the baseline.
        Returns True if match (within threshold), False otherwise.
        """
        baseline_path = self.baseline_dir / f"{name}.png"
        current_path = self.capture_screenshot(name)
        
        if not baseline_path.exists():
            logger.warning(f"Baseline not found for '{name}'. Creating new baseline.")
            # Move current to baseline
            current_path.rename(baseline_path)
            return True

        # Compare
        try:
            baseline_img = Image.open(baseline_path).convert('RGB')
            current_img = Image.open(current_path).convert('RGB')

            # Handle size mismatch
            if baseline_img.size != current_img.size:
                logger.error(f"Visual Mismatch: Size difference. Baseline: {baseline_img.size}, Current: {current_img.size}")
                self._save_diff(current_img, baseline_img, name)
                return False

            # Pixel comparison
            diff = ImageChops.difference(baseline_img, current_img)
            if diff.getbbox():
                # Differences found
                logger.error(f"Visual Mismatch for '{name}'")
                self._save_diff(current_img, baseline_img, name)
                return False
            
            logger.info(f"Visual Match for '{name}'")
            # Cleanup current if match
            current_path.unlink()
            return True

        except Exception as e:
            logger.error(f"Error during visual comparison: {e}")
            return False

    def _save_diff(self, current: Image.Image, baseline: Image.Image, name: str):
        """Saves the diff image for analysis."""
        diff_path = self.failure_dir / f"{name}_diff.png"
        diff = ImageChops.difference(baseline, current)
        diff.save(diff_path)
        logger.info(f"Saved diff image to {diff_path}")
