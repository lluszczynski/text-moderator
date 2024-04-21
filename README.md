# Text Moderator MVP

Welcome to Text Moderator MVP! This project aims to provide a simple service for text moderation using a pre-trained model from Hugging Face.

## Features

- **Text Classification**: Classify text into different categories based on predefined criteria.
- **Local Inference**: Perform inference locally, ensuring data privacy and reduced latency.
- **Prometheus Metrics**: Export metrics using Prometheus for monitoring and performance analysis.
- **Grafana Dashboards**: Present metrics using Grafana and Prometheus as datasource. See [the dashboard](./images/grafana-dashboard.png) from the local test.
- **API Endpoint**: Expose an API endpoint for easy integration with other services.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- Docker

### Installation

1. Clone the repository:

```bash
git clone https://github.com/lluszczynski/text-moderator.git
```

2. Navigate to the project directory:

```bash
cd text-moderator
```

3. Build docker image:

```bash
docker-compose build
```

### Usage

1. Run the application:

```bash
docker-compose up 
```

2. Send a POST request to the `/classify` endpoint with a JSON payload containing the text to classify:

```bash
curl -X POST http://localhost:8080/classify -d '{"text": "Sample text for classification"}' -H "Content-Type: application/json"
```

3. Monitor metrics using Grafana:

Visit http://localhost:3000 to access the Grafana dashboard.

### Before going production

Please review [the documentation](PRODUCTION.md) covering the essential considerations to address before proceeding to production.

### Testing

Run the unit tests using the following command:

```bash
pipenv run test
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.