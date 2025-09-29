# Pipelines Perceptual Evaluation

This repository contains a Flask-based web application for conducting multimodal perceptual evaluations, specifically for comparing video stimuli using MUSHRA and AB testing methodologies.

## Project Structure
- **app.py**: Main Flask application handling session management, experiment flow, and result storage in local CSV files.
- **config/**: Contains experiment configuration (`experiment.py`).
- **data/**: Stores video files for evaluation (not tracked in Git).
- **results/**: Stores participant results as CSV files (not tracked in Git).
- **sessionlogs/**: Stores session logs as JSON files (not tracked in Git).
- **styles/**: CSS styles for the web interface.
- **templates/**: HTML templates for the experiment pages.
- **figs/**: Example images for MUSHRA and AB interfaces.

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Multimodal-Perceptual-Evaluation
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure the `data/` directory contains the required video files in subfolders (`llm`, `llm_DiT`, `ref_high`, `ref_low`).
4. Run the application:
   ```bash
   python app.py
   ```
5. Access the experiment at `http://localhost:5000`.

## Requirements
- Python 3.x
- Flask
- Pandas
- NumPy

See `requirements.txt` for a complete list.

## Usage
- The application presents an initial page (`index.html`) to start a new session.
- Participants complete MUSHRA and AB tests as configured in `config/experiment.py`.
- Results are saved locally in the `results/` directory as CSV files.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
   cd Pipelines-Perceptual-Evaluation