import json
import logging
import os
import time

import requests
from prometheus_client import Histogram
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_dir_path = os.environ.get('MODEL_DIR_PATH', 'ai_model')

# Model files
FILES_TO_DOWNLOAD = {
    "config.json": "https://huggingface.co/KoalaAI/Text-Moderation/resolve/main/config.json",
    "model.safetensors": "https://huggingface.co/KoalaAI/Text-Moderation/resolve/main/model.safetensors",
    "tokenizer_config.json": "https://huggingface.co/KoalaAI/Text-Moderation/resolve/main/tokenizer_config.json",
    "vocab.json": "https://huggingface.co/KoalaAI/Text-Moderation/resolve/main/vocab.json",
    "merges.txt": "https://huggingface.co/KoalaAI/Text-Moderation/resolve/main/merges.txt",
    "tokenizer.json": "https://huggingface.co/KoalaAI/Text-Moderation/resolve/main/tokenizer.json",
    "special_tokens_map.json": "https://huggingface.co/KoalaAI/Text-Moderation/resolve/main/special_tokens_map.json"
}


class KoalaAiTextModerator:
    koala_ai_model = None
    tokenizer = None
    model_metadata = None
    ai_model_loading_histogram = Histogram('ai_model_loading', 'Model loading duration in seconds')

    def __init__(self):
        start_time = time.time()
        self.load_ai_model()
        duration = time.time() - start_time
        logger.info("Model loading duration in seconds: %s", duration)
        self.ai_model_loading_histogram.observe(duration)

    def load_ai_model(self):
        # Load the model and tokenizer
        if not os.path.exists(model_dir_path):
            # Create the directory if it doesn't exist
            os.makedirs(model_dir_path, exist_ok=True)

            # Download model files
            for filename, url in FILES_TO_DOWNLOAD.items():
                response = requests.get(url)
                if response.status_code == 200:
                    with open(os.path.join(model_dir_path, filename), 'wb') as f:
                        f.write(response.content)
                        logger.info(f"Downloaded {filename}")
                else:
                    logger.info(f"Failed to download {filename} due to {response}")
                    raise Exception(f"Failed to download {filename} due to {response}")
        self.koala_ai_model = AutoModelForSequenceClassification.from_pretrained(model_dir_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir_path)
        self.model_metadata = self.load_model_metadata()

    @staticmethod
    def load_model_metadata():
        """Load the model metadata from config.json"""
        config_path = os.path.join(model_dir_path, "config.json")
        if not os.path.exists(config_path):
            raise Exception(f"Config file {config_path} does not exist")

        with open(os.path.join(config_path)) as f:
            config = json.load(f)
            return config

    def run_inference(self, text):
        if text is None:
            raise ValueError("Text argument cannot be None")

        # Run the model on your input
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.koala_ai_model(**inputs)

        # Get the predicted logits
        logits = outputs.logits

        # Apply softmax to get probabilities (scores)
        probabilities = logits.softmax(dim=-1).squeeze()

        # Retrieve the labels
        id2label = self.koala_ai_model.config.id2label
        labels = [id2label[idx] for idx in range(len(probabilities))]

        # Combine labels and probabilities, then sort
        label_prob_pairs = list(zip(labels, probabilities))
        label_prob_pairs.sort(key=lambda item: item[1], reverse=True)

        # Print the sorted results
        result = {}
        for label, probability in label_prob_pairs:
            result[label] = f"{probability:.4f}"
        return result
