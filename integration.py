def identify_prompt_type(prompt):
    """
    Identifies whether the given prompt is a text prompt or an image prompt.

    Args:
    prompt: The user-provided prompt.

    Returns:
    A string indicating the prompt type: "text" or "image".
    """
    # Check for presence of keywords indicative of text retrieval
    text_keywords = ["what", "who", "why", "where", "when", "how"]
    text_match = any(keyword in prompt.lower() for keyword in text_keywords)

    # Check for file extensions or image-related words
    image_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    image_words = ["image", "picture", "photo", "visual","report", "images", "reports"]
    image_match = any(ext in prompt for ext in image_extensions) or \
                any(word in prompt.lower() for word in image_words)

    # Determine prompt type based on matches
    if image_match and not text_match:
        return "image"
    elif text_match and not image_match:
        return "text"
    else:
        return "text"



