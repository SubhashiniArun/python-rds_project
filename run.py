from app import create_app
import logging

logging.basicConfig(level=logging.INFO)

app = create_app(config_name="development")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)