# OAuth Service

OAuth Service provides an oauth style authentication mechanism for Convo users. It's primarily used to authenticate into Convo's browser extension.

```
# Build
docker build . -t oauth

# Run in development mode
docker run -e DEBUG=1 -p 8000:8000 -v $(pwd):/var/www oauth:latest uvicorn oauth:app --host 0.0.0.0 --port 8000 --reload

# Run in production mode
docker run oauth:latest
```
