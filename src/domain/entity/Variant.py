from dataclasses import dataclass

@dataclass
class Variant:
    id: int
    var_text: str

    def change_text(self, text):
        """Изменить текст варианта ответа"""
        self.var_text = text
