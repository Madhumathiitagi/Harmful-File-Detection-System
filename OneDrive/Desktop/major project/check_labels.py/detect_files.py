import os
import pandas as pd
import joblib
from utils import extract_features


def detect_files(folder_path, model_path='model.pkl'):
    """Scan folder using the EMBER-trained LightGBM model (2381 features)."""

    # Load model
    print("Loading model...")
    model = joblib.load(model_path)
    print("Model loaded!")

    results = []
    file_count = 0

    for root, dirs, files in os.walk(folder_path):

        for file in files:
            file_path = os.path.join(root, file)
            file_count += 1
            print(f"Processing file {file_count}: {file_path}")

            try:
                # ---- 1. Extract EMBER features (must output 2381 features) ----
                features = extract_features(file_path)

                if features is None:
                    raise Exception("Feature extraction failed")

                # ---- 2. Put into DataFrame ----
                df = pd.DataFrame([features])

                # MUST match LightGBM model input length
                expected = model.n_features_in_
                if df.shape[1] != expected:
                    raise ValueError(
                        f"Feature mismatch! Got {df.shape[1]}, expected {expected}"
                    )

                # ---- 3. Predict ----
                pred = model.predict(df)[0]

                proba = model.predict_proba(df)[0][1]  # probability of class 1

                status = "Harmful" if pred == 1 else "Safe"

                results.append({
                    "file": file_path,
                    "prediction": status,
                    "probability": float(proba)
                })

            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                results.append({
                    "file": file_path,
                    "prediction": "Error",
                    "probability": 0.0,
                    "status": f"Error: {str(e)}"
                })

    print("\n--- SCAN COMPLETE ---")
    for r in results:
        print(f"{r['file']} → {r['prediction']} ({r['probability']:.2f})")

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detect_files.py <folder_path> [model_path]")
        sys.exit(1)

    folder_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) > 2 else "model.pkl"

    detect_files(folder_path, model_path)
