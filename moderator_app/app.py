import logging
import time

from flask import Flask, jsonify, request
from prometheus_client import Histogram
from prometheus_flask_exporter import PrometheusMetrics

from moderator_app.model import KoalaAiTextModerator

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Activate metrics export
metrics = PrometheusMetrics(app)
classify_duration_histogram = Histogram('classify_duration_seconds', 'Classification duration in seconds')

# Initialize the TextModerator model
text_moderator = KoalaAiTextModerator()


@app.get("/")
def home():
    return "Welcome to Text Moderator!"


@app.post('/classify')
def classify_text():
    start_time = time.time()
    data = request.get_json()
    text = data.get('text')
    logger.debug("Received classification request for text: %s", text)
    if text is None:
        return jsonify({'error': 'No text provided'}), 400

    scores = text_moderator.run_inference(text)
    duration = time.time() - start_time
    logger.debug("Inference completed in %f seconds", duration)

    classify_duration_histogram.observe(duration)
    return jsonify({'scores': scores, 'duration_seconds': duration})


# register additional default metrics
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080)
