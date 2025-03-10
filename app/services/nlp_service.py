import torch
from transformers import pipeline

# Determine the device: use GPU if available, otherwise CPU
device = 0 if torch.cuda.is_available() else -1

# Initialize a zero-shot classification pipeline using a state-of-the-art model.
# This model will help in classifying the text as "fake" or "real".
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=device
)

def analyze_text(text: str) -> tuple:
    """
    Performs an advanced analysis of the input text using a zero-shot classification approach.
    
    The function classifies the text into two candidate labels: "fake" and "real".
    It returns a veracity score, representing the confidence for the "real" label,
    along with a detailed analysis report that includes the confidence scores for each label.
    
    Parameters:
        text (str): The text of the news article to be analyzed.
    
    Returns:
        tuple: A tuple containing:
            - veracity_score (float): Confidence score for the text being real.
            - report (str): A detailed analysis report.
    """
    candidate_labels = ["fake", "real"]
    result = classifier(text, candidate_labels)
    
    # Extract the confidence score for the "real" label
    try:
        real_index = result["labels"].index("real")
        veracity_score = result["scores"][real_index]
    except ValueError:
        veracity_score = 0.0

    # Build a detailed report based on the model's output
    report = "Advanced analysis report:\n"
    report += "Text analyzed using zero-shot classification with candidate labels: " + ", ".join(candidate_labels) + ".\n"
    for label, score in zip(result["labels"], result["scores"]):
        report += f"Label '{label}': confidence {score:.2f}\n"
    report += f"\nDetermined veracity score (for 'real'): {veracity_score:.2f}"
    
    return veracity_score, report
