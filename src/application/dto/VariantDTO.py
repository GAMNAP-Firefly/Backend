from dataclasses import dataclass

@dataclass
class VariantDTO:
    id: int
    text: str
    is_selected: bool = False 