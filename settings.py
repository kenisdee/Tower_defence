class Settings:
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

    def __init__(self):
        """
        Инициализация объекта Settings.
        """
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.rows = 10
        self.cols = 15
        self.grid_size = (64, 64)

        self.tower_cost = 100
        self.money_tower_cost = 200
        self.tower_upgrade_cost = 150
        self.tower_sell_percentage = 0.75

        self.enemy_paths = [
            {
                'number': 1,
                'path': [(50, 400), (200, 400), (200, 300), (400, 300), (400, 500), (700, 500), (700, 400), (1150, 400)]
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

        self.tower_sprites = {
            'basic': 'assets/towers/basic_tower.png',
            'sniper': 'assets/towers/sniper_tower.png',
            'money': 'assets/towers/money_tower.png',
        }
        self.enemy_sprite = 'assets/enemies/basic_enemy.png'
        self.bullet_sprite = 'assets/bullets/basic_bullet.png'
        self.background_image = 'assets/backgrounds/game_background.png'

        # Звуки
        self.shoot_sound = 'assets/sounds/shoot.mp3'
        self.enemy_spawn_sound = 'assets/sounds/enemy_spawn.mp3'
        self.upgrade_sound = 'assets/sounds/upgrade.wav'
        self.sell_sound = 'assets/sounds/sell.wav'
        self.enemy_hit_sound = 'assets/sounds/enemy_hit.wav'
        self.background_music = 'assets/sounds/background_music.mp3'

        self.starting_money = 500
        self.lives = 20

        self.tower_positions = [
            (x * self.grid_size[0] + self.grid_size[0] // 2, y * self.grid_size[1] + self.grid_size[1] // 2)
            for x in range(1, self.cols) for y in range(3, self.rows)]
