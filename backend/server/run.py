# /run.py

from app import create_app

app = create_app()

if __name__ == '__main__':
    
    app.run(host='192.168.0.15')