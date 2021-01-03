import sys
import joblib
import traceback

import click
import datetime
import random
import datetime

from .config import check_config, get_fake_followers
from .models import create_all
from .utils import check_links_and_update, fetch_accounts_and_links, get_followers_generator, send_offline_links_notifications



@click.command(help='Fetch links from Twitter user bio')
def fetch():
    print(f"fetch - {datetime.datetime.now()}")
    fetch_accounts_and_links(get_fake_followers())
    fetch_accounts_and_links(get_followers_generator())
    print(f"done fetch - {datetime.datetime.now()}")

@click.command(help='Check which of the fetched links are online/offline')
def check():
    print(f"check - {datetime.datetime.now()}")
    check_links_and_update()
    print(f"done check - {datetime.datetime.now()}")

@click.command(help='Send notifications to users that have links down in their bio')
def notify():
    print(f"notify - {datetime.datetime.now()}")
    send_offline_links_notifications()
    print(f"done notify - {datetime.datetime.now()}")

@click.command(help='Check links status and send notifications to users that have links down in their bio')
def check_notify():
    print(f"check - {datetime.datetime.now()}")
    check_links_and_update()
    send_offline_links_notifications()
    print(f"done check - {datetime.datetime.now()}")

@click.group()
def main_handler():
    # Kept empty as it is only an entry point to other commands
    pass

main_handler.add_command(fetch)
main_handler.add_command(check)
main_handler.add_command(notify)
main_handler.add_command(check_notify)

def main():
    try:
        check_config()
        create_all()
        main_handler()
    except Exception as err:
        print("Exception in user code:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)


if __name__ == "__main__":
    main()