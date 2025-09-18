import datetime
from dataclasses import dataclass
from typing import Optional

from src.domain.entity.Test import Test
from src.domain.entity.User import User


@dataclass
class Result:
    id: int
    user: User
    test: Test
    start_time: Optional[datetime.datetime]
    end_time: Optional[datetime.datetime]
    status: str
    link_token: Optional[str] = None
    interpretation: Optional[str] = None

    def change_status(self, status):
        """"Изменить статус результата"""
        self.status = status

    def set_start_time(self, start_time):
        """"Задать время начала"""
        self.start_time = start_time

    def set_end_time(self, end_time):
        """"Задать время окончания"""
        self.end_time = end_time

    def assign_link_token(self, token: str):
        self.link_token = token

    def set_interpretation(self, text: str):
        self.interpretation = text
        
