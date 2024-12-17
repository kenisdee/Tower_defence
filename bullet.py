import pygame
from pygame.math import Vector2


class Bullet(pygame.sprite.Sprite):
    """
    Класс Bullet представляет пулю, выпущенную башней.

    Атрибуты:
        game (TowerDefenseGame): Ссылка на основной объект игры.
        image (pygame.Surface): Изображение пули.
        rect (pygame.Rect): Прямоугольник для обработки коллизий.
        position (Vector2): Текущая позиция пули.
        target (Vector2): Целевая позиция, куда летит пуля.
        speed (int): Скорость пули.
        damage (int): Урон, наносимый пулей.
        velocity (Vector2): Вектор скорости пули.
    """

    def __init__(self, start_pos, target_pos, damage, game):
        """
        Инициализация объекта Bullet.

        Args:
            start_pos (tuple): Начальная позиция пули.
            target_pos (tuple): Целевая позиция пули.
            damage (int): Урон, наносимый пулей.
            game (TowerDefenseGame): Основной объект игры.
        """
        super().__init__()
        self.game = game
        self.image = pygame.image.load('assets/bullets/basic_bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.position = Vector2(start_pos)
        self.target = Vector2(target_pos)
        self.speed = 5
        self.damage = damage
        self.velocity = self.calculate_velocity()

    def calculate_velocity(self):
        """
        Вычисляет вектор скорости пули на основе целевой позиции.

        Returns:
            Vector2: Вектор скорости пули.
        """
        direction = (self.target - self.position).normalize()
        velocity = direction * self.speed
        return velocity

    def update(self):
        """
        Обновляет позицию пули и проверяет, достигла ли она цели или вышла за пределы экрана.
        """
        self.position += self.velocity
        self.rect.center = self.position
        if self.position.distance_to(self.target) < 10 or not self.game.is_position_inside(self.position):
            self.kill()

    def is_position_inside(self, pos):
        """
        Проверяет, находится ли позиция внутри игрового экрана.

        Args:
            pos (Vector2): Координаты позиции.

        Returns:
            bool: True, если позиция находится внутри экрана, иначе False.
        """
        return 0 <= pos.x <= self.game.settings.screen_width and 0 <= pos.y <= self.game.settings.screen_height
