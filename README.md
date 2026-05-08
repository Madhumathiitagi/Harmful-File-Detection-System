# 🛡️ Harmful File Detection System
### AI-Powered Malware & Suspicious File Detection Using Machine Learning

<img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python"/>
<img src="https://img.shields.io/badge/Machine%20Learning-LightGBM-orange?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Cybersecurity-AI%20Project-red?style=for-the-badge"/>
<img src="https://img.shields.io/badge/GUI-CustomTkinter-green?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Web-FastAPI-blue?style=for-the-badge&logo=fastapi"/>
<img src="https://img.shields.io/badge/Frontend-React-cyan?style=for-the-badge&logo=react"/>

---

🚀 Intelligent file scanning system that detects harmful files using  
Machine Learning, PE analysis, and AI-powered threat prediction.

**Now includes Web API and Frontend for complete full-stack experience!**

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

**New Features:**
- 🖥️ **Desktop GUI** - Modern Tkinter interface
- 🌐 **Web API** - FastAPI backend for HTTP scanning
- 💻 **Web Frontend** - React-based file upload interface

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
✅ **Web API with FastAPI**  
✅ **React Web Frontend**  
✅ **Full-Stack File Scanning**

---

# 🧠 Machine Learning Workflow

```text
File → Feature Extraction → ML Model → Prediction → Quarantine
```

### Detection Pipeline

1. Select Folder (Desktop) or Upload File (Web)
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
| **FastAPI** | **Web API Framework** |
| **React** | **Web Frontend** |
| **Vite** | **Frontend Build Tool** |
| Joblib | Model Serialization |
| EMBER Dataset | Malware Dataset |

---

# 📂 Project Structure

```bash
Harmful-File-Detection-System/
│
├── backend/               # 🆕 FastAPI Web API
│   ├── main.py           # API endpoints
│   ├── requirements.txt  # Backend dependencies
│   ├── utils.py          # Feature extraction
│   ├── model.pkl         # Trained ML model
│   └── uploads/          # File upload directory
│
├── frontend/              # 🆕 React Web App
│   ├── src/
│   │   ├── App.jsx       # Main React component
│   │   └── index.css     # Styling
│   ├── package.json      # Frontend dependencies
│   ├── vite.config.js    # Vite configuration
│   └── index.html        # HTML template
│
├── check_labels.py/       # Desktop Python App
│   ├── detect_files.py   # File scanning logic
│   ├── train_model.py    # ML model training
│   ├── utils.py          # Feature extraction
│   ├── gui_app.py        # Original GUI
│   ├── gui_app_modern.py # Modernized GUI
│   ├── model.pkl         # Trained model
│   ├── requirements.txt  # Dependencies
│   ├── quarantine/       # Harmful files storage
│   └── scan_results.csv  # Exported results
│
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Madhumathiitagi/Harmful-File-Detection-System.git
cd Harmful-File-Detection-System
```

---

## 2️⃣ Install Dependencies

### Desktop App
```bash
cd check_labels.py
pip install -r requirements.txt
```

### Web Backend
```bash
cd ../backend
pip install -r requirements.txt
```

### Web Frontend
```bash
cd ../frontend
npm install
```

---

# ▶️ Run Application

## Desktop GUI

```bash
cd check_labels.py
python gui_app_modern.py
```

## Web Application

### Start Backend API
```bash
cd backend
python main.py
```
API will run on http://localhost:8000

### Start Frontend
```bash
cd frontend
npm run dev
```
Frontend will run on http://localhost:3000

---

# 🧪 Train the ML Model

```bash
cd check_labels.py
python train_model.py
```

---

# 🔍 Scan Files

## Desktop CLI
```bash
cd check_labels.py
python detect_files.py <folder_path>
```

Example:
```bash
python detect_files.py sample_files/
```

## Web API
Use the web interface at http://localhost:3000 or send POST requests to `/scan`

---

# 🌐 Web API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/scan` | Upload and scan a file |
| GET | `/results` | Get list of quarantined files |

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

### Desktop Features
- 📂 Folder Selection
- 🚀 Start Scan
- 📈 Progress Tracking
- 🛡️ Threat Detection
- 📁 Quarantine Access
- 📄 CSV Export
- 🌗 Theme Toggle
- 📊 Scan Statistics

### Web Features
- 📤 File Upload Interface
- 🔍 Real-time Scanning
- 📊 Result Display
- 🛡️ Automatic Quarantine
- 📱 Responsive Design

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
- Web Upload Security
- API Rate Limiting

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
- Advanced Web Dashboard
- Live Threat Monitoring
- Multi-threaded Scanning
- Mobile App
- Docker Containerization

---

# 👨‍💻 Developed By

## B5 Team — 2025

Cybersecurity & Machine Learning Project  
Full-Stack Development with AI Integration

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

## 🛡️ AI + Cybersecurity + Machine Learning + Full-Stack

### Detect • Analyze • Protect • Deploy

</div>

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

## 🛡️ AI + Cybersecurity + Machine Learning + Full-Stack

### Detect • Analyze • Protect • Deploy

</div>
