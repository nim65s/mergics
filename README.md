# Mergics

Just merging multiple ICS into one.


## Launch all the things

```bash
echo SECRET_KEY=$(openssl rand -base64 32) >> .env
echo POSTGRES_PASSWORD=$(openssl rand -base64 32) >> .env
docker-compose up -d
```

## Start the tests

```bash
docker-compose up --build --exit-code-from test test
```
