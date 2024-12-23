import math  # Импортирует модуль math для работы с математическими функциями.

import pygame  # Импортирует библиотеку Pygame для работы с графикой и игровыми объектами.

from bullet import Bullet  # Импортирует класс Bullet из файла bullet.py.


class Tower(pygame.sprite.Sprite):  # Определяет базовый класс Tower, который наследуется от pygame.sprite.Sprite.
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

    def __init__(self, position, game):  # Конструктор класса Tower.
        """
        Инициализация объекта Tower.

        Args:
            position (tuple): Позиция башни.
            game (TowerDefenseGame): Основной объект игры.
        """
        super().__init__()  # Вызывает конструктор родительского класса (pygame.sprite.Sprite).
        self.position = pygame.math.Vector2(position)  # Сохраняет позицию башни как вектор.
        self.game = game  # Сохраняет ссылку на основной объект игры.

        self.image = None  # Инициализирует изображение башни как None.
        self.rect = None  # Инициализирует прямоугольник башни как None.
        self.tower_range = 0  # Инициализирует дальность действия башни.
        self.damage = 0  # Инициализирует урон башни.
        self.rate_of_fire = 0  # Инициализирует скорострельность башни.
        self.last_shot_time = pygame.time.get_ticks()  # Записывает время последнего выстрела.
        self.level = 1  # Устанавливает уровень башни на 1.
        self.original_image = self.image  # Сохраняет оригинальное изображение башни.

    def upgrade_cost(self):  # Метод для расчета стоимости улучшения башни.
        """
        Возвращает стоимость улучшения башни.

        Returns:
            int: Стоимость улучшения.
        """
        return 50 * self.level  # Возвращает стоимость улучшения, зависящую от текущего уровня башни.

    def draw(self, screen):  # Метод для отрисовки башни на экране.
        """
        Отрисовывает башню на экране.

        Args:
            screen (pygame.Surface): Поверхность для отрисовки.
        """
        mouse_pos = pygame.mouse.get_pos()  # Получает текущую позицию мыши.
        if self.is_hovered(mouse_pos):  # Проверяет, наведена ли мышь на башню.
            level_text = self.game.font.render(f"Level: {self.level}", True,
                                               (255, 255, 255))  # Создает текст с уровнем башни.
            upgrade_cost_text = self.game.font.render(f"Upgrade: ${self.upgrade_cost()}", True,
                                                      (255, 255, 255))  # Создает текст с ценой улучшения.

            level_text_pos = (self.position.x, self.position.y + 20)  # Устанавливает позицию текста с уровнем.
            upgrade_cost_pos = (
            self.position.x, self.position.y + 40)  # Устанавливает позицию текста с ценой улучшения.

            screen.blit(level_text, level_text_pos)  # Рисует текст с уровнем на экране.
            screen.blit(upgrade_cost_text, upgrade_cost_pos)  # Рисует текст с ценой улучшения на экране.

    def update(self, enemies, current_time, bullets_group):  # Метод для обновления состояния башни.
        """
        Обновляет состояние башни.

        Args:
            enemies (pygame.sprite.Group): Группа врагов.
            current_time (int): Текущее время в миллисекундах.
            bullets_group (pygame.sprite.Group): Группа пуль.
        """
        if current_time - self.last_shot_time > self.rate_of_fire:  # Проверяет, прошло ли достаточно времени для выстрела.
            target = self.find_target(enemies)  # Находит цель для атаки.
            if target:  # Если цель найдена.
                self.rotate_towards_target(target)  # Поворачивает башню в сторону цели.
                self.shoot(target, bullets_group)  # Выполняет выстрел.
                self.last_shot_time = current_time  # Обновляет время последнего выстрела.

    def is_hovered(self, mouse_pos):  # Метод для проверки, наведена ли мышь на башню.
        """
        Проверяет, наведена ли мышь на башню.

        Args:
            mouse_pos (tuple): Координаты мыши.

        Returns:
            bool: True, если мышь наведена на башню, иначе False.
        """
        return self.rect.collidepoint(mouse_pos)  # Возвращает True, если мышь наведена на башню.

    def shoot(self, target, bullets_group):  # Метод для выполнения выстрела.
        """
        Выстрел башни по цели.

        Args:
            target (Enemy): Цель для выстрела.
            bullets_group (pygame.sprite.Group): Группа пуль.
        """
        # Преобразуем Vector2 в кортеж
        start_pos = (self.position.x, self.position.y)  # Получает начальную позицию башни.
        target_pos = (target.position.x, target.position.y)  # Получает позицию цели.

        # Создаем новую пулю
        new_bullet = Bullet(start_pos, target_pos, self.damage, self.game)  # Создает новую пулю.

        # Добавляем пулю в группу
        bullets_group.add(new_bullet)  # Добавляет пулю в группу пуль.

        # Воспроизводим звук выстрела
        self.play_shoot_sound()  # Воспроизводит звук выстрела.

    def play_shoot_sound(self):  # Метод для воспроизведения звука выстрела.
        """
        Воспроизведение звука выстрела.
        """
        shoot_sound = pygame.mixer.Sound(self.game.settings.shoot_sound)  # Загружает звук выстрела.
        shoot_sound.play()  # Воспроизводит звук.

    def rotate_towards_target(self, target):  # Метод для поворота башни в сторону цели.
        """
        Поворачивает башню в сторону цели.

        Args:
            target (Enemy): Цель для поворота.
        """
        dx = target.position.x - self.position.x  # Вычисляет разницу по оси X.
        dy = target.position.y - self.position.y  # Вычисляет разницу по оси Y.
        # Вычисляем угол в радианах
        angle_rad = math.atan2(dy, dx)  # Вычисляет угол в радианах.
        # Преобразуем радианы в градусы
        angle_deg = math.degrees(angle_rad)  # Преобразует угол в градусы.
        angle_deg = -angle_deg - 90  # Корректирует угол для правильного отображения.
        self.image = pygame.transform.rotate(self.original_image, angle_deg)  # Поворачивает изображение башни.
        self.rect = self.image.get_rect(center=self.position)  # Обновляет прямоугольник башни.

    def find_target(self, enemies):  # Метод для поиска цели для атаки.
        """
        Находит ближайшую цель для атаки.

        Args:
            enemies (pygame.sprite.Group): Группа врагов.

        Returns:
            Enemy: Ближайший враг, находящийся в радиусе действия башни.
        """
        nearest_enemy = None  # Инициализирует переменную для ближайшего врага.
        min_distance = float('inf')  # Инициализирует минимальное расстояние как бесконечность.
        for enemy in enemies:  # Перебирает всех врагов.
            distance = self.position.distance_to(enemy.position)  # Вычисляет расстояние до врага.
            if distance < min_distance and distance <= self.tower_range:  # Проверяет, ближе ли враг и в радиусе действия башни.
                nearest_enemy = enemy  # Обновляет ближайшего врага.
                min_distance = distance  # Обновляет минимальное расстояние.
        return nearest_enemy  # Возвращает ближайшего врага.

    def upgrade(self):  # Метод для улучшения башни.
        """
        Улучшает башню, увеличивая её уровень, урон и скорострельность.
        """
        if self.game.settings.starting_money >= self.upgrade_cost():  # Проверяет, достаточно ли денег для улучшения.
            self.game.settings.starting_money -= self.upgrade_cost()  # Уменьшает количество денег на стоимость улучшения.
            self.level += 1  # Увеличивает уровень башни.
            self.damage = int(self.damage * 1.2)  # Увеличивает урон на 20%.
            self.rate_of_fire = int(self.rate_of_fire * 0.8)  # Увеличивает скорострельность на 20%.
            print(f"Tower upgraded to level {self.level}!")  # Выводит сообщение об улучшении.
        else:
            print("Not enough money to upgrade tower.")  # Выводит сообщение о недостатке денег.


