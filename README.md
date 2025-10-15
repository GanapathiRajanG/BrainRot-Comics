# BrainROT Comics - AI Story Generator

A Flask web application that generates imaginative stories using machine learning and AI techniques.

## Features

## Features

- AI-powered story generation based on user prompts
- Multiple genre options (Fantasy, Sci-Fi, Mystery, etc.)
- Adjustable story length
- Example prompts for inspiration
- Copy-to-clipboard functionality
- Responsive UI

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd "BrainROT Comics"
```

2. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

Note: TensorFlow is optional and large. The app will run without it and use a rule-based generator.

## Running locally

Start the app:

```powershell
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## TensorFlow / ML model notes

- If TensorFlow is not installed, the app will skip ML model loading and training and fall back to a rule-based generator (fast and lightweight).
- To enable ML features, install TensorFlow compatible with your Python version and OS. After installing TensorFlow, you can either provide a trained model at `model/trained_model/story_model.h5` or trigger training via the `/train_model` endpoint (training runs only if TensorFlow is available).

## Troubleshooting

- If static assets (CSS/JS) 404, ensure the `static` folder exists and contains `css/styles.css` and `js/script.js`.
- If you get import errors for heavy packages like TensorFlow, either install them or rely on the rule-based generator.

## License

This project is provided as-is for educational/demo purposes.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd brainrot-comics