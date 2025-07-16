from dataclasses import dataclass

@dataclass
class Category:
    id: int
    name: str
    mean: float | None = None
    deviation: float | None = None

    def change_name(self, name):
        """"Изменить название категории"""
        self.name = name

