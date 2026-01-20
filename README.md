# Railway Quest

Railway Quest is a structured FastAPI backend project that simulates a mini railway system.
It demonstrates clean backend architecture, graph algorithms, and REST API design.

The project includes station discovery, cheapest-route calculation, trip scheduling,
and ticket booking functionality. It is suitable for learning, interviews, and portfolio use.

---

## Project Overview

Railway Quest models a railway network as a weighted graph.
Stations are nodes, tracks are edges, and routing is computed using Dijkstra’s algorithm.

The system is intentionally kept modular so that in-memory data can later be replaced
with a real database, authentication, or external services.

---

## Features

<table>
<tr><th>Feature</th><th>Description</th></tr>
<tr><td>Stations API</td><td>List all available railway stations</td></tr>
<tr><td>Route Finder</td><td>Find cheapest route between two stations using Dijkstra</td></tr>
<tr><td>Trips API</td><td>View upcoming train trips</td></tr>
<tr><td>Bookings API</td><td>Create and list ticket bookings</td></tr>
<tr><td>Clean Architecture</td><td>Clear separation of API, services, data, and models</td></tr>
<tr><td>Swagger UI</td><td>Interactive API documentation</td></tr>
<tr><td>Testing</td><td>Basic automated tests using pytest</td></tr>
</table>

---

## Architecture

The application follows a layered architecture:

<pre>
API Layer        -> HTTP endpoints (FastAPI routers)
Service Layer    -> Business logic (routing, booking)
Data Layer       -> Graph + seed data
Model Layer      -> Pydantic schemas
</pre>

This design improves testability, readability, and extensibility.

---

## Project Structure

<pre>
Railway/
├── requirements.txt
├── run.sh
├── README.md
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes/
│   │       ├── health.py
│   │       ├── stations.py
│   │       ├── routing.py
│   │       ├── trips.py
│   │       └── bookings.py
│   ├── core/
│   │   └── config.py
│   ├── data/
│   │   ├── network.py
│   │   └── seed.py
│   ├── models/
│   │   └── schemas.py
│   └── services/
│       ├── routing_service.py
│       └── booking_service.py
└── tests/
    └── test_routing.py
</pre>

---

## Tech Stack

<table>
<tr><th>Technology</th><th>Purpose</th></tr>
<tr><td>Python 3.10+</td><td>Programming language</td></tr>
<tr><td>FastAPI</td><td>Web framework</td></tr>
<tr><td>Pydantic</td><td>Data validation and schemas</td></tr>
<tr><td>Uvicorn</td><td>ASGI server</td></tr>
<tr><td>Pytest</td><td>Testing framework</td></tr>
</table>

---

## Installation & Setup

### 1. Clone the Repository

<pre>
git clone https://github.com/gupta-8/Railway.git
cd Railway
</pre>

### 2. Run the Application

<pre>
bash run.sh
</pre>

This script:
- Creates a virtual environment
- Installs dependencies
- Starts the FastAPI server

### 3. Open API Documentation

<pre>
http://127.0.0.1:8000/docs
</pre>

---

## How to Use

### List Stations

<pre>
GET /stations
</pre>

### Find Cheapest Route

<pre>
GET /route?from_station=NDLS&to_station=BPL
</pre>

### List Trips

<pre>
GET /trips
</pre>

### Create Booking

<pre>
POST /bookings
Content-Type: application/json

{
  "passenger_name": "Harsh",
  "trip_id": "T1002",
  "seats": 2
}
</pre>

### List Bookings

<pre>
GET /bookings
</pre>

---

## API Reference

<table>
<tr><th>Method</th><th>Endpoint</th><th>Description</th></tr>
<tr><td>GET</td><td>/health</td><td>Service health check</td></tr>
<tr><td>GET</td><td>/stations</td><td>List all stations</td></tr>
<tr><td>GET</td><td>/route</td><td>Find cheapest route</td></tr>
<tr><td>GET</td><td>/trips</td><td>List upcoming trips</td></tr>
<tr><td>POST</td><td>/bookings</td><td>Create a booking</td></tr>
<tr><td>GET</td><td>/bookings</td><td>List all bookings</td></tr>
</table>

---

## Configuration

Configuration is defined in:

<pre>
app/core/config.py
</pre>

Example:

<pre>
fare_per_km = 2
</pre>

This can be extended for dynamic pricing or multiple travel classes.

---

## Testing

Run tests using:

<pre>
source .venv/bin/activate
pytest -q
</pre>

Current tests validate:
- Route calculation correctness
- Invalid station handling

---

## Future Improvements

- Persistent database (SQLite / PostgreSQL)
- Authentication and authorization
- Seat availability management
- Payment gateway simulation
- Admin dashboard
- Frontend UI (React or Next.js)
- Docker and CI/CD support
