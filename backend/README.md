# Backend


## Database

To download de database use the following [link](https://drive.google.com/file/d/1d5IVKl9UkmqORDULL0ag1fLQ9jcVqPfy/view?usp=sharing)

Place the `db` directory on the root of the `backend` folder

## Chrome Extension

To download de chrome extension use the following [link](https://drive.google.com/file/d/1nbJz6FGyvrp7RABEEt70anILTZdCHrzH/view?usp=sharing)

Place the `nnpljppamoaalgkieeciijbcccohlpoh` directory on the root of the `backend` folder

## Setup

**Install Python 3.7**

```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.7 python3.7-venv
```

**Create Virutal Env**

```
python3.7 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Download Mongodb**

```
sudo apt install gnupg curl
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt-get install -y mongodb-org
```

**Change files with machine IPS**

- server/run.py:9
- server/config.py:5
- nnpljppamoaalgkieeciijbcccohlpoh/Path.js:85

## Running

**Running the Database**

```
mongod --dbpath=db --bind_ip 192.168.0.15
```

**Running the Backend**

```
source .venv/bin/activate
python server/run.py
```
