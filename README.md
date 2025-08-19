# <img src="frontend/public/favicon.svg" alt="Favicon" width="30"/> **PM ACCELERATOR - WEATHER APP**
---
App is live at: https://pm-accelerator-weather-app-ram.netlify.app
<p align="center">
  <img src="assets/Screenshot 2025-08-20 003616.png" alt="Screenshot 1" width="49%">
  <img src="assets/Screenshot 2025-08-20 003727.png" alt="Screenshot 2" width="49%">
</p>

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
│   │   ├── main.py               # FastAPI entry, mounts routers, CORS
│   │   ├── routes/
│   │   │   ├── weather.py        # Current, forecast, history CRUD APIs
│   │   │   ├── locations.py      # Search locations
│   │   │   ├── export.py         # Export history (CSV, JSON, XML, PDF)
│   │   │   ├── youtube.py        # Fetch YouTube videos
│   │   │   └── maps.py           # Static maps (coords & city)
│   │   ├── services/
│   │   │   ├── weather_service.py  # Wrapper around OWM API
│   │   │   ├── youtube_service.py  # Wrapper around YouTube API
│   │   │   └── map_service.py      # Static map generation
│   │   ├── utils/
│   │   │   ├── exporters.py        # CSV/JSON/XML/PDF export helpers
│   │   │   └── db.py               # SQLite history storage
│   │   └── __init__.py
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── public/
│   │   ├── favicon.svg
│   │   └── index.html
│   ├── src/
│   │   ├── api/
│   │   │   └── axios.js          # Centralized axios instance
│   │   ├── store/
│   │   │   └── lastSearch.js     # Zustand store for persisting last search
│   │   ├── components/
│   │   │   ├── SearchBar.jsx     # Input for city search
│   │   │   ├── WeatherCard.jsx   # Display current weather
│   │   │   ├── ForecastCard.jsx  # Display forecast
│   │   │   ├── MapView.jsx       # Static map rendering
│   │   │   └── VideoGallery.jsx  # YouTube video embedding
│   │   ├── App.jsx               # Main layout + routing
│   │   ├── main.jsx              # React root
│   │   └── index.css             # Tailwind base styles
│   ├── package.json
│   └── ...
│
├── assets/
│   ├── homepage.png
│   ├── swagger.png
│   └── search.png
│
└── README.md
```
---

## **Functionalities by Module**

| **Script**                         | **Purpose**                                         |
| ---------------------------------- | --------------------------------------------------- |
| `backend/app/main.py`              | Starts FastAPI app, configures middleware + routers |
| `backend/app/routes/weather.py`    | Current weather, forecast, CRUD for history         |
| `backend/app/routes/locations.py`  | Search locations by name                            |
| `backend/app/routes/export.py`     | Export search history in CSV/JSON/XML/PDF           |
| `backend/app/routes/youtube.py`    | Fetch YouTube videos for a city                     |
| `backend/app/routes/maps.py`       | Get static maps by city or coords                   |
| `backend/app/utils/exporters.py`   | Handles export formatting                           |
| `backend/app/utils/db.py`          | SQLite + ORM wrapper for search history             |
| `frontend/src/store/lastSearch.js` | Persists last search across navigation + refresh    |
| `frontend/src/api/axios.js`        | Central API call config using `VITE_API_BASE`       |
| `frontend/src/components/*.jsx`    | Modular UI components (weather, maps, videos)       |
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
* Swagger UI
  <p align="center">
  <img src="assets/Screenshot 2025-08-20 004148.png" alt="Screenshot 1" width="99%">
  </p>


## **API Endpoints**

### **Weather**

| Method | Endpoint                  | Purpose         |
| ------ | ------------------------- | --------------- |
| POST   | `/weather/current`        | Current weather |
| POST   | `/weather/forecast`       | Forecast        |
| POST   | `/weather/history`        | Add record      |
| GET    | `/weather/history`        | Get history     |
| GET    | `/weather/history/search` | Search history  |
| PUT    | `/weather/history/{id}`   | Update record   |
| DELETE | `/weather/history/{id}`   | Delete record   |

### **Locations**

| Method | Endpoint            | Purpose               |
| ------ | ------------------- | --------------------- |
| POST   | `/locations/search` | Search city locations |

### **Export**

| Method | Endpoint       | Purpose     |
| ------ | -------------- | ----------- |
| GET    | `/export/csv`  | Export CSV  |
| GET    | `/export/json` | Export JSON |
| GET    | `/export/xml`  | Export XML  |
| GET    | `/export/pdf`  | Export PDF  |

### **Maps**

| Method | Endpoint                | Purpose                   |
| ------ | ----------------------- | ------------------------- |
| GET    | `/maps/by-coords`       | Static map by coordinates |
| GET    | `/maps/by-coords/image` | Static map image          |
| GET    | `/maps/{location}`      | Static map by city        |

### **YouTube**

| Method | Endpoint              | Purpose                     |
| ------ | --------------------- | --------------------------- |
| GET    | `/youtube/{location}` | YouTube videos for location |

### **Health**

| Method | Endpoint | Purpose          |
| ------ | -------- | ---------------- |
| GET    | `/`      | API Health check |

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
