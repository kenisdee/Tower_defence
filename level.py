import random  # Импортирует модуль random для работы со случайными числами.

import pygame  # Импортирует библиотеку Pygame для работы с графикой и игровыми объектами.

from enemy import Enemy  # Импортирует класс Enemy из файла enemy.py.
from tower import BasicTower, SniperTower, MoneyTower  # Импортирует классы башен из файла tower.py.


class Level:  # Определяет класс Level, который управляет уровнем игры.
    """
    Класс Level управляет уровнем игры, включая волны врагов и расстановку башен.

    Атрибуты:
        game (TowerDefenseGame): Ссылка на основной объект игры.
        enemies (pygame.sprite.Group): Группа врагов.
        towers (pygame.sprite.Group): Группа башен.
        bullets (pygame.sprite.Group): Группа пуль.
        waves (list): Список волн врагов.
        current_wave (int): Индекс текущей волны.
        spawned_enemies (int): Количество заспавненных врагов в текущей волне.
        spawn_delay (int): Задержка между спавном врагов.
        last_spawn_time (int): Время последнего спавна врага.
        all_waves_complete (bool): Флаг, указывающий, что все волны завершены.
        font (pygame.font.Font): Шрифт для отрисовки текста.
        current_path (dict): Текущий путь для врагов с номером.
    """

    def __init__(self, game):  # Конструктор класса Level.
        """
        Инициализация объекта Level.

        Args:
            game (TowerDefenseGame): Основной объект игры.
        """
        self.game = game  # Сохраняет ссылку на основной объект игры.
        self.enemies = pygame.sprite.Group()  # Инициализирует группу для хранения врагов.
        self.towers = pygame.sprite.Group()  # Инициализирует группу для хранения башен.
        self.bullets = pygame.sprite.Group()  # Инициализирует группу для хранения пуль.

        # Выбираем случайный путь для врагов
        self.current_path = random.choice(
            self.game.settings.enemy_paths)  # Выбирает случайный путь для врагов из настроек игры.

        self.waves = [  # Определяет список волн врагов.
            [{'path': self.current_path['path'], 'speed': 1, 'health': 100,  # Первая волна: 5 базовых врагов.
              'image_path': 'assets/enemies/basic_enemy.png'}] * 5,
            [{'path': self.current_path['path'], 'speed': 1.5, 'health': 150,  # Вторая волна: 7 быстрых врагов.
              'image_path': 'assets/enemies/fast_enemy.png'}] * 7,
            [{'path': self.current_path['path'], 'speed': 0.75, 'health': 200,  # Третья волна: 4 сильных врагов.
              'image_path': 'assets/enemies/strong_enemy.png'}] * 4,
        ]
        self.current_wave = 0  # Устанавливает индекс текущей волны на 0.
        self.spawned_enemies = 0  # Устанавливает количество заспавненных врагов на 0.
        self.spawn_delay = 1000  # Устанавливает задержку между спавном врагов (в миллисекундах).
        self.last_spawn_time = pygame.time.get_ticks()  # Записывает время последнего спавна врага.
        self.all_waves_complete = False  # Устанавливает флаг завершения всех волн в False.
        self.start_next_wave()  # Запускает первую волну.
        self.font = pygame.font.SysFont("Arial", 24)  # Загружает шрифт для отображения текста.

    def start_next_wave(self):  # Метод для запуска следующей волны.
        """
        Запускает следующую волну врагов.
        """
        if self.current_wave < len(self.waves):  # Проверяет, есть ли еще волны.
            self.spawned_enemies = 0  # Сбрасывает количество заспавненных врагов.
            self.spawn_next_enemy()  # Спавнит первого врага в новой волне.

    def spawn_next_enemy(self):  # Метод для спавна следующего врага.
        """
        Спавнит следующего врага в текущей волне.
        """
        if self.spawned_enemies < len(self.waves[self.current_wave]):  # Проверяет, есть ли еще враги в текущей волне.
            enemy_info = self.waves[self.current_wave][self.spawned_enemies]  # Получает информацию о следующем враге.
            new_enemy = Enemy(**enemy_info, game=self.game)  # Создает нового врага.
            self.enemies.add(new_enemy)  # Добавляет врага в группу врагов.
            self.spawned_enemies += 1  # Увеличивает счетчик заспавненных врагов.

    def attempt_place_tower(self, mouse_pos, tower_type):  # Метод для попытки размещения башни.
        tower_classes = {  # Словарь с типами башен и их классами.
            'basic': BasicTower,
            'sniper': SniperTower,
            'money': MoneyTower,
        }
        if tower_type in tower_classes and self.game.settings.starting_money >= self.game.settings.tower_cost:  # Проверяет, достаточно ли денег и существует ли тип башни.
            grid_pos = self.game.grid.get_grid_position(mouse_pos)  # Получает координаты клетки сетки по позиции мыши.
            if self.game.grid.is_spot_available(grid_pos):  # Проверяет, доступна ли позиция для размещения башни.
                self.game.settings.starting_money -= self.game.settings.tower_cost  # Уменьшает количество денег на стоимость башни.
                new_tower = tower_classes[tower_type](grid_pos, self.game)  # Создает новую башню.
                self.towers.add(new_tower)  # Добавляет башню в группу башен.
                print("Tower placed.")  # Выводит сообщение о размещении башни.
            else:
                print("Invalid position for tower.")  # Выводит сообщение о недопустимой позиции.
        else:
            print(
                "Not enough money or unknown tower type.")  # Выводит сообщение о недостатке денег или неизвестном типе башни.

    def update(self):  # Метод для обновления состояния уровня.
        """
        Обновляет состояние уровня, включая врагов, башни и пули.
        """
        current_time = pygame.time.get_ticks()  # Получает текущее время.

        if self.current_wave < len(self.waves) and self.spawned_enemies < len(
                self.waves[self.current_wave]):  # Проверяет, есть ли еще враги для спавна.
            if current_time - self.last_spawn_time > self.spawn_delay:  # Проверяет, прошла ли задержка для спавна следующего врага.
                enemy_info = self.waves[self.current_wave][
                    self.spawned_enemies].copy()  # Копирует информацию о следующем враге.
                enemy_info['game'] = self.game  # Добавляет ссылку на игру в информацию о враге.
                new_enemy = Enemy(**enemy_info)  # Создает нового врага.
                self.enemies.add(new_enemy)  # Добавляет врага в группу врагов.
                self.spawned_enemies += 1  # Увеличивает счетчик заспавненных врагов.
                self.last_spawn_time = current_time  # Обновляет время последнего спавна.

        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True,
                                                False)  # Проверяет столкновения между пулями и врагами.
        for bullet in collisions:  # Перебирает все столкнувшиеся пули.
            for enemy in collisions[bullet]:  # Перебирает всех столкнувшихся врагов.
                enemy.take_damage(bullet.damage)  # Наносит урон врагу.

        self.enemies.update()  # Обновляет состояние всех врагов.
        for tower in self.towers:  # Перебирает все башни.
            tower.update(self.enemies, current_time, self.bullets)  # Обновляет состояние башни.
        self.bullets.update()  # Обновляет состояние всех пуль.

        if len(self.enemies) == 0 and self.current_wave < len(
                self.waves) - 1:  # Проверяет, закончилась ли текущая волна.
            self.current_wave += 1  # Переходит к следующей волне.
            self.start_next_wave()  # Запускает следующую волну.
        elif len(self.enemies) == 0 and self.current_wave == len(
                self.waves) - 1:  # Проверяет, закончились ли все волны.
            self.all_waves_complete = True  # Устанавливает флаг завершения всех волн.

    def draw_path(self, screen):  # Метод для отрисовки пути врагов.
        """
        Отрисовывает путь врагов на экране.

        Args:
            screen (pygame.Surface): Поверхность для отрисовки.
        """
        pygame.draw.lines(screen, (0, 128, 0), False, self.current_path['path'], 5)  # Рисует путь врагов.
        for pos in self.game.settings.tower_positions:  # Перебирает все доступные позиции для башен.
            pygame.draw.circle(screen, (128, 0, 0), pos, 10)  # Рисует круги на доступных позициях.

    def draw(self, screen):  # Метод для отрисовки уровня.
        """
        Отрисовывает уровень, включая врагов, башни и пули.

        Args:
            screen (pygame.Surface): Поверхность для отрисовки.
        """
        self.draw_path(screen)  # Отрисовывает путь врагов.
        self.enemies.draw(screen)  # Отрисовывает всех врагов.
        self.towers.draw(screen)  # Отрисовывает все башни.
        self.bullets.draw(screen)  # Отрисовывает все пули.

        # Отображаем номер выбранного пути
        path_number_text = self.font.render(f"Path: {self.current_path['number']}", True,
                                            (255, 255, 255))  # Создает текст с номером пути.
        screen.blit(path_number_text, (10, 130))  # Рисует текст с номером пути на экране.

        mouse_pos = pygame.mouse.get_pos()  # Получает текущую позицию мыши.
        for tower in self.towers:  # Перебирает все башни.
            tower.draw(screen)  # Отрисовывает башню.
            if tower.is_hovered(mouse_pos):  # Проверяет, наведена ли мышь на башню.
                tower_stats_text = self.font.render(f"Damage: {tower.damage}, Range: {tower.tower_range}", True,
                                                    # Создает текст с характеристиками башни.
                                                    (255, 255, 255))
                screen.blit(tower_stats_text,
                            (tower.rect.x, tower.rect.y - 20))  # Рисует текст с характеристиками башни над башней.
