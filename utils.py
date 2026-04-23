from dataclasses import dataclass

@dataclass
class Vector2:
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
