import cv2
import numpy as np
from PIL import Image, ExifTags
import os

def analyze_image(image_path: str) -> tuple:
    """
    Performs advanced analysis on the given image.
    
    This function analyzes both the image's histogram and its metadata (EXIF) to determine its authenticity.
    It checks for natural variations in the image and inspects metadata for any signs of modifications.
    
    Parameters:
        image_path (str): The file path to the image.
    
    Returns:
        tuple: A tuple containing:
            - veracity_score (float): Confidence score (between 0.0 and 1.0) indicating authenticity.
            - report (str): A detailed analysis report.
    """
    try:
        # Load the image using PIL and convert to RGB
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        return 0.0, f"Error loading image: {str(e)}"

    # Convert image to NumPy array for OpenCV processing
    image_np = np.array(image)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    
    # Calculate the histogram of the grayscale image and compute its standard deviation
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist_std = np.std(hist)
    
    # Basic analysis using histogram standard deviation
    base_score = 0.9 if hist_std > 50 else 0.4
    report = f"Image histogram standard deviation: {hist_std:.2f}.\n"
    
    # Attempt to extract EXIF data for extended analysis
    try:
        exif_data = image._getexif()
        if exif_data:
            exif_report = "EXIF Data Found:\n"
            for tag, value in exif_data.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                exif_report += f"  {decoded}: {value}\n"
            report += exif_report
            # Placeholder: Adjust score if certain EXIF tags indicate modifications
            if any("Adobe" in str(val) or "Photoshop" in str(val) for val in exif_data.values()):
                base_score -= 0.1
                report += "Indicator: Image metadata suggests possible post-processing modifications.\n"
        else:
            report += "No EXIF metadata found.\n"
    except Exception as e:
        report += f"Error reading EXIF data: {str(e)}\n"
    
    # Ensure the score is between 0 and 1
    veracity_score = max(0.0, min(base_score, 1.0))
    report += f"Determined veracity score: {veracity_score:.2f}.\n"
    report += "Final verdict: " + ("Image appears authentic." if veracity_score > 0.5 else "Image may be manipulated.")
    
    return veracity_score, report

def analyze_video(video_path: str) -> tuple:
    """
    Performs advanced analysis on the given video by sampling frames and analyzing each frame.
    
    The analysis includes histogram evaluation for each sampled frame and provides a detailed report.
    
    Parameters:
        video_path (str): The file path to the video.
    
    Returns:
        tuple: A tuple containing:
            - veracity_score (float): Average confidence score for the video's authenticity.
            - report (str): A detailed analysis report.
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return 0.0, "Error opening video file."
    except Exception as e:
        return 0.0, f"Error loading video: {str(e)}"
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    sample_rate = max(frame_count // 10, 1)  # Sample approximately 10 frames
    scores = []
    analyzed_frames = 0
    current_frame = 0
    frame_reports = ""
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if current_frame % sample_rate == 0:
            # Convert frame to grayscale and compute histogram standard deviation
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            hist_std = np.std(hist)
            frame_score = 0.9 if hist_std > 50 else 0.4
            scores.append(frame_score)
            analyzed_frames += 1
            frame_reports += f"Frame {current_frame}: histogram std = {hist_std:.2f}, score = {frame_score:.2f}\n"
        current_frame += 1
    cap.release()
    
    if analyzed_frames == 0:
        return 0.0, "No frames were analyzed from the video."
    
    average_score = sum(scores) / len(scores)
    report = f"Analyzed {analyzed_frames} frames from video. Average score: {average_score:.2f}.\n"
    report += frame_reports
    report += "\nFinal verdict: " + ("Video appears authentic." if average_score > 0.5 else "Video may be manipulated.")
    
    return average_score, report
