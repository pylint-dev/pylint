class CustomIndex:
    """__index__ returns a dict"""

    def __index__(self):  # [invalid-index-returned]
        return {"19": "19"}
