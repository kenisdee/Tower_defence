import math

import pygame

from bullet import Bullet


class Tower(pygame.sprite.Sprite):
    """
    Базовый класс для всех типов башен.

    Атрибуты:
        position (pygame.math.Vector2): Позиция башни.
        game (TowerDefenseGame): Ссылка на основной объект игры.
        image (pygame.Surface): Изображение башни.
        rect (pygame.Rect): Прямоугольник для обработки коллизий.
        tower_range (int): Дальность действия башни.
        damage (int): Урон, наносимый башней.
        rate_of_fire (int): Скорострельность башни (в миллисекундах).
        last_shot_time (int): Время последнего выстрела.
        level (int): Уровень башни.
        original_image (pygame.Surface): Оригинальное изображение башни (без поворота).
    """

    def __init__(self, position, game):
        """
        Инициализация объекта Tower.

        Args:
            position (tuple): Позиция башни.
            game (TowerDefenseGame): Основной объект игры.
        """
        super().__init__()
        self.position = pygame.math.Vector2(position)
        self.game = game

        self.image = None
        self.rect = None
        self.tower_range = 0
        self.damage = 0
        self.rate_of_fire = 0
        self.last_shot_time = pygame.time.get_ticks()
        self.level = 1
        self.original_image = self.image

    def upgrade_cost(self):
        """
        Возвращает стоимость улучшения башни.

        Returns:
            int: Стоимость улучшения.
        """
        return 50 * self.level

    def draw(self, screen):
        """
        Отрисовывает башню на экране.

        Args:
            screen (pygame.Surface): Поверхность для отрисовки.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            level_text = self.game.font.render(f"Level: {self.level}", True, (255, 255, 255))
            upgrade_cost_text = self.game.font.render(f"Upgrade: ${self.upgrade_cost()}", True, (255, 255, 255))

            level_text_pos = (self.position.x, self.position.y + 20)
            upgrade_cost_pos = (self.position.x, self.position.y + 40)

            screen.blit(level_text, level_text_pos)
            screen.blit(upgrade_cost_text, upgrade_cost_pos)

    def update(self, enemies, current_time, bullets_group):
        """
        Обновляет состояние башни.

        Args:
            enemies (pygame.sprite.Group): Группа врагов.
            current_time (int): Текущее время в миллисекундах.
            bullets_group (pygame.sprite.Group): Группа пуль.
        """
        if current_time - self.last_shot_time > self.rate_of_fire:
            target = self.find_target(enemies)
            if target:
                self.rotate_towards_target(target)
                self.shoot(target, bullets_group)
                self.last_shot_time = current_time

    def is_hovered(self, mouse_pos):
        """
        Проверяет, наведена ли мышь на башню.

        Args:
            mouse_pos (tuple): Координаты мыши.

        Returns:
            bool: True, если мышь наведена на башню, иначе False.
        """
        return self.rect.collidepoint(mouse_pos)

    def shoot(self, target, bullets_group):
        """
        Выстрел башни по цели.

        Args:
            target (Enemy): Цель для выстрела.
            bullets_group (pygame.sprite.Group): Группа пуль.
        """
        # Преобразуем Vector2 в кортеж
        start_pos = (self.position.x, self.position.y)
        target_pos = (target.position.x, target.position.y)

        # Создаем новую пулю
        new_bullet = Bullet(start_pos, target_pos, self.damage, self.game)

        # Добавляем пулю в группу
        bullets_group.add(new_bullet)

        # Воспроизводим звук выстрела
        self.play_shoot_sound()

    def play_shoot_sound(self):
        """
        Воспроизведение звука выстрела.
        """
        shoot_sound = pygame.mixer.Sound(self.game.settings.shoot_sound)
        shoot_sound.play()

    def rotate_towards_target(self, target):
        """
        Поворачивает башню в сторону цели.

        Args:
            target (Enemy): Цель для поворота.
        """
        dx = target.position.x - self.position.x
        dy = target.position.y - self.position.y
        # Вычисляем угол в радианах
        angle_rad = math.atan2(dy, dx)
        # Преобразуем радианы в градусы
        angle_deg = math.degrees(angle_rad)
        angle_deg = -angle_deg - 90
        self.image = pygame.transform.rotate(self.original_image, angle_deg)
        self.rect = self.image.get_rect(center=self.position)

    def find_target(self, enemies):
        """
        Находит ближайшую цель для атаки.

        Args:
            enemies (pygame.sprite.Group): Группа врагов.

        Returns:
            Enemy: Ближайший враг, находящийся в радиусе действия башни.
        """
        nearest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = self.position.distance_to(enemy.position)
            if distance < min_distance and distance <= self.tower_range:
                nearest_enemy = enemy
                min_distance = distance
        return nearest_enemy

    def upgrade(self):
        """
        Улучшает башню, увеличивая её уровень, урон и скорострельность.
        """
        if self.game.settings.starting_money >= self.upgrade_cost():
            self.game.settings.starting_money -= self.upgrade_cost()
            self.level += 1
            self.damage = int(self.damage * 1.2)  # Увеличиваем урон на 20%
            self.rate_of_fire = int(self.rate_of_fire * 0.8)  # Увеличиваем скорострельность на 20%
            print(f"Tower upgraded to level {self.level}!")
        else:
            print("Not enough money to upgrade tower.")

class BasicTower(Tower):
    """
    Класс BasicTower представляет базовую башню.

    Атрибуты:
        tower_range (int): Дальность действия башни.
        damage (int): Урон, наносимый башней.
        rate_of_fire (int): Скорострельность башни (в миллисекундах).
    """

    def __init__(self, position, game):
        """
        Инициализация объекта BasicTower.

        Args:
            position (tuple): Позиция башни.
            game (TowerDefenseGame): Основной объект игры.
        """
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/basic_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 150
        self.damage = 20
        self.rate_of_fire = 1000


class SniperTower(Tower):
    """
    Класс SniperTower представляет снайперскую башню.

    Атрибуты:
        tower_range (int): Дальность действия башни.
        damage (int): Урон, наносимый башней.
        rate_of_fire (int): Скорострельность башни (в миллисекундах).
    """

    def __init__(self, position, game):
        """
        Инициализация объекта SniperTower.

        Args:
            position (tuple): Позиция башни.
            game (TowerDefenseGame): Основной объект игры.
        """
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/sniper_tower.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 300
        self.damage = 40
        self.rate_of_fire = 2000

    def find_target(self, enemies):
        """
        Находит цель с наибольшим здоровьем для атаки.

        Args:
            enemies (pygame.sprite.Group): Группа врагов.

        Returns:
            Enemy: Враг с наибольшим здоровьем, находящийся в радиусе действия башни.
        """
        healthiest_enemy = None
        max_health = 0
        for enemy in enemies:
            if self.position.distance_to(enemy.position) <= self.tower_range and enemy.health > max_health:
                healthiest_enemy = enemy
                max_health = enemy.health
        return healthiest_enemy


class MoneyTower(Tower):
    """
    Класс MoneyTower представляет башню, которая генерирует деньги.

    Атрибуты:
        money_generation_rate (int): Частота генерации денег (в миллисекундах).
        money_amount (int): Количество денег, которое генерирует башня.
        last_money_time (int): Время последней генерации денег.
    """

    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/money_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.money_generation_rate = 3000  # Генерация денег каждые 3 секунды
        self.money_amount = 50  # Башня генерирует 50 денег
        self.last_money_time = pygame.time.get_ticks()

    def update(self, enemies, current_time, bullets_group):
        """
        Обновляет состояние башни, проверяя, прошло ли достаточно времени для генерации денег.
        """
        if current_time - self.last_money_time > self.money_generation_rate:
            self.game.settings.starting_money += self.money_amount
            self.last_money_time = current_time
            print(f"Money generated: +${self.money_amount}")
