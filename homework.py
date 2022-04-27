from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    INFO: str = (
        'Тип тренировки: {training_type}; Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self):
        return self.INFO.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int      # количество совершённых действий
    duration: float  # длительность тренировки в часах
    weight: float    # вес спортсмена в килограммах

    LEN_STEP: float = 0.65      # длина шага
    M_IN_KM: int = 1000         # количество метров в километре
    MINUTES_IN_HOUR: int = 60   # количество минут в часе

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить каличество затраченных каларий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_RUNNING_1: int = 18
    # коэффициент для расчета калорий при беге
    COEFF_CALORIE_RUNNING_2: int = 20
    # коэффициент для расчета калорий при беге

    def get_spent_calories(self) -> float:
        """Получить каличество затраченных каларий при беге."""
        return ((self.COEFF_CALORIE_RUNNING_1
                * self.get_mean_speed()
                - self.COEFF_CALORIE_RUNNING_2)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.MINUTES_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action, duration, weight, height) -> None:
        super().__init__(action, duration, weight)
        self.height: int = height       # рост спортсмена в сантиметрах

    COEFF_CALORIE_SPORTWALKING_1: float = 0.035
    # коэффициент для расчета калорий при спортивной хотьбе
    COEFF_CALORIE_SPORTWALKING_2: float = 0.029
    # коэффициент для расчета калорий при спортивной хотьбе

    def get_spent_calories(self) -> float:
        """Получить каличество затраченных каларий при спортивной ходьбе."""
        return ((self.COEFF_CALORIE_SPORTWALKING_1
                * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_CALORIE_SPORTWALKING_2
                * self.weight
                 )
                * self.duration
                * self.MINUTES_IN_HOUR
                )


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        self.action: int = action
        # количество гребков
        self.duration: float = duration
        # длительность тренировки в часах
        self.weight: float = weight
        # вес спортсмена в килограммах
        self.length_pool: float = length_pool
        # длина бассейна в метрах
        self.count_pool: int = count_pool
        # сколько раз спортсмен переплыл бассейн

    LEN_STEP: float = 1.38
    # длина гребка
    COEFF_CALORIE_SWIMMING_1: float = 1.1
    # коэффициент для расчета калорий при плавании
    COEFF_CALORIE_SWIMMING_2: int = 2
    # коэффициент для расчета калорий при плавании

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить каличество затраченных каларий при плавании."""
        return ((self.get_mean_speed() + self.COEFF_CALORIE_SWIMMING_1)
                * self.COEFF_CALORIE_SWIMMING_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    TRAINING_DICT: Type[Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return TRAINING_DICT[workout_type](*data)
    except Exception:
        raise RuntimeError(f'Такого типа тренировки нет: "{workout_type}"')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
