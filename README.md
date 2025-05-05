# CI/CD practice
Simple Flask API app using CI/CD (GitHub Actions), Docker.

Usage:
## Running via app.py
Installing requirements: 
```bash
pip install -r requirements.txt
```
Running app:
```bash
python app.py
```
Testing:
```bash
pytest tests/ -v --cov=app --cov-report=xml
```

## Building and Running Docker Image
To build the Docker image:
```bash
docker build -t myapp:latest .
```
To run the Docker container:
```bash
docker run -p 5000:5000 myapp:latest
```
Access the API at http://localhost:5000/books



Result:
![image](https://github.com/user-attachments/assets/ddf6fcf7-436b-4b1f-a59c-44d15ac4a4a7)
Success!
