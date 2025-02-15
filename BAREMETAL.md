
1) install react.js

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
. .bashrc

nvm install 18

node --version  # v18.20.6

npm --version  # 10.8.2


------

1) install pnpm  https://pnpm.io/installation

curl -fsSL https://get.pnpm.io/install.sh | sh -

. .bashrc


------

1) clone github repo voice-assistant-frontend

git clone https://github.com/livekit-examples/voice-assistant-frontend

2) provide credentials from livekit

cd voice-assistant-frontend

cat >.env.local

LIVEKIT_URL="wss://<URL>"
LIVEKIT_API_KEY="api-key"
LIVEKIT_API_SECRET="<api-secret>"

3) install node dependencies

pnpm i

4) start voice-assistant

pnpm dev

> voice-assistant2@0.1.0 dev /root/voice-assistant-frontend
> next dev

  ▲ Next.js 14.2.24
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Starting...
 

------

1) check python version

python3 --version
Python 3.8.10

2) if previous python than 3.10, remove it

apt remove python3-pip
apt remove python3
apt autoremove

3) install python 3.10
Install Python 3.10.x on Ubuntu 20.04 https://gist.github.com/rutcreate/c0041e842f858ceb455b748809763ddb

apt update
apt install software-properties-common -y

add-apt-repository ppa:deadsnakes/ppa
apt update

apt install python3.10 python3.10-dev

rm /usr/bin/python3
ln -s python3.10 /usr/bin/python3

4) install pip3 (compatible with python 3.10)

curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

python3.10 -m pip --version
pip 25.0.1 from /usr/local/lib/python3.10/dist-packages/pip (python 3.10)

------

1) install python dependencies

mkdir livekit-backend
cd livekit-backend

cat >requirements.txt  (copy from repo)

python3.10 -m pip install -r requirements.txt

2) copy agent_flight.py

cat >agent_flight.py  (copy from repo)

3) copy credentials

cat >.env

LIVEKIT_URL="wss://myserviceapp-yycieqvv.livekit.cloud"
LIVEKIT_API_KEY="<api-key>"
LIVEKIT_API_SECRET="<api-secret>"
GROQ_API_KEY="<api-key>"
ELEVEN_API_KEY="<api-key>"
DEEPGRAM_API_KEY="<api-key>"

4) start backend

python3 agent_flight.py dev

2025-02-15 23:12:25,842 - DEBUG asyncio - Using selector: EpollSelector
2025-02-15 23:12:25,845 - DEV  livekit.agents - Watching /root/livekit-backend
2025-02-15 23:12:26,923 - DEBUG asyncio - Using selector: EpollSelector
2025-02-15 23:12:26,929 - INFO livekit.agents - starting worker {"version": "0.12.13", "rtc-version": "0.20.0"}
2025-02-15 23:12:27,041 - INFO livekit.agents - registered worker {"id": "AW_2zmxSJNbytJa", "region": "Brazil", "protocol": 15, "node_id": "NC_OSAOPAULO1B_nzWQHHTofWTp"}

------

Create certicates

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout localhost.key -out localhost.crt

cp localhost.crt /etc/ssl/certs/localhost.crt

cp localhost.key /etc/ssl/private/localhost.key

------

Configure nginx

apt-get update && apt-get install nginx

1) create livekit file with nginx config

cd /etc/nginx/sites-available
cat >livefront (copy template from repo)

2) create symlink

cd /etc/nginx/sites-enabled
ln -s /etc/nginx/sites-available/livefront livefront

3) test and reload nginx

nginx -t
nginx -s reload

------

Configure hosts on client machine

cd C:\Windows\System32\drivers\etc

add an entry in hosts file using same name as in nginx

192.168.0.213   livefront

------

open an browser in client machine

https://livefront

<allow microphone>








