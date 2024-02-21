from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image
import reports_detector as rd


def image_searcher(query,uploaded_files):
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    uploaded_img_reports=[]
    supported_formats=["jpg", "jpeg", "png"]

    for filename in uploaded_files:
        is_Imagefile = rd.check_file_format(filename, supported_formats)
        if is_Imagefile:
            uploaded_img_reports.append(filename)

    #loading uploaded images
    images = [Image.open(img_path) for img_path in uploaded_img_reports]

    # Preprocess images and text using the model's processor
    inputs = processor(text=query, images=images, return_tensors="pt")

    outputs = model(**inputs)
    image_features = outputs.image_embeds
    text_features = outputs.text_embeds

    # Calculate cosine similarities between text and image embeddings
    similarities = torch.cosine_similarity(text_features, image_features)

    # Get indices of top-k similar images
    top_k = similarities.topk(k=2)  # Retrieve top 5 similar images
    similar_image_indices = top_k.indices.tolist()

    # Load and display retrieved images
    similar_images = [images[index] for index in similar_image_indices]
    print("similar images:",similar_images)

    return similar_images
