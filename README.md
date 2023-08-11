# chat-potato

Open source chat app for simplified community based organizations

## Build for Development

```
docker compose build --build-arg userid=$(id -u) --build-arg groupid=$(id -g)
docker compose run fullstack /bin/bash
cd server
pdm install
echo SECRET_KEY=narf > .env
echo DEBUG=on >> .env
pdm manage migrate
cd ..
npm install
```

## Development Environment Usage

### Frontend

```
docker compose run fullstack /bin/bash
npm run dev
```

### Backend

```
docker compose run fullstack /bin/bash
cd server/
pdm run dev
```
