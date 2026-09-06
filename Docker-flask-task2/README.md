# Dockerized Flask App

## 1. Run locally without Docker (optional sanity check)
```bash
pip install -r requirements.txt
python app.py
# visit http://localhost:5000
```

## 2. Build the Docker image
```bash
cd task4-docker-flask
docker build -t flask-demo .
```

## 3. Run the container
```bash
docker run -p 5000:5000 flask-demo
```
Open `http://localhost:5000` in your browser — you should see the HTML page,
and `http://localhost:5000/api/status` should return JSON.

If port 5000 is already taken on your machine, map to a different host port:
```bash
docker run -p 8080:5000 flask-demo
```

## 4. (Bonus) Push to Docker Hub
```bash
docker login
docker tag flask-demo <your-dockerhub-username>/flask-demo:latest
docker push <your-dockerhub-username>/flask-demo:latest
```
Anyone can now run it with:
```bash
docker run -p 5000:5000 <your-dockerhub-username>/flask-demo:latest
```

## Troubleshooting
- **"port already allocated"** — another process is using 5000; use `-p 8080:5000` instead.
- **Build fails on pip install** — check your internet connection; Docker needs to reach PyPI during build.
- **Blank page in browser** — confirm the container is actually running with `docker ps`, and check logs with `docker logs <container_id>`.
