from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import pandas as pd
import joblib
from utils import extract_features
from pathlib import Path

app = FastAPI(title="Harmful File Detector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
MODEL_PATH = Path(__file__).parent / "model.pkl"
if not MODEL_PATH.exists():
    raise FileNotFoundError("Model not found. Please train the model first.")

artifact = joblib.load(MODEL_PATH)
if isinstance(artifact, dict) and 'model' in artifact and 'columns' in artifact:
    model = artifact['model']
    trained_columns = artifact['columns']
else:
    model = artifact
    trained_columns = None

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

QUARANTINE_DIR = UPLOAD_DIR / "quarantine"
QUARANTINE_DIR.mkdir(exist_ok=True)

@app.post("/scan")
async def scan_file(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract features
        features = extract_features(str(file_path))
        df = pd.DataFrame([features])

        if 'file_extension' in df.columns:
            df = pd.get_dummies(df, columns=['file_extension'])

        df = df.fillna(0)

        if trained_columns is not None:
            df = df.reindex(columns=trained_columns, fill_value=0)
        else:
            expected = getattr(model, "n_features_in_", None)
            if expected and df.shape[1] < expected:
                for i in range(expected - df.shape[1]):
                    df[f'extra_{i}'] = 0
            if expected and df.shape[1] > expected:
                df = df.iloc[:, :expected]

        df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

        prediction = model.predict(df)[0]

        probability = 0.0
        try:
            proba = model.predict_proba(df)[0]
            classes = list(model.classes_)
            if 1 in classes:
                idx = classes.index(1)
                probability = float(proba[idx])
            else:
                probability = float(max(proba))
        except Exception:
            pass

        result = {
            'filename': file.filename,
            'prediction': 'Harmful' if int(prediction) == 1 else 'Safe',
            'probability': probability
        }

        if int(prediction) == 1:
            # Move to quarantine
            quarantine_path = QUARANTINE_DIR / file.filename
            shutil.move(file_path, quarantine_path)
            result['status'] = 'Quarantined'
        else:
            # Remove uploaded file
            os.remove(file_path)
            result['status'] = 'Safe'

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results")
async def get_results():
    # Return list of quarantined files
    quarantined = []
    for f in QUARANTINE_DIR.iterdir():
        if f.is_file():
            quarantined.append(f.name)
    return {"quarantined": quarantined}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)