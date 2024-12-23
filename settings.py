class Settings:  # Определяет класс Settings, который содержит конфигурационные параметры игры.
    """
    Класс Settings содержит конфигурационные параметры игры.

    Атрибуты:
        screen_width (int): Ширина игрового экрана.
        screen_height (int): Высота игрового экрана.
        bg_color (tuple): Цвет фона игрового экрана в формате RGB.
        rows (int): Количество строк сетки.
        cols (int): Количество столбцов сетки.
        grid_size (tuple): Размер одной клетки сетки (ширина, высота).
        tower_cost (int): Стоимость башни.
        tower_upgrade_cost (int): Стоимость улучшения башни.
        tower_sell_percentage (float): Процент возврата денег при продаже башни.
        enemy_path (list): Список координат, по которым движутся враги.
        tower_sprites (dict): Словарь с путями к изображениям башен.
        enemy_sprite (str): Путь к изображению врага.
        bullet_sprite (str): Путь к изображению пули.
        background_image (str): Путь к фоновому изображению.
        shoot_sound (str): Путь к звуку выстрела.
        enemy_spawn_sound (str): Путь к звуку появления врага.
        upgrade_sound (str): Путь к звуку улучшения.
        sell_sound (str): Путь к звуку продажи.
        enemy_hit_sound (str): Путь к звуку попадания по врагу.
        background_music (str): Путь к фоновой музыке.
        starting_money (int): Стартовая сумма денег у игрока.
        lives (int): Количество жизней игрока.
        tower_positions (list): Список координат, где можно размещать башни.
    """

    def __init__(self):  # Конструктор класса Settings.
        """
        Инициализация объекта Settings.
        """
        self.screen_width = 1200  # Устанавливает ширину игрового экрана.
        self.screen_height = 800  # Устанавливает высоту игрового экрана.
        self.bg_color = (230, 230, 230)  # Устанавливает цвет фона игрового экрана в формате RGB.

        self.rows = 10  # Устанавливает количество строк сетки.
        self.cols = 15  # Устанавливает количество столбцов сетки.
        self.grid_size = (64, 64)  # Устанавливает размер одной клетки сетки (ширина, высота).

        self.tower_cost = 100  # Устанавливает стоимость башни.
        self.money_tower_cost = 200  # Устанавливает стоимость башни, генерирующей деньги.
        self.tower_upgrade_cost = 150  # Устанавливает стоимость улучшения башни.
        self.tower_sell_percentage = 0.75  # Устанавливает процент возврата денег при продаже башни.

        self.enemy_paths = [  # Определяет список путей для врагов.
            {
                'number': 1,  # Номер пути.
                'path': [(50, 400), (200, 400), (200, 300), (400, 300), (400, 500), (700, 500), (700, 400), (1150, 400)]
                # Координаты пути.
            },
            {
                'number': 2,
                'path': [(50, 400), (300, 400), (300, 600), (600, 600), (600, 200), (900, 200), (900, 500), (1150, 500)]
            },
            {
                'number': 3,
                'path': [(50, 400), (300, 400), (300, 200), (600, 200), (600, 600), (900, 600), (900, 300), (1150, 300)]
            },
            {
                'number': 4,
                'path': [(50, 400), (200, 400), (200, 500), (400, 500), (400, 300), (600, 300), (600, 400), (1150, 400)]
            },
            {
                'number': 5,
                'path': [(50, 400), (300, 400), (300, 200), (600, 200), (600, 600), (900, 600), (900, 300), (1150, 300)]
            },
            {
                'number': 6,
                'path': [(50, 400), (150, 400), (150, 500), (350, 500), (350, 300), (550, 300), (550, 400), (1150, 400)]
            },
            {
                'number': 7,
                'path': [(50, 400), (100, 400), (100, 500), (300, 500), (300, 300), (500, 300), (500, 400), (1150, 400)]
            },
            {
                'number': 8,
                'path': [(50, 400), (100, 400), (100, 500), (300, 500), (300, 300), (500, 200), (500, 400), (1150, 500)]
            },
        ]

        self.tower_sprites = {  # Определяет словарь с путями к изображениям башен.
            'basic': 'assets/towers/basic_tower.png',  # Путь к изображению базовой башни.
            'sniper': 'assets/towers/sniper_tower.png',  # Путь к изображению снайперской башни.
            'money': 'assets/towers/money_tower.png',  # Путь к изображению башни, генерирующей деньги.
        }
        self.enemy_sprite = 'assets/enemies/basic_enemy.png'  # Путь к изображению врага.
        self.bullet_sprite = 'assets/bullets/basic_bullet.png'  # Путь к изображению пули.
        self.background_image = 'assets/backgrounds/game_background.png'  # Путь к фоновому изображению.

        # Звуки
        self.shoot_sound = 'assets/sounds/shoot.mp3'  # Путь к звуку выстрела.
        self.enemy_spawn_sound = 'assets/sounds/enemy_spawn.mp3'  # Путь к звуку появления врага.
        self.upgrade_sound = 'assets/sounds/upgrade.wav'  # Путь к звуку улучшения.
        self.sell_sound = 'assets/sounds/sell.wav'  # Путь к звуку продажи.
        self.enemy_hit_sound = 'assets/sounds/enemy_hit.wav'  # Путь к звуку попадания по врагу.
        self.background_music = 'assets/sounds/background_music.mp3'  # Путь к фоновой музыке.

        self.starting_money = 500  # Устанавливает стартовую сумму денег у игрока.
        self.lives = 20  # Устанавливает количество жизней игрока.

        self.tower_positions = [  # Определяет список координат, где можно размещать башни.
            (x * self.grid_size[0] + self.grid_size[0] // 2, y * self.grid_size[1] + self.grid_size[1] // 2)
            # Вычисляет координаты для каждой клетки сетки.
            for x in range(1, self.cols) for y in
            range(3, self.rows)]  # Перебирает строки и столбцы сетки, начиная с 1 и 3 соответственно.
