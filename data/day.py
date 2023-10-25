from dataclasses import dataclass


@dataclass
class Day:
    average_temperature: float | None
    relevant_conditions_hours: int | None

    def __repr__(self):
        return f'{self.average_temperature}°C, {self.relevant_conditions_hours} good days'
