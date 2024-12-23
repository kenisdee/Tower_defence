import pygame  # Импортирует библиотеку Pygame для работы с графикой и игровыми объектами.


class Grid:  # Определяет класс Grid, который управляет сеткой для размещения башен.
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

    def __init__(self, game):  # Конструктор класса Grid.
        """
        Инициализация объекта Grid.

        Args:
            game (TowerDefenseGame): Основной объект игры.
        """
        self.game = game  # Сохраняет ссылку на основной объект игры.
        self.settings = game.settings  # Сохраняет настройки игры.
        self.screen = game.screen  # Сохраняет поверхность для отрисовки.
        self.available_spots = self.settings.tower_positions  # Загружает список доступных позиций для размещения башен из настроек.
        self.towers = []  # Инициализирует пустой список для хранения размещённых башен.
        self.show_spots = False  # Инициализирует флаг для отображения позиций на сетке (по умолчанию выключен).

    def update(self):  # Метод для обновления состояния сетки (пока не используется).
        """
        Обновление состояния сетки (пока не используется).
        """
        pass  # Просто пропускает выполнение, так как метод пока не используется.

    def draw(self):  # Метод для отрисовки сетки на экране.
        """
        Отрисовка сетки на экране.

        Если флаг show_spots установлен в True, отображаются доступные позиции для размещения башен.
        """
        if self.show_spots:  # Проверяет, нужно ли отображать доступные позиции.
            for spot in self.available_spots:  # Перебирает все доступные позиции.
                pygame.draw.circle(self.screen, (0, 255, 0), spot, 15,
                                   2)  # Рисует круг (позицию) на экране зеленым цветом.

    def place_tower(self, tower=None):  # Метод для размещения башни на сетке.
        """
        Размещение башни на сетке.

        Args:
            tower (Tower): Башня для размещения.

        Returns:
            bool: True, если башня успешно размещена, иначе False.
        """
        grid_pos = Grid.get_grid_position(
            tower.position)  # Получает координаты клетки сетки, на которую указывает башня.
        if grid_pos in self.available_spots and not any(tower.rect.collidepoint(grid_pos) for tower in
                                                        self.towers):  # Проверяет, доступна ли позиция и не занята ли она другой башней.
            self.towers.append(tower)  # Добавляет башню в список размещённых башен.
            return True  # Возвращает True, если башня успешно размещена.
        return False  # Возвращает False, если башня не может быть размещена.

    def remove_tower(self, tower):  # Метод для удаления башни с сетки.
        """
        Удаление башни с сетки.

        Args:
            tower (Tower): Башня для удаления.
        """
        if tower in self.towers:  # Проверяет, есть ли башня в списке размещённых башен.
            self.towers.remove(tower)  # Удаляет башню из списка.

    @staticmethod
    def get_grid_position(mouse_pos):  # Статический метод для получения координат клетки сетки по положению мыши.
        """
        Получаем координаты клетки сетки по положению мыши.

        Args:
            mouse_pos (tuple): Координаты мыши (x, y).

        Returns:
            tuple: Центр нажатой клетки сетки.
        """
        grid_x = mouse_pos[0] // 64 * 64 + 32  # Вычисляет координату x клетки сетки.
        grid_y = mouse_pos[1] // 64 * 64 + 32  # Вычисляет координату y клетки сетки.
        return grid_x, grid_y  # Возвращает координаты центра клетки сетки.

    def is_spot_available(self, grid_pos):  # Метод для проверки доступности позиции на сетке.
        """
        Проверяет, доступно ли место для размещения башни.

        Args:
            grid_pos (tuple): Координаты клетки сетки.

        Returns:
            bool: True, если место доступно, иначе False.
        """
        return grid_pos in self.available_spots and all(not tower.rect.collidepoint(grid_pos) for tower in
                                                        self.towers)  # Возвращает True, если позиция доступна и не занята другой башней.
