# biolinkchecker
Periodically checks links in Twitter bio and send a notification if a link is down

## Quickstart
### Requirements
First of all, you need [docker>=19.03](https://docs.docker.com/install/) and [docker-compose>=1.25.1](https://docs.docker.com/compose/install/)

### Configuration
A file named `.env` based on `template.env` is required at the root of the project directory.
Required parameters are:
```bash
# Used only for testing purposes should be kept empty in production
FAKE_FOLLOWERS_IDS=


# If set (1), check and fetch will be executed as one cron based on CRON_SCHEDULE_CHECK_NOTIFY
CHECK_NOTIFY=

# For more informations about cron schedules visit: https://en.wikipedia.org/wiki/Cron
# schedule when followers are fetched #watchout for the Twitter api limits
CRON_SCHEDULE_FETCH="0 */12 */1 * *"
# Schedule how often/when urls in followers' bio are checked. It should be at max once per hour
CRON_SCHEDULE_CHECK="15 */4 */1 * *"
# Schedule how often/when notifications are send to users. It shouldn't be more often than CRON_SCHEDULE_CHECK
CRON_SCHEDULE_NOTIFY="30 */4 */1 * *"
# Schedule how often/when : urls and check and notifications are send to users. It shouldn't be more often than
CRON_SCHEDULE_CHECK_NOTIFY="30 */4 */1 * *"


# SqlAlchemy database connection string. For more informations visit: https://docs.sqlalchemy.org/en/latest/core/engines.html
## e.g.: "sqlite:///code/data/db.sqlite3"  or "sqlite://" for an in-memory database
SQLALCHEMY_DATABASE_URI="sqlite://"

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