"""
Module name: scratch

used for testing and debugging
"""

from redistools import connect_to_redis, get_sorted_index_list_for_word


def main():
    """
    Main
    """

    client = connect_to_redis()

    print(str(get_sorted_index_list_for_word(client, "python")))


if __name__ == "__main__":
    main()
