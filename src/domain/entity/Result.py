import datetime
from dataclasses import dataclass

from src.domain.entity.Test import Test
from src.domain.entity.User import User


@dataclass
class Result:
    id: int
    user: User
    test: Test
    start_time: datetime
    end_time: datetime
    status: str

    def change_status(self, status):
        """"Изменить статус результата"""
        self.status = status

    def set_start_time(self, start_time):
        """"Задать время начала"""
        self.start_time = start_time

    def set_end_time(self, end_time):
        """"Задать время окончания"""
        self.end_time = end_time
        
