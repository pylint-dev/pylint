class Unicorn:
    def __init__(self, fluffiness_level):
        if self.fluffiness_level > 9000:  # [access-member-before-definition]
            print("It's OVER-FLUFFYYYY ! *crush glasses*")
        self.fluffiness_level = fluffiness_level