class BasicTower(Tower):  # Определяет класс BasicTower, который наследуется от Tower.
    """
    Класс BasicTower представляет базовую башню.

    Атрибуты:
        tower_range (int): Дальность действия башни.
        damage (int): Урон, наносимый башней.
        rate_of_fire (int): Скорострельность башни (в миллисекундах).
    """

    def __init__(self, position, game):  # Конструктор класса BasicTower.
        """
        Инициализация объекта BasicTower.

        Args:
            position (tuple): Позиция башни.
            game (TowerDefenseGame): Основной объект игры.
        """
        super().__init__(position, game)  # Вызывает конструктор родительского класса.
        self.image = pygame.image.load(
            'assets/towers/basic_tower.png').convert_alpha()  # Загружает изображение базовой башни.
        self.original_image = self.image  # Сохраняет оригинальное изображение башни.
        self.rect = self.image.get_rect(center=self.position)  # Создает прямоугольник для башни.
        self.tower_range = 150  # Устанавливает дальность действия башни.
        self.damage = 20  # Устанавливает урон башни.
        self.rate_of_fire = 1000  # Устанавливает скорострельность башни.


class SniperTower(Tower):  # Определяет класс SniperTower, который наследуется от Tower.
    """
    Класс SniperTower представляет снайперскую башню.

    Атрибуты:
        tower_range (int): Дальность действия башни.
        damage (int): Урон, наносимый башней.
        rate_of_fire (int): Скорострельность башни (в миллисекундах).
    """

    def __init__(self, position, game):  # Конструктор класса SniperTower.
        """
        Инициализация объекта SniperTower.

        Args:
            position (tuple): Позиция башни.
            game (TowerDefenseGame): Основной объект игры.
        """
        super().__init__(position, game)  # Вызывает конструктор родительского класса.
        self.image = pygame.image.load(
            'assets/towers/sniper_tower.png').convert_alpha()  # Загружает изображение снайперской башни.
        self.image = pygame.transform.rotate(self.image, 90)  # Поворачивает изображение башни на 90 градусов.
        self.original_image = self.image  # Сохраняет оригинальное изображение башни.
        self.rect = self.image.get_rect(center=self.position)  # Создает прямоугольник для башни.
        self.tower_range = 300  # Устанавливает дальность действия башни.
        self.damage = 40  # Устанавливает урон башни.
        self.rate_of_fire = 2000  # Устанавливает скорострельность башни.

    def find_target(self, enemies):  # Переопределяет метод поиска цели для снайперской башни.
        """
        Находит цель с наибольшим здоровьем для атаки.

        Args:
            enemies (pygame.sprite.Group): Группа врагов.

        Returns:
            Enemy: Враг с наибольшим здоровьем, находящийся в радиусе действия башни.
        """
        healthiest_enemy = None  # Инициализирует переменную для врага с наибольшим здоровьем.
        max_health = 0  # Инициализирует максимальное здоровье.
        for enemy in enemies:  # Перебирает всех врагов.
            if self.position.distance_to(
                    enemy.position) <= self.tower_range and enemy.health > max_health:  # Проверяет, в радиусе ли враг и его здоровье больше максимального.
                healthiest_enemy = enemy  # Обновляет врага с наибольшим здоровьем.
                max_health = enemy.health  # Обновляет максимальное здоровье.
        return healthiest_enemy  # Возвращает врага с наибольшим здоровьем.


