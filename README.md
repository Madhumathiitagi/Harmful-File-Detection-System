# Harmful File Detection System

A comprehensive malware detection system with desktop GUI, web API, and web frontend.

## Features

- **Machine Learning Detection**: Uses RandomForest classifier trained on EMBER dataset
- **Desktop GUI**: Modern Tkinter-based interface with scanning and quarantine features
- **Web API**: FastAPI backend for file scanning via HTTP
- **Web Frontend**: React-based web interface for uploading and scanning files
- **Quarantine System**: Automatically moves detected malware to quarantine folders

## Project Structure

```
major project/
├── backend/          # FastAPI server
│   ├── main.py       # API endpoints
│   ├── requirements.txt
│   ├── utils.py      # Feature extraction
│   └── model.pkl     # Trained ML model
├── frontend/         # React web app
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── check_labels.py/  # Desktop Python app
    ├── gui_app.py    # Original GUI
    ├── gui_app_modern.py # Modernized GUI
    ├── train_model.py
    ├── detect_files.py
    └── utils.py
```

## Setup

### Desktop App

1. Navigate to `check_labels.py/`
2. Install dependencies: `pip install -r requirements.txt`
3. Run GUI: `python gui_app_modern.py`

### Web App

1. **Backend**:
   - Navigate to `backend/`
   - Install: `pip install -r requirements.txt`
   - Run: `python main.py`

2. **Frontend**:
   - Navigate to `frontend/`
   - Install: `npm install`
   - Run: `npm run dev`

3. Open http://localhost:3000

## Usage

### Desktop
- Select folder to scan
- Click "Start Scan"
- View results and quarantine harmful files

### Web
- Upload files via the web interface
- View scan results
- Files are automatically quarantined if harmful

## Training

To retrain the model:
```bash
cd check_labels.py
python train_model.py
```

## API Endpoints

- `POST /scan`: Upload and scan a file
- `GET /results`: Get list of quarantined files

## Technologies

- Python, Scikit-learn, FastAPI, React, Vite, CustomTkinter

## License

MIT