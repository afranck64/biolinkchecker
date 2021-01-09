# biolinkchecker
Periodically checks links in Twitter bio and send a notification if a link is down

## Quickstart
### Requirements
First of all, you need [docker>=19.03](https://docs.docker.com/install/) and [docker-compose>=1.25.1](https://docs.docker.com/compose/install/)

### Configuration
A file named `.env` based on `template.env` is required at the root of the project directory.
Required parameters are listed below:
```bash
# Twitter app/bot credentials. For more informations visit: https://apps.twitter.com/
TWITTER_CONSUMER_KEY=
TWITTER_CONSUMER_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_SECRET=
```

## Build the project:
```bash
./build.sh
```

## Use individual actions

### Fetch data/links from followers
```bash
docker-compose run bot fetch
```

### Check if previously fetched links are online/offline
```bash
docker-compose run bot check
```

### Notify users that have links down in their bio
```bash
docker-compose run bot notify
```

### Start the bot and let it manage all required actions
```bash
docker-compose up bot
```


## Author(s)
- [@afranck64](https://github.com/afranck64)