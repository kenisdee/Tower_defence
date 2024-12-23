import sys  # Импортирует модуль sys для работы с системными функциями.

import pygame  # Импортирует библиотеку Pygame для работы с графикой и игровыми объектами.

from grid import Grid  # Импортирует класс Grid из файла grid.py.
from level import Level  # Импортирует класс Level из файла level.py.
from settings import Settings  # Импортирует класс Settings из файла settings.py.


class TowerDefenseGame:  # Определяет основной класс игры TowerDefenseGame.
    """
    Основной класс игры Tower Defense, управляющий игровым циклом, событиями и отрисовкой.

    Атрибуты:
        settings (Settings): Настройки игры.
        screen (pygame.Surface): Поверхность для отрисовки.
        clock (pygame.time.Clock): Таймер для управления FPS.
        background (pygame.Surface): Фон игры.
        level (Level): Объект уровня.
        grid (Grid): Объект сетки для размещения башен.
        font (pygame.font.Font): Шрифт для текста.
        shoot_sound (pygame.mixer.Sound): Звук выстрела.
        selected_tower_type (str): Выбранный тип башни ('basic' или 'sniper').
        is_game_over (bool): Флаг окончания игры.
    """

    def __init__(self):  # Конструктор класса TowerDefenseGame.
        """
        Инициализация игры.
        """
        pygame.init()  # Инициализирует библиотеку Pygame.
        self.settings = Settings()  # Создает объект настроек игры.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))  # Создает окно игры с заданными размерами.
        pygame.display.set_caption("Tower Defense Game")  # Устанавливает заголовок окна.
        self.clock = pygame.time.Clock()  # Создает объект таймера для управления FPS.

        self.background = pygame.image.load(
            self.settings.background_image).convert()  # Загружает изображение фона игры.
        self.background = pygame.transform.scale(self.background,  # Масштабирует фон до размеров экрана.
                                                 (self.settings.screen_width, self.settings.screen_height))

        self.level = Level(self)  # Создает объект уровня игры.
        self.grid = Grid(self)  # Создает объект сетки для размещения башен.

        self.font = pygame.font.SysFont("Arial", 24)  # Загружает шрифт для отображения текста.

        self.shoot_sound = pygame.mixer.Sound(self.settings.shoot_sound)  # Загружает звук выстрела.
        self.selected_tower_type = 'basic'  # Устанавливает выбранный тип башни по умолчанию.
        self.is_game_over = False  # Устанавливает флаг окончания игры в False.

    def game_over(self):  # Метод для установки флага окончания игры.
        """
        Устанавливает флаг окончания игры.
        """
        self.is_game_over = True  # Устанавливает флаг окончания игры в True.

    def is_position_inside(self, pos):  # Метод для проверки, находится ли позиция внутри игрового экрана.
        """
        Проверяет, находится ли заданная позиция внутри игрового экрана.

        Args:
            pos (tuple): Координаты позиции (x, y).

        Returns:
            bool: True, если позиция находится внутри экрана, иначе False.
        """
        return 0 <= pos[0] <= self.settings.screen_width and 0 <= pos[
            1] <= self.settings.screen_height  # Возвращает True, если позиция находится внутри экрана.

    def _check_events(self):  # Метод для обработки событий, таких как нажатия клавиш и клики мыши.
        """
        Обрабатывает события, такие как нажатия клавиш и клики мыши.
        """
        for event in pygame.event.get():  # Перебирает все события в очереди.
            if event.type == pygame.QUIT:  # Проверяет, была ли нажата кнопка закрытия окна.
                pygame.quit()  # Завершает работу Pygame.
                sys.exit()  # Завершает выполнение программы.
            elif event.type == pygame.KEYDOWN:  # Проверяет, была ли нажата клавиша.
                if event.key == pygame.K_1:  # Проверяет, была ли нажата клавиша '1'.
                    self.selected_tower_type = 'basic'  # Устанавливает выбранный тип башни на 'basic'.
                    print("Selected basic tower.")  # Выводит сообщение в консоль.
                elif event.key == pygame.K_2:  # Проверяет, была ли нажата клавиша '2'.
                    self.selected_tower_type = 'sniper'  # Устанавливает выбранный тип башни на 'sniper'.
                    print("Selected sniper tower.")  # Выводит сообщение в консоль.
                elif event.key == pygame.K_3:  # Проверяет, была ли нажата клавиша '3'.
                    self.selected_tower_type = 'money'  # Устанавливает выбранный тип башни на 'money'.
                    print("Selected money tower.")  # Выводит сообщение в консоль.
                elif event.key == pygame.K_SPACE:  # Проверяет, была ли нажата клавиша 'Пробел'.
                    self.grid.show_spots = not self.grid.show_spots  # Переключает флаг отображения позиций на сетке.
                    print("Show spots:", self.grid.show_spots)  # Выводит сообщение в консоль.
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Проверяет, была ли нажата кнопка мыши.
                if event.button == 1:  # Проверяет, была ли нажата левая кнопка мыши.
                    if self.selected_tower_type:  # Проверяет, выбран ли тип башни.
                        mouse_pos = pygame.mouse.get_pos()  # Получает текущую позицию мыши.
                        self.level.attempt_place_tower(mouse_pos,
                                                       self.selected_tower_type)  # Пытается разместить башню.
                    else:
                        print("No tower type selected.")  # Выводит сообщение, если тип башни не выбран.
                elif event.button == 3:  # Проверяет, была ли нажата правая кнопка мыши.
                    mouse_pos = pygame.mouse.get_pos()  # Получает текущую позицию мыши.
                    for tower in self.level.towers:  # Перебирает все башни.
                        if tower.is_hovered(mouse_pos):  # Проверяет, наведена ли мышь на башню.
                            tower.upgrade()  # Улучшает башню.

    def _update_game(self):  # Метод для обновления состояния игры.
        """
        Обновляет состояние игры, включая уровень и сетку.
        """
        self.level.update()  # Обновляет состояние уровня.
        self.grid.update()  # Обновляет состояние сетки.

    def _draw_win_screen(self):  # Метод для отрисовки экрана победы.
        """
        Отрисовывает экран победы.
        """
        win_text = "You Win!"  # Текст для экрана победы.
        win_render = self.font.render(win_text, True, (255, 215, 0))  # Создает изображение текста.
        win_rect = win_render.get_rect(
            center=(self.settings.screen_width / 2, self.settings.screen_height / 2))  # Центрирует текст на экране.
        self.screen.blit(win_render, win_rect)  # Рисует текст на экране.

    def _draw_game_over_screen(self):  # Метод для отрисовки экрана проигрыша.
        """
        Отрисовывает экран проигрыша.
        """
        self.screen.fill((0, 0, 0))  # Заполняет экран черным цветом.

        game_over_text = "Game Over!"  # Текст для экрана проигрыша.
        game_over_render = self.font.render(game_over_text, True, (255, 0, 0))  # Создает изображение текста.
        game_over_rect = game_over_render.get_rect(  # Центрирует текст на экране.
            center=(self.settings.screen_width / 2, self.settings.screen_height / 2))

        self.screen.blit(game_over_render, game_over_rect)  # Рисует текст на экране.

    def _draw(self):  # Метод для отрисовки всех элементов игры.
        """
        Отрисовывает все элементы игры на экране.
        """
        if self.is_game_over:  # Проверяет, закончилась ли игра.
            self._draw_game_over_screen()  # Отрисовывает экран проигрыша.
        else:
            self.screen.blit(self.background, (0, 0))  # Рисует фон игры.
            self.level.draw(self.screen)  # Отрисовывает уровень.
            self.grid.draw()  # Отрисовывает сетку.

            money_text = self.font.render(f"Money: ${self.settings.starting_money}", True,
                                          (255, 255, 255))  # Создает текст с количеством денег.
            tower_text = self.font.render(  # Создает текст с выбранным типом башни.
                f"Selected Tower: {self.selected_tower_type if self.selected_tower_type else 'None'}", True,
                (255, 255, 255))
            waves_text = self.font.render(f"Waves Left: {len(self.level.waves) - self.level.current_wave}", True,
                                          # Создает текст с количеством оставшихся волн.
                                          (255, 255, 255))
            enemies_text = self.font.render(f"Enemies Left: {len(self.level.enemies)}", True,
                                            (255, 255, 255))  # Создает текст с количеством оставшихся врагов.

            self.screen.blit(money_text, (10, 10))  # Рисует текст с количеством денег.
            self.screen.blit(tower_text, (10, 40))  # Рисует текст с выбранным типом башни.
            self.screen.blit(waves_text, (10, 70))  # Рисует текст с количеством оставшихся волн.
            self.screen.blit(enemies_text, (10, 100))  # Рисует текст с количеством оставшихся врагов.

            if self.level.all_waves_complete:  # Проверяет, завершены ли все волны.
                self._draw_win_screen()  # Отрисовывает экран победы.

        pygame.display.flip()  # Обновляет экран.

    def run_game(self):  # Метод для запуска основного игрового цикла.
        """
        Запускает основной игровой цикл.
        """
        while True:  # Бесконечный цикл игры.
            self._check_events()  # Обрабатывает события.
            self._update_game()  # Обновляет состояние игры.

            if len(self.level.enemies) == 0 and not self.level.all_waves_complete:  # Проверяет, закончилась ли текущая волна.
                self.level.start_next_wave()  # Запускает следующую волну.

            self._draw()  # Отрисовывает все элементы игры.
            self.clock.tick(60)  # Ограничивает FPS до 60.


if __name__ == '__main__':  # Проверяет, запущен ли файл напрямую.
    td_game = TowerDefenseGame()  # Создает объект игры.
    td_game.run_game()  # Запускает игру.
