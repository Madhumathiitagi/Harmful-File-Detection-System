<div align="center">

# 🛡️ Harmful File Detection System
### AI-Powered Malware & Suspicious File Detection Using Machine Learning

<img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python"/>
<img src="https://img.shields.io/badge/Machine%20Learning-LightGBM-orange?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Cybersecurity-AI%20Project-red?style=for-the-badge"/>
<img src="https://img.shields.io/badge/GUI-CustomTkinter-green?style=for-the-badge"/>

---

🚀 Intelligent file scanning system that detects harmful files using  
Machine Learning, PE analysis, and AI-powered threat prediction.

</div>

---

# 📌 Project Overview

The **Harmful File Detection System** is an advanced cybersecurity project designed to identify whether files are **Safe** or **Malicious** using Machine Learning techniques.

The system analyzes executable files by extracting important PE (Portable Executable) features such as:

- File entropy
- Import/export functions
- File structure
- Section information
- Entry point details
- SHA256 hash patterns

These extracted features are processed using a trained **LightGBM Machine Learning Model** to classify files intelligently.

---

# ✨ Features

✅ AI-Powered Harmful File Detection  
✅ Machine Learning-Based Classification  
✅ Beautiful GUI using CustomTkinter  
✅ Real-Time File Scanning  
✅ Probability-Based Detection  
✅ Automatic Quarantine System  
✅ Export Scan Results to CSV  
✅ Retrain Model Support  
✅ Dark / Light Theme Toggle  
✅ PE File Feature Extraction  
✅ EMBER Dataset Integration  
✅ Professional Cybersecurity Workflow  

---

# 🧠 Machine Learning Workflow

```text
File → Feature Extraction → ML Model → Prediction → Quarantine
```

### Detection Pipeline

1. Select Folder
2. Scan Files
3. Extract PE Features
4. Analyze Using LightGBM
5. Predict Harmful or Safe
6. Move Harmful Files to Quarantine
7. Generate Scan Logs & Reports

---

# 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core Development |
| LightGBM | Machine Learning Model |
| Scikit-Learn | Model Training |
| Pandas | Data Processing |
| NumPy | Numerical Operations |
| PEFile | PE Analysis |
| CustomTkinter | Modern GUI |
| Joblib | Model Serialization |
| EMBER Dataset | Malware Dataset |

---

# 📂 Project Structure

```bash
Harmful-File-Detection-System/
│
├── detect_files.py        # File scanning logic
├── train_model.py         # ML model training
├── utils.py               # Feature extraction
├── gui_app.py             # GUI application
├── model.pkl              # Trained model
├── requirements.txt       # Dependencies
├── quarantine/            # Harmful files storage
├── scan_results.csv       # Exported results
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/Harmful-File-Detection-System.git
cd Harmful-File-Detection-System
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Application

## Launch GUI

```bash
python gui_app.py
```

---

# 🧪 Train the ML Model

```bash
python train_model.py
```

---

# 🔍 Scan Files Using CLI

```bash
python detect_files.py <folder_path>
```

Example:

```bash
python detect_files.py sample_files/
```

---

# 📊 Dataset Used

### EMBER Malware Dataset

The project uses the EMBER 2018 dataset for training the malware detection model.

It contains:
- Benign Files
- Malicious Files
- Extracted PE Features
- Real-world malware samples

---

# 🖥️ GUI Preview

### Features Available in GUI

- 📂 Folder Selection
- 🚀 Start Scan
- 📈 Progress Tracking
- 🛡️ Threat Detection
- 📁 Quarantine Access
- 📄 CSV Export
- 🌗 Theme Toggle
- 📊 Scan Statistics

---

# 📈 Model Details

| Model | LightGBM Classifier |
|------|--------------------|
| Type | Binary Classification |
| Objective | Harmful / Safe Detection |
| Dataset | EMBER 2018 |
| Features | PE File Features |
| Output | Prediction + Probability |

---

# 🔐 Security Features

- Quarantine Isolation
- PE Header Analysis
- Entropy-Based Detection
- Import/Export Analysis
- File Metadata Inspection
- Hash-Based Identification

---

# 📸 Sample Output

```text
Processing file 1: malware.exe
Prediction: Harmful (0.98)

Processing file 2: app.exe
Prediction: Safe (0.03)
```

---

# 🚀 Future Enhancements

- Deep Learning Integration
- Real-Time Background Protection
- Cloud Threat Intelligence
- VirusTotal API Support
- Email Alert System
- Web Dashboard
- Live Threat Monitoring
- Multi-threaded Scanning

---

# 👨‍💻 Developed By

## B5 Team — 2025

Cybersecurity & Machine Learning Project

---

# ⭐ Support

If you like this project:

🌟 Star the repository  
🍴 Fork the project  
📢 Share with others  

---

# 📜 License

This project is created for educational and research purposes.

---

<div align="center">

## 🛡️ AI + Cybersecurity + Machine Learning

### Detect • Analyze • Protect

</div>