class MoneyTower(Tower):  # Определяет класс MoneyTower, который наследуется от Tower.
    """
    Класс MoneyTower представляет башню, которая генерирует деньги.

    Атрибуты:
        money_generation_rate (int): Частота генерации денег (в миллисекундах).
        money_amount (int): Количество денег, которое генерирует башня.
        last_money_time (int): Время последней генерации денег.
    """

    def __init__(self, position, game):  # Конструктор класса MoneyTower.
        super().__init__(position, game)  # Вызывает конструктор родительского класса.
        self.image = pygame.image.load(
            'assets/towers/money_tower.png').convert_alpha()  # Загружает изображение башни, генерирующей деньги.
        self.original_image = self.image  # Сохраняет оригинальное изображение башни.
        self.rect = self.image.get_rect(center=self.position)  # Создает прямоугольник для башни.
        self.money_generation_rate = 3000  # Устанавливает частоту генерации денег (каждые 3 секунды).
        self.money_amount = 50  # Устанавливает количество денег, которое генерирует башня.
        self.last_money_time = pygame.time.get_ticks()  # Записывает время последней генерации денег.

    def update(self, enemies, current_time,
               bullets_group):  # Переопределяет метод обновления для башни, генерирующей деньги.
        """
        Обновляет состояние башни, проверяя, прошло ли достаточно времени для генерации денег.
        """
        if current_time - self.last_money_time > self.money_generation_rate:  # Проверяет, прошло ли достаточно времени для генерации денег.
            self.game.settings.starting_money += self.money_amount  # Увеличивает количество денег игрока.
            self.last_money_time = current_time  # Обновляет время последней генерации денег.
            print(f"Money generated: +${self.money_amount}")  # Выводит сообщение о сгенерированных деньгах.
