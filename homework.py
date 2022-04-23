from __future__ import annotations


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {format(self.duration, ".3f")} ч.;'
                f' Дистанция: {format(self.distance, ".3f")} км;'
                f' Ср. скорость: {format(self.speed, ".3f")} км/ч;'
                f' Потрачено ккал: {format(self.calories, ".3f")}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65      # длина шага
    M_IN_KM = 1000       # количество метров в километре
    miutes_in_hour = 60  # количество минут в часе

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return Training.get_distance(self) / self.duration

    def get_spent_calories(self) -> float:
        """Получить каличество затраченных каларий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    coeff_calorie_1 = 18  # коэффициент для расчета калорий
    coeff_calorie_2 = 20  # коэффициент для расчета калорий

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight,
                         )

    def get_spent_calories(self) -> float:
        """Получить каличество затраченных каларий при беге."""
        return ((self.coeff_calorie_1
                * self.get_mean_speed()
                - self.coeff_calorie_2)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.miutes_in_hour)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    coeff_calorie_3 = 0.035  # коэффициент для расчета калорий
    coeff_calorie_4 = 2      # коэффициент для расчета калорий
    coeff_calorie_5 = 0.029  # коэффициент для расчета калорий

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight,
                         )
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить каличество затраченных каларий при спортивной ходьбе."""
        return ((self.coeff_calorie_3
                * self.weight
                + (self.get_mean_speed()**self.coeff_calorie_4 // self.height)
                * self.coeff_calorie_5
                * self.weight
                 )
                * self.duration
                * self.miutes_in_hour
                )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38        # длина гребка
    coeff_calorie_6 = 1.1  # коэффициент для расчета калорий
    coeff_calorie_7 = 2    # коэффициент для расчета калорий

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight,
                         )
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить каличество затраченных каларий при плавании."""
        return ((self.get_mean_speed() + self.coeff_calorie_6)
                * self.coeff_calorie_7
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(data[0], data[1], data[2], data[3], data[4])
    elif workout_type == 'RUN':
        return Running(data[0], data[1], data[2])
    elif workout_type == 'WLK':
        return SportsWalking(data[0], data[1], data[2], data[3])


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
