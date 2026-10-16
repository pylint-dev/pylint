"""Test for deleted index."""

# pylint: disable=missing-function-docstring

def test_deleted_index(letters: list[str]) -> None:
    for index, letter in enumerate(letters): # [unused-variable]
        del index
        print(letters[index]) # [unnecessary-list-index-lookup]
