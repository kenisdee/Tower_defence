import pygame  # Импортирует библиотеку Pygame для работы с графикой и игровыми объектами.
from pygame.math import Vector2  # Импортирует класс Vector2 из модуля math библиотеки Pygame для работы с векторами.


class Enemy(pygame.sprite.Sprite):  # Определяет класс Enemy, который наследуется от pygame.sprite.Sprite.
    """
    Класс Enemy представляет врага, которого игрок должен уничтожить.

    Атрибуты:
        image (pygame.Surface): Изображение врага.
        rect (pygame.Rect): Прямоугольник для обработки коллизий.
        game (TowerDefenseGame): Ссылка на основной объект игры.
        path (list): Список точек, по которым движется враг.
        path_index (int): Индекс текущей точки пути.
        speed (float): Скорость движения врага.
        health (int): Здоровье врага.
        position (Vector2): Текущая позиция врага.
    """

    def __init__(self, path, speed=2, health=10, image_path=None, game=None):  # Конструктор класса Enemy.
        """
        Инициализация объекта Enemy.

        Args:
            path (list): Список точек, по которым движется враг.
            speed (float): Скорость движения врага.
            health (int): Здоровье врага.
            image_path (str): Путь к изображению врага.
            game (TowerDefenseGame): Основной объект игры.
        """
        super().__init__()  # Вызывает конструктор родительского класса (pygame.sprite.Sprite).
        self.image = pygame.Surface((30, 40))  # Создает пустое изображение врага размером 30x40.
        self.image = pygame.image.load(
            image_path).convert_alpha()  # Загружает изображение врага и конвертирует его с учетом прозрачности.
        self.rect = self.image.get_rect()  # Создает прямоугольник для обработки коллизий на основе изображения.
        self.game = game  # Сохраняет ссылку на основной объект игры.
        self.path = path  # Сохраняет список точек, по которым будет двигаться враг.
        self.path_index = 0  # Устанавливает начальный индекс пути (первая точка).
        self.speed = speed  # Устанавливает скорость движения врага.
        self.health = health  # Устанавливает здоровье врага.
        self.position = Vector2(path[0])  # Устанавливает начальную позицию врага (первая точка пути).
        self.rect.center = self.position  # Центрирует прямоугольник врага на его позиции.

        self.play_spawn_sound()  # Воспроизводит звук появления врага.

    def take_damage(self, amount):  # Метод для нанесения урона врагу.
        """
        Наносит урон врагу.

        Args:
            amount (int): Количество урона.
        """
        self.health -= amount  # Уменьшает здоровье врага на указанное количество.
        if self.health <= 0:  # Проверяет, если здоровье меньше или равно нулю.
            self.kill()  # Удаляет врага из группы спрайтов.

    def update(self):  # Метод для обновления состояния врага.
        """
        Обновляет позицию врага и проверяет, достиг ли он конца пути.
        """
        if self.path_index < len(self.path) - 1:  # Проверяет, есть ли еще точки в пути.
            start_point = Vector2(self.path[self.path_index])  # Получает текущую точку пути.
            end_point = Vector2(self.path[self.path_index + 1])  # Получает следующую точку пути.
            direction = (
                        end_point - start_point).normalize()  # Вычисляет направление к следующей точке и нормализует его.

            self.position += direction * self.speed  # Обновляет позицию врага на основе его скорости.
            self.rect.center = self.position  # Обновляет прямоугольник врага, чтобы он соответствовал новой позиции.

            if self.position.distance_to(end_point) < self.speed:  # Проверяет, достиг ли враг следующей точки.
                self.path_index += 1  # Переходит к следующей точке пути.

            if self.path_index >= len(self.path) - 1:  # Проверяет, достиг ли враг конца пути.
                self.game.game_over()  # Вызывает метод game_over у игры.
                self.kill()  # Удаляет врага из группы спрайтов.

    def play_spawn_sound(self):  # Метод для воспроизведения звука появления врага.
        """
        Воспроизведение звука появления врага.
        """
        spawn_sound = pygame.mixer.Sound(self.game.settings.enemy_spawn_sound)  # Загружает звук появления врага.
        spawn_sound.play()  # Воспроизводит звук.
