
**Prequisites**
- Download MongoDB Community Server - https://www.mongodb.com/try/download/community
- Connect through mongoDB compass.
- Start a database instance at localhost to store forensic artifacts

To get started with this project, follow these steps:

```bash
git clone https://github.com/SherwinAllen/styx.git
```

```bash
cd styx
```

---

**Recommended:**  
Create a Python virtual environment for the backend (for isolation and dependency management):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # On Mac/Linux
# .venv\Scripts\activate       # On Windows
# .venv\Scripts\Activate.ps1   # On Windows PowerShell
```

> **Note:** Always ensure your backend server is running with the virtual environment activated.  
> This ensures all Python scripts use the correct dependencies from `.venv`.

---

Setup node dependencies:

```bash
npm run setup
```

Setup the backend dependencies:

```bash
npm run install:browsers
```
> **Note:** Configure the Environment Variables as shown in ```.env.example```

To start the backend (with the virtual environment activated): 

```bash
node backend/server.js
```

Then, open a new terminal, and launch the frontend using:

```bash
npm start
```


# Tool Description

This tool unifies two distinct IoT forensic workflows—Android-based Smartwatches and Smart Assistant cloud data acquisition—into a single, integrated and practical framework for investigators.

## Smartwatch Module

The Smartwatch module operates using wireless ADB through the standard developer mode, allowing investigators to collect data without the need to root or modify the device. 

It is capable of extracting a wide range of forensic artifacts, including:
- System logs  
- Wireless connection history  
- User account information  
- Sensor data such as GPS, accelerometer, and gyroscope readings  
- The complete file system from the wearable device  

In addition to data extraction, the smartwatch pipeline automatically generates a detailed summary highlighting forensically important findings. Each extracted artifact is accompanied by its computed hash value to ensure data integrity and authenticity.

The acquisition process also retrieves all accessible files from the smartwatch’s file system and integrates them into a content viewer available through the web interface, enabling investigators to conveniently examine file contents.

## Smart Assistant Module

For Smart Assistant devices such as Amazon Alexa or Fire TV Stick remotes, the tool employs a secure, session-cookie–based authentication mechanism to access the user’s Amazon account. 

This automated process retrieves crucial evidence, including:
- Voice transcripts  
- Recorded audio files  
- Timestamps  
- Device identifiers  
- Other associated metadata  

All of this is performed without requiring any manual interaction or browsing.

## Summary

Overall, this framework is designed to minimize manual effort, ensure completeness of evidence acquisition, and enhance scalability for IoT forensics across a wide range of devices and investigations.

