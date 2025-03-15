import torch
import numpy as np
import cv2
import os
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator

class SAMSegmentationService:
    def __init__(self, model_path=os.path.join(os.path.dirname(__file__), "model", "sam_vit_h.pth")):
        """Initialize the SAM model."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = sam_model_registry["vit_h"](checkpoint=model_path).to(self.device)
        self.mask_generator = SamAutomaticMaskGenerator(self.model)

    def segment_largest_region(self, image_path):
        """Segments the largest region in the image using SAM2."""
        # Load image
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Generate masks
        masks = self.mask_generator.generate(image_rgb)
        if not masks:
            raise ValueError("No segments found in the image.")

        # Find the largest segment
        largest_mask = max(masks, key=lambda x: np.sum(x["segmentation"]))

        # Calculate the percentage of the highlighted area
        highlighted_area = np.sum(largest_mask["segmentation"])
        total_area = image.shape[0] * image.shape[1]
        highlighted_percentage = (highlighted_area / total_area) * 100

        # Overlay mask on the image
        highlighted_image = self.highlight_mask(image, largest_mask["segmentation"])

        return highlighted_image, largest_mask, highlighted_percentage

    def highlight_mask(self, image, mask):
        """Overlay the mask on the image to highlight the largest segment."""
        overlay = image.copy()
        border_color = (110,254,52)
        inner_highlight = (133, 187, 153)

        # Create a border around the mask
        contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(overlay, contours, -1, border_color, thickness=9)

        # Highlight the inner region of the mask
        overlay[mask] = inner_highlight

        # Blend with original image
        alpha = 0.5
        blended = cv2.addWeighted(image, 1 - alpha, overlay, alpha, 0)

        return blended
