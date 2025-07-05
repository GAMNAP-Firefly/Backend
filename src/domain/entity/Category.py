from dataclasses import dataclass

@dataclass
class Category:
    id: int
    name: str

    def change_name(self, name):
        """"Изменить название категории"""
        self.name = name

