def is_palindrome(string):  # [too-many-lines]
    left_pos = 0
    right_pos = len(string) - 1
    while right_pos >= left_pos:
        if not string[left_pos] == string[right_pos]:
            return False
        left_pos += 1
        right_pos -= 1
    return True


def main():
    print(is_palindrome("aza"))
    print(is_palindrome("racecar"))
    print(is_palindrome("trigger"))
    print(is_palindrome("ogre"))
