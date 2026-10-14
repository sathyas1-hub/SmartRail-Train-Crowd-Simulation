# SmartRail — Local Train Tracking & Compartment Crowd Simulation

An interactive Streamlit simulation for the Smart Local Train Tracking and Compartment Crowd Monitoring System.

## Features
- Train journey progress visual and demo ETA
- Four compartments with adjustable demo passenger counts
- Low / Medium / High crowd classification
- Least-crowded-compartment recommendation
- Normal weekday, peak-hour, festival and balanced scenarios
- Downloadable crowd table as CSV
- Clear distinction between simulated values and future hardware integration

## Run locally
Install Python 3.10 or newer. In this folder run:

```bash
python -m venv .venv
```

Windows PowerShell activation:
```powershell
.\.venv\Scripts\Activate.ps1
```

Install and run:
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local address shown in the terminal (usually http://localhost:8501).

## Deploy on Render later
1. Extract this ZIP.
2. Upload the files to a GitHub repository.
3. In Render, choose New + → Web Service and connect the repository.
4. Use build command `pip install -r requirements.txt`.
5. Use start command `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`.
6. Deploy and open the generated public URL.

The included `render.yaml` contains the service configuration.

## Important limitation
This is a model simulation. Train route, progress, ETA and coach passenger counts are demo values. It is not connected to Indian Railways, live GPS, ESP32-CAM or a real passenger-counting system. Do not present the outputs as measured results.

## Planned hardware integration
- NEO-6M GPS requires a suitable serial/USB adapter or a microcontroller serial bridge and a valid GPS fix.
- ESP32-CAM should first be tested for camera streaming; automated counting needs a separate validated computer-vision approach.
- Public camera use requires attention to consent, privacy, data retention and railway approval.
