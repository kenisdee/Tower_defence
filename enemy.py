import pygame
from pygame.math import Vector2


class Enemy(pygame.sprite.Sprite):
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

    def __init__(self, path, speed=2, health=10, image_path=None, game=None):
        """
        Инициализация объекта Enemy.

        Args:
            path (list): Список точек, по которым движется враг.
            speed (float): Скорость движения врага.
            health (int): Здоровье врага.
            image_path (str): Путь к изображению врага.
            game (TowerDefenseGame): Основной объект игры.
        """
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.game = game
        self.path = path
        self.path_index = 0
        self.speed = speed
        self.health = health
        self.position = Vector2(path[0])
        self.rect.center = self.position

        self.play_spawn_sound()

    def take_damage(self, amount):
        """
        Наносит урон врагу.

        Args:
            amount (int): Количество урона.
        """
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def update(self):
        """
        Обновляет позицию врага и проверяет, достиг ли он конца пути.
        """
        if self.path_index < len(self.path) - 1:
            start_point = Vector2(self.path[self.path_index])
            end_point = Vector2(self.path[self.path_index + 1])
            direction = (end_point - start_point).normalize()

            self.position += direction * self.speed
            self.rect.center = self.position

            if self.position.distance_to(end_point) < self.speed:
                self.path_index += 1

            if self.path_index >= len(self.path) - 1:
                self.game.game_over()
                self.kill()

    def play_spawn_sound(self):
        """
        Воспроизведение звука появления врага.
        """
        spawn_sound = pygame.mixer.Sound(self.game.settings.enemy_spawn_sound)
        spawn_sound.play()
