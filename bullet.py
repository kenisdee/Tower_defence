import pygame  # Импортирует библиотеку Pygame для работы с графикой и игровыми объектами.
from pygame.math import Vector2  # Импортирует класс Vector2 из модуля math библиотеки Pygame для работы с векторами.


class Bullet(pygame.sprite.Sprite):  # Определяет класс Bullet, который наследуется от pygame.sprite.Sprite.
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

    def __init__(self, start_pos, target_pos, damage, game):  # Конструктор класса Bullet.
        """
        Инициализация объекта Bullet.

        Args:
            start_pos (tuple): Начальная позиция пули.
            target_pos (tuple): Целевая позиция пули.
            damage (int): Урон, наносимый пулей.
            game (TowerDefenseGame): Основной объект игры.
        """
        super().__init__()  # Вызывает конструктор родительского класса (pygame.sprite.Sprite).
        self.game = game  # Сохраняет ссылку на основной объект игры.
        self.image = pygame.image.load(
            'assets/bullets/basic_bullet.png').convert_alpha()  # Загружает изображение пули и конвертирует его с учетом прозрачности.
        self.rect = self.image.get_rect(
            center=start_pos)  # Создает прямоугольник для обработки коллизий, центрируя его на начальной позиции.
        self.position = Vector2(start_pos)  # Сохраняет начальную позицию пули как вектор.
        self.target = Vector2(target_pos)  # Сохраняет целевую позицию пули как вектор.
        self.speed = 5  # Устанавливает скорость пули.
        self.damage = damage  # Устанавливает урон, наносимый пулей.
        self.velocity = self.calculate_velocity()  # Вычисляет вектор скорости пули.

    def calculate_velocity(self):  # Метод для вычисления вектора скорости пули.
        """
        Вычисляет вектор скорости пули на основе целевой позиции.

        Returns:
            Vector2: Вектор скорости пули.
        """
        direction = (self.target - self.position).normalize()  # Вычисляет направление к цели и нормализует его.
        velocity = direction * self.speed  # Умножает нормализованное направление на скорость, чтобы получить вектор скорости.
        return velocity  # Возвращает вектор скорости.

    def update(self):  # Метод для обновления состояния пули.
        """
        Обновляет позицию пули и проверяет, достигла ли она цели или вышла за пределы экрана.
        """
        self.position += self.velocity  # Обновляет позицию пули на основе её скорости.
        self.rect.center = self.position  # Обновляет прямоугольник пули, чтобы он соответствовал новой позиции.
        if self.position.distance_to(self.target) < 10 or not self.game.is_position_inside(
                self.position):  # Проверяет, достигла ли пуля цели или вышла за пределы экрана.
            self.kill()  # Удаляет пулю из группы спрайтов.

    def is_position_inside(self, pos):  # Метод для проверки, находится ли позиция внутри игрового экрана.
        """
        Проверяет, находится ли позиция внутри игрового экрана.

        Args:
            pos (Vector2): Координаты позиции.

        Returns:
            bool: True, если позиция находится внутри экрана, иначе False.
        """
        return 0 <= pos.x <= self.game.settings.screen_width and 0 <= pos.y <= self.game.settings.screen_height  # Возвращает True, если позиция находится внутри экрана, иначе False.
