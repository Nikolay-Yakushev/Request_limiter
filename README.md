Request time limiter is a HTTP flask based service to limit request which exceeds certain amount.

User instruction:
It is allowed to set custom variables to a server. To od this read docker-compose.yaml comments section.

    input:
        sudo docker-compose up
        
    output:
        app_1  |  * Serving Flask app "main" (lazy loading)
        app_1  |  * Environment: production
        app_1  |    WARNING: This is a development server. Do not use it in a production deployment.
        app_1  |    Use a production WSGI server instead.
        app_1  |  * Debug mode: off
        app_1  |  * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)

