class Enemy(object):
    x = 0
    y = 0
    sprite = None
    
    def __init__(self, x, y, sprite) -> None:
        self.x = x
        self.y = y
        self.sprite = sprite