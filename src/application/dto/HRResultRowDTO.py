from dataclasses import dataclass

@dataclass
class HRResultRowDTO:
    test_name: str
    start_time: str
    end_time: str
    link_token: str 