# Introduction 
A simple, educational honeypot written in Python with a graphical user interface (GUI). This project demonstrates how honeypots work by listening on a specified port, logging connection attempts, and displaying activity in real-time.

## Project structure 
```text
Honeypot/
├── src/                   
│   ├── honeypot_logger.py
│   ├── honeypot_functions.py
│   ├── honeypot_gui.py
│   └── honeypot_main.py
├── logs/                                      
├── README.md
└── requirements.txt
```
# Quick start
```text
# clone the repo
git clone https://github.com/Prabesh-collab/Honeypot.git 
cd Honeypot

# install the requirements
 pip install -r requirements.txt

# run the application
python honeypot_main.py
```

# Features 
1. TCP Port listner 
2. connection Logging
3. Fake Service Banners 
4. Real-time GUI
5. Multi-threaded
6. Start/Stop control 


# legal Disclamer 
WARNING: This project is for educational purposes only.

Only run this honeypot on systems you own or have explicit permission to test
Running a honeypot on a public network may violate laws or regulations in your jurisdiction
This is a basic demonstration and not a production-ready honeypot
The authors are not responsible for any misuse or damage caused by this software
