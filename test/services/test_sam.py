import cv2
import pytest
import os

from app.services.segment_anything.sam import SAMSegmentationService

@pytest.fixture
def sam_service():
    """Fixture to initialize the SAM Segmentation Service"""
    return SAMSegmentationService()

def test_sam_segmentation_service(sam_service):
    """Test the SAM model for segmenting the largest object"""
    image_path = "test/.testimages/image.png"
    
    assert os.path.exists(image_path), f"Test image not found: {image_path}"

    highlighted_image, largest_mask, highlighted_percentage = sam_service.segment_largest_region(image_path)
    
    print(f"\nHighlighted percentage: {highlighted_percentage:.2f}%")

    assert highlighted_percentage > 0, "Highlighted percentage should be greater than 0"
    assert highlighted_percentage <= 100, "Highlighted percentage should be less than or equal to 100"

    assert highlighted_image is not None, "Highlighted image should not be None"
    assert largest_mask is not None, "Largest mask should not be None"

    # Show the highlighted image
    output_path = "test/.testimages/segmented_image.png"
    cv2.imwrite(output_path, highlighted_image)
    assert os.path.exists(output_path), f"Failed to save the segmented image: {output_path}"