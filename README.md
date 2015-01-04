tunefish
========

An automated band application and voting platform

Build client:
```sh
cd client
grunt build
```

Start celery for mails queue:
```sh
celery -A server.bands.mails worker
```

Start server:
```sh
python tunefish.py
```