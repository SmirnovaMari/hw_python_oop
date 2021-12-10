from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(
            self.training_type, self.duration,
            self.distance, self.speed,
            self.calories
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MIN_IN_HR: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise Exception

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: ClassVar[float] = 18
    COEFF_CALORIE_2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = (
            self.COEFF_CALORIE_1
            * self.get_mean_speed()
            - self.COEFF_CALORIE_2
        ) * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_HR
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_3: ClassVar[float] = 0.035
    COEFF_CALORIE_4: ClassVar[float] = 0.029
    height: float

    def get_spent_calories(self) -> float:
        spent_calories = ((self.COEFF_CALORIE_3 * self.weight
                          + (self.get_mean_speed()
                           ** 2 // self.height)
                           * self.COEFF_CALORIE_4 * self.weight)
                          ) * self.duration * self.MIN_IN_HR
        return spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38
    COEFF_CALORIE_5: ClassVar[float] = 1.1
    COEFF_CALORIE_6: ClassVar[float] = 2
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      ) / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = (self.get_mean_speed()
                          + self.COEFF_CALORIE_5
                          ) * self.COEFF_CALORIE_6 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {'WLK': SportsWalking,
                     'RUN': Running,
                     'SWM': Swimming}
    if workout_type in training_type:
        return training_type.get(workout_type)(*data)
    else:
        print('There is no such workout')


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
