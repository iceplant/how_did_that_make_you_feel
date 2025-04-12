To run 

python3.9 -m uvicorn main:app --reload --host 0.0.0.0 --port 8001

To query the microservice

curl -X POST "http://127.0.0.1:8001/emotion" -H "Content-Type: application/json" -d '{"text": "I am feeling great today!"}'