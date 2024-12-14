import pygame


class Grid:
    """
    Класс Grid управляет сеткой, на которой игрок может размещать башни.

    Атрибуты:
        game (TowerDefenseGame): Ссылка на основной объект игры.
        settings (Settings): Настройки игры.
        screen (pygame.Surface): Поверхность для отрисовки.
        available_spots (list): Список доступных позиций для размещения башен.
        towers (list): Список размещённых башен.
        show_spots (bool): Флаг для отображения позиций на сетке.
    """

    def __init__(self, game):
        """
        Инициализация объекта Grid.

        Args:
            game (TowerDefenseGame): Основной объект игры.
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.available_spots = self.settings.tower_positions
        self.towers = []
        self.show_spots = False  # Флаг для отображения позиций

    def update(self):
        """
        Обновление состояния сетки (пока не используется).
        """
        pass

    def draw(self):
        """
        Отрисовка сетки на экране.

        Если флаг show_spots установлен в True, отображаются доступные позиции для размещения башен.
        """
        if self.show_spots:  # Отображаем позиции только если флаг установлен
            for spot in self.available_spots:
                pygame.draw.circle(self.screen, (0, 255, 0), spot, 15, 2)

    def place_tower(self, tower=None):
        """
        Размещение башни на сетке.

        Args:
            tower (Tower): Башня для размещения.

        Returns:
            bool: True, если башня успешно размещена, иначе False.
        """
        grid_pos = self.get_grid_position(tower.position)
        if grid_pos in self.available_spots and not any(tower.rect.collidepoint(grid_pos) for tower in self.towers):
            self.towers.append(tower)
            return True
        return False

    def remove_tower(self, tower):
        """
        Удаление башни с сетки.

        Args:
            tower (Tower): Башня для удаления.
        """
        if tower in self.towers:
            self.towers.remove(tower)

    def get_grid_position(self, mouse_pos):
        """
        Получаем координаты клетки сетки по положению мыши.

        Args:
            mouse_pos (tuple): Координаты мыши (x, y).

        Returns:
            tuple: Центр нажатой клетки сетки.
        """
        grid_x = mouse_pos[0] // 64 * 64 + 32
        grid_y = mouse_pos[1] // 64 * 64 + 32
        return grid_x, grid_y

    def is_spot_available(self, grid_pos):
        """
        Проверяет, доступно ли место для размещения башни.

        Args:
            grid_pos (tuple): Координаты клетки сетки.

        Returns:
            bool: True, если место доступно, иначе False.
        """
        return grid_pos in self.available_spots and all(not tower.rect.collidepoint(grid_pos) for tower in self.towers)
