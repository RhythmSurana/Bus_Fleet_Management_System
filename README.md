# 🚌 Bus Fleet Management System

A Full-Stack Web Application for Real-Time Bus Monitoring, Fleet Management, and Role-Based Dashboard Control.

This system enables transport authorities, drivers, and passengers to interact with a centralized platform for managing buses, tracking live locations, and monitoring fleet performance.

---

## 🚀 Features

### 🔐 Authentication & Authorization
- JWT-based secure authentication
- Role-based access control
- Separate dashboards for:
  - Authority
  - Driver
  - Passenger

### 🗺 Real-Time Bus Tracking
- Live bus location simulation
- Interactive maps using Leaflet.js
- Dynamic marker updates

### 📊 Authority Dashboard
- View total buses
- Monitor active routes
- Track fleet status
- Manage system-level insights

### 🧑‍✈️ Driver Dashboard
- View assigned bus details
- Route tracking
- Live status updates

### 🧑‍💼 Passenger Dashboard
- View available buses
- Track live bus positions
- Route information

---

## 🛠 Tech Stack

### 🔹 Backend
- Python
- Flask
- Flask-JWT-Extended
- REST API Architecture

### 🔹 Frontend
- React (CDN-based)
- Tailwind CSS
- Leaflet.js (Maps)
- Vanilla JavaScript (No build tools)

---

## 📂 Project Structure

```
Bus_Fleet_Management_System/
│
├── app.py                # Flask backend server
├── new.html              # Frontend (React + Tailwind)
├── requirements.txt      # Python dependencies
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/RhythmSurana/Bus_Fleet_Management_System.git
cd Bus_Fleet_Management_System
```

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the Flask Server

```bash
python app.py
```

Server will start at:

```
http://127.0.0.1:5000/
```

---

## 🔑 Authentication Flow

1. User selects role (Authority / Driver / Passenger)
2. Logs in
3. JWT token is generated
4. Token stored in localStorage
5. Protected routes accessed via Authorization headers

---

## 🌍 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | Authenticate user |
| GET | `/buses` | Fetch bus data |
| GET | `/routes` | Fetch route data |
| GET | `/stats` | Fetch dashboard stats |

---

## 📈 Future Improvements

- Convert to full React project (Vite/CRA)
- Use PostgreSQL/MySQL database
- Deploy backend & frontend separately
- Add WebSocket for real-time updates
- Add Admin CRUD operations
- Implement production-level error handling

---

## 🏆 Use Case

This project was built as a real-world simulation for:
- Smart City Transport Systems
- Fleet Management Solutions
- Hackathon Projects
- College Capstone Projects

---

## 👨‍💻 Author

**Rhythm Surana Jain**

- Electronics & Instrumentation Engineering
- Full-Stack Developer
- AI/ML Enthusiast
- Public Relations Head – E-Cell IET DAVV

---

## ⭐ If You Like This Project

Give it a star on GitHub and feel free to fork it!
