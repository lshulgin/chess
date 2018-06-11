# Helper class for displaying board coordinates
class Square:
    def __init__(self, x, y):
        self.x, self.y = x, y

    @staticmethod
    def create(string):
        x = ord(string[0]) - ord('a')
        y = int(string[1]) - 1
        return Square(x, y)

    def __repr__(self):
        if self.x > 25 or self.y > 8:
            raise Exception("Can't support squares past z9")

        return '%s%d' % (chr(ord('a') + self.x), self.y + 1)
