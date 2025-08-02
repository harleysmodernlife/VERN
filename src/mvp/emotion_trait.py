"""
VERN Emotion Recognition & Trait Modeling
----------------------------------------
Provides functions for text-based emotion classification and psychological trait inference.
Integrates with archetype resonance mapping for adaptive user profiling.

- emotion_classify(text): returns dict of emotion scores (e.g., joy, sadness, anger, etc.)
- trait_infer(text): returns dict of Big Five/MBTI trait scores

Uses HuggingFace transformers (if available) and open datasets (MELD, EmotionLines).
"""

import logging

try:
    from transformers import pipeline
    # Emotion model: multi-class emotion classification
    emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
    # Big Five/MBTI: fallback to sentiment analysis or custom model if available
    trait_classifier = pipeline("sentiment-analysis")
    HF_AVAILABLE = True
except Exception as e:
    logging.warning(f"HuggingFace transformers not available or model load failed: {e}")
    HF_AVAILABLE = False

EMOTIONS = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]
BIG_FIVE = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
MBTI = ["INTJ", "INFJ", "INFP", "ENFP", "ENTP", "ENTJ", "ENFJ", "ISTJ", "ISFJ", "ISTP", "ISFP", "ESTP", "ESFP", "ESTJ", "ESFJ"]

def emotion_classify(text: str) -> dict:
    """
    Classify emotions in text. Returns dict of emotion scores.
    Uses HuggingFace emotion model if available, else returns neutral.
    """
    if HF_AVAILABLE:
        try:
            results = emotion_classifier(text)
            # Aggregate scores for each emotion
            scores = {item['label'].lower(): round(item['score'], 3) for item in results[0]}
            # Ensure all expected emotions are present
            for e in EMOTIONS:
                if e not in scores:
                    scores[e] = 0.0
            return scores
        except Exception as e:
            logging.error(f"Emotion classification failed: {e}")
            return {e: 0.0 for e in EMOTIONS}
    else:
        # Fallback: neutral
        return {e: (1.0 if e == "neutral" else 0.0) for e in EMOTIONS}

def trait_infer(text: str) -> dict:
    """
    Infer psychological traits from text. Returns dict of Big Five and MBTI scores.
    Uses HuggingFace sentiment analysis as fallback; replace with Big Five/MBTI model if available.
    """
    if HF_AVAILABLE:
        try:
            # Sentiment as proxy for extraversion/agreeableness (demo only)
            sentiment = trait_classifier(text)[0]
            big_five_scores = {
                "openness": 0.5,
                "conscientiousness": 0.5,
                "extraversion": 0.8 if sentiment["label"] == "POSITIVE" else 0.2,
                "agreeableness": 0.8 if sentiment["label"] == "POSITIVE" else 0.2,
                "neuroticism": 0.2 if sentiment["label"] == "POSITIVE" else 0.8
            }
            mbti_type = "ENFP" if sentiment["label"] == "POSITIVE" else "INTJ"
            return {"big_five": big_five_scores, "mbti": mbti_type}
        except Exception as e:
            logging.error(f"Trait inference failed: {e}")
            return {"big_five": {t: 0.5 for t in BIG_FIVE}, "mbti": "INTJ"}
    else:
        # Fallback: neutral trait scores
        return {"big_five": {t: 0.5 for t in BIG_FIVE}, "mbti": "INTJ"}

# Example usage:
# emotions = emotion_classify("I'm feeling great today!")
# traits = trait_infer("I love exploring new ideas and helping others.")
