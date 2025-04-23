class Field:
    __slots__ = ("name", "value", "verified_at")
    def __init__(self, name: str, value: str, verified_at: str = None):
        self.name = name
        self.value = value
        self.verified_at = verified_at
