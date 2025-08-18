
# <img src="frontend/public/favicon.svg" alt="Favicon" width="30"/> **PM ACCELERATOR - WEATHER APP**

---

## **Problem Statement - Technical Assignment**

Most weather applications only show basic temperature and conditions. My goal was to create an **integrated weather intelligence app** that not only fetches weather data but also:
- Displays weather maps with zoom-level controls.
- Embeds related YouTube content dynamically.
- Provides a **search history feature** that persists across navigation.
- Offers an easy-to-use **API layer with Swagger UI** for developers.

This makes the app both a **consumer-facing product** and a **developer tool**.

---

## **Tech Stack**

### **Frontend**
- React (Vite)
- Axios for API requests
- TailwindCSS for styling
- Deployed on **Netlify**

### **Backend**
- Python 3.11.5 + FastAPI
- Uvicorn (ASGI server)
- Geopy & GeographicLib for geocoding
- Google API Python Client for YouTube data
- Deployed on **Render**

---

## **Basic Product Flow**

1. **User Interaction**
   - User searches a city from the frontend.
   - Weather and video data are displayed.
   - History persists even after navigation.

2. **Frontend Flow**
   - `axios` calls → `import.meta.env.VITE_API_BASE` → backend API.
   - Displays weather map + thumbnails in a scrollable container.
   - State management ensures home retains last search.

3. **Backend Flow**
   - FastAPI routes handle requests.
   - Weather API + Geopy resolve lat/lon.
   - YouTube API fetches related videos.
   - JSON response returned to frontend.

4. **Swagger UI**
   - Available at `/docs`.
   - Lets developers test endpoints directly.

---

## **Code Structure**

```

pm-accelerator-weather-app/
│
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI entry point
│   │   ├── routes.py        # API route definitions
│   │   ├── services/        # Weather + YouTube logic
│   │   └── utils/           # Helper utilities
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── public/
│   │   ├── favicon.svg
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── api.js
│   ├── package.json
│   └── ...
│
├── assets/                  # Screenshots for README
│   ├── homepage.png
│   ├── swagger.png
│   └── search.png
│
└── README.md

````

---

## **Setup Instructions**

### **1. Clone Repo**
```bash
git clone https://github.com/RamakrishnaReddyPalle/pm-accelerator-weather-app.git
cd pm-accelerator-weather-app
````

---

### **2. Backend Setup (FastAPI)**

#### **Create Virtual Environment**

```bash
cd backend
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

#### **Install Requirements**

```bash
pip install -r requirements.txt
```

#### **Run Uvicorn**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### **Check Local**

* API Base: `http://127.0.0.1:8000`
* Swagger: `http://127.0.0.1:8000/docs`

---

### **3. Frontend Setup (React + Vite)**

```bash
cd frontend
npm install
npm run dev
```

Open: `http://localhost:5173`

---

### **4. Split-Terminal Workflow**

**Terminal 1 (Backend)**:

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 (Frontend)**:

```bash
cd frontend
npm run dev
```

---

## **Deployment Instructions**

### **Backend (Render)**

* Root directory: `backend/`
* Build command: `pip install -r requirements.txt`
* Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
* Auto-deploy on main branch.

### **Frontend (Netlify)**

* Base directory: `frontend/`
* Build command: `npm run build`
* Publish directory: `frontend/dist`
* Environment variable:

  ```env
  VITE_API_BASE=https://pm-accelerator-weather-app.onrender.com
  ```

---

## **Swagger UI**

* Endpoint: `/docs`
* Example Screenshot:
  ![Swagger UI](assets/swagger.png)

---

## **API Routes**

| Route      | Method | Purpose                                                   |
| ---------- | ------ | --------------------------------------------------------- |
| `/`        | GET    | Health check                                              |
| `/weather` | GET    | Fetch weather data for a city (lat/lon, temp, conditions) |
| `/map`     | GET    | Fetch weather map tile for given lat/lon                  |
| `/youtube` | GET    | Fetch YouTube videos related to city & weather            |
| `/history` | GET    | Retrieve search history                                   |
| `/history` | POST   | Add a city search to history                              |

---

## **Additional Notes**

* **Python version**: 3.11.5

* **Node.js version**: >=18.x

* **Environment Variables** (backend):

  * `GOOGLE_API_KEY`
  * `WEATHER_API_KEY`

* **Backend Testing**:

  ```bash
  pytest
  ```

* **Frontend Build**:

  ```bash
  npm run build
  npm run preview
  ```

---

## **Acknowledgments**

* [FastAPI Docs](https://fastapi.tiangolo.com/)
* [Netlify Docs](https://docs.netlify.com/)
* [Render Docs](https://render.com/docs)
* [YouTube Data API](https://developers.google.com/youtube/v3)
* [OpenWeatherMap API](https://openweathermap.org/api)

