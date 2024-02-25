"""
Module name: main

Author: Cabbage Stone

Date: 02-24-2024

Description: This is the control center for the Wikipedia search engine. It
handles the user input, and the search term by fetching the search page,
creating the page index, and updating relevant pagerank scores, and then
returning the relevant links sorted by a hybrid scoring system.

Example usage:

    python main.py

"""

import sys

from redistools import connect_to_redis
from search import handle_search_term


def main():
    """
    Main function that connects to Redis, prompts the user for a search term,
    and handles the search term by fetching the search page, creating the page index,
    and updating relevant pagerank scores, and then returning the relevant links
    sorted by a hybrid scoring system
    """
    redis_client = connect_to_redis()

    while True:

        search_term = input("Enter a search term or !help: ")

        if handle_command(search_term):
            continue

        handle_search_term(redis_client, search_term)


def handle_command(search_term):
    """
    Function that checks to see if the search_term is a command,
    and if so, executes the command.

    Parameters:
    - search_term: The search term entered by the user.

    Returns:
    - True if the search term was a command, False otherwise.
    """
    if search_term.startswith("!"):
        if search_term == "!help":
            print("type !exit to exit the program.")
            print("type !help to see this message.")
            return True
        if search_term == "!exit":
            print("Exiting program.")
            sys.exit()
        else:
            print("Unknown command. Type !help for help.")
            return True

    return False


if __name__ == "__main__":
    main()
