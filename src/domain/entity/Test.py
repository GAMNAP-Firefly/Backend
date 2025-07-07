from dataclasses import dataclass

@dataclass
class Test:
    id: int
    name: str
    description: str

    def change_name(self, name):
        """"Изменить наизвание теста"""
        self.name = name

    def  change_description(self, description):
        """"Изменить описание теста"""
        self.description = description