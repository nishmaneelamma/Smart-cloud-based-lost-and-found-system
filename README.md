# Smart Lost & Found System
Cloud Computing Project — Event-driven Microservices on Docker

## Architecture
5 Docker containers communicating via Redis Pub/Sub:

- **Redis**         — message broker (pub/sub channels)
- **item-service**  — VM2: REST API to report lost/found items (Flask + SQLite)
- **match-service** — VM3: worker that detects matches between items
- **notify-service**— VM4: worker that logs alerts when a match is found
- **dashboard**     — VM5: web UI showing all items and match notifications

## How to Run

### Prerequisites
- Docker Desktop installed and running

### Start the project
```bash
docker compose up --build
```

Open your browser: http://localhost:8888

### Stop the project
```bash
docker compose down
```

## Demo Flow (for viva)

Open two terminal windows.

**Terminal 1** — watch live logs:
```bash
docker compose logs -f
```

**Terminal 2** — trigger a match:
```bash
# Step 1: Report a found wallet
curl -X POST http://localhost:5001/items \
  -H "Content-Type: application/json" \
  -d '{"type":"found","name":"Black wallet","category":"wallet","location":"Cafeteria","date":"2026-04-09","contact":"finder@uni.edu"}'

# Step 2: Report a lost wallet — triggers the match!
curl -X POST http://localhost:5001/items \
  -H "Content-Type: application/json" \
  -d '{"type":"lost","name":"My wallet","category":"wallet","location":"Campus","date":"2026-04-09","contact":"owner@uni.edu"}'
```

Watch Terminal 1 for:
- `[MATCH] MATCH FOUND: "My wallet" <-> "Black wallet"`
- `[NOTIFY] *** MATCH ALERT — NOTIFYING BOTH PARTIES ***`

And the dashboard at http://localhost:8888 auto-refreshes every 3 seconds to show the match.

## Project Structure
```
lost-and-found/
├── docker-compose.yml
├── data/                        <- SQLite database (auto-created)
├── item-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py                   <- Flask REST API
├── match-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── worker.py                <- Redis subscriber, finds matches
├── notify-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── worker.py                <- Redis subscriber, fires alerts
└── dashboard/
    ├── Dockerfile
    ├── requirements.txt
    ├── app.py                   <- Flask web server
    └── templates/
        └── index.html           <- UI with auto-refresh
```

## Patterns Demonstrated
- Microservices
- Event-driven architecture
- Pub/Sub messaging (Redis)
- Work queue pattern
- Containerisation with Docker
