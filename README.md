# OAuth Service

```
sudo docker run -e DEBUG=1 -p 8000:8000 -v $(pwd):/var/www oauth uvicorn oauth:app --host 0.0.0.0 --port 8000 --reload
```
