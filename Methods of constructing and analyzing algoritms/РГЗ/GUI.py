import os
import time
import wx
import RRT


ADD_OBSTACLE = 1
ADD_START_POINT = 2
ADD_END_POINT = 3
LAUNCH_RRT = 4
LAUNCH_BEST_PATH = 5

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        # Инициализация пользовательского окна
        super().__init__(parent=parent, size=(1200, 800), pos=(100, 100), title=title,
                         style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)

        # Инициализация меню
        menu_bar = wx.MenuBar()

        # Вкладка меню "Файл" и её компоненты
        self.file_menu = wx.Menu()
        file_item_save = self.file_menu.Append(wx.ID_SAVE, '&Сохранить\tCtrl+S', 'Сохранить сцену как .png')
        file_item_exit = self.file_menu.Append(wx.ID_EXIT, '&Выход\tCtrl+Q', 'Выход из приложения')

        # Вкладка меню "Добавить" и её компоненты
        self.add_menu = wx.Menu()
        add_item_start_point = self.add_menu.Append(ADD_START_POINT, '&Начальная точка\tCtrl+1', 'Добавить начальную точку пути')
        add_item_end_point = self.add_menu.Append(ADD_END_POINT, '&Конечная точка\tCtrl+2', 'Добавить конечную точку пути')
        add_item_obstacle = self.add_menu.Append(ADD_OBSTACLE, '&Препятствие\tCtrl+3', 'Добавить препятствие')

        # Вкладка меню "Запустить" и её компоненты
        self.launch = wx.Menu()
        launch_RRT = self.launch.Append(LAUNCH_RRT, '&Построить все пути\tCtrl+P', 'Построить все возможные пути')
        launch_best_path = self.launch.Append(LAUNCH_BEST_PATH, '&Построить кратчайший путь\tCtrl+B', 'Построить кратчайший путь из начальной в конечную точку')

        # Добавление всех вкладок и их компонентов в меню
        menu_bar.Append(self.file_menu, 'Файл')
        menu_bar.Append(self.add_menu, 'Добавить')
        menu_bar.Append(self.launch, 'Запустить')
        self.SetMenuBar(menu_bar)

        # События в меню
        self.Bind(wx.EVT_MENU, self.onQuit, file_item_exit)                     # Выход
        self.Bind(wx.EVT_MENU, self.onSave, file_item_save)                     # Сохранение

        self.Bind(wx.EVT_MENU, self.onAddStartPoint, add_item_start_point)      # Добавление нач. точки
        self.Bind(wx.EVT_MENU, self.onAddEndPoint, add_item_end_point)          # Добавление кон. точки
        self.Bind(wx.EVT_MENU, self.onAddObstacle, add_item_obstacle)           # Добавление препятствия

        self.Bind(wx.EVT_MENU, self.onLaunchRRT, launch_RRT)                    # Построение вершин дерева
        self.Bind(wx.EVT_MENU, self.onLaunchBestPath, launch_best_path)         # Поиск и построение кратчайшего пути

        # Переменные класса
        self.start_point_pos = (-1, -1)         # Координаты нач. точки
        self.end_point_pos = (-1, -1)           # Кординаты кон. точки
        self.obstacle = []                      # Координаты одного препятствия
        self.obstacles = []                     # Координаты препятствий (одно препятствие = две точки; из них прямоугольник)
        self.iterations_num = 0                 # Количество итераций получения случайных точек на поле
        self.step_size = 0                      # Шаг (размер) между вершинами графа
        self.best_path_flag = False             # Флаг на то, что получилось построить кратчайший путь
        self.rrt = None                         # Объект класса RRTAlgorithm

        # Инициализация "битовой карты" (для сохранения сцены как .bmp)
        self.btm = wx.Bitmap((1184, 742))
        self.btm_dc = wx.MemoryDC()
        self.btm_dc.SelectObject(self.btm)
        self.Bind(wx.EVT_PAINT, self.onPaintBorder)

    def onQuit(self, event):
        # Событие на выход из приложения
        dlg = wx.MessageDialog(self, 'Вы дейстительно хотите выйти из программы?', 'Выход', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        res = dlg.ShowModal()
        if res == wx.ID_YES:
            self.Close()

    def onSave(self, event):
        # Событие на сохранение файла
        path = os.path.abspath(__file__)
        file_name = os.path.basename(__file__)
        path = path[0:len(path)-len(file_name)]
        dlg = wx.MessageDialog(self, f'Файл сохранен в {path}img.bmp', 'Сохранить', wx.OK_DEFAULT)
        dlg.ShowModal()
        self.btm.SaveFile('img.bmp', wx.BITMAP_TYPE_BMP)

    def onAddStartPoint(self, event):
        # Событие на добавление стартовой точки
        #dlg = wx.MessageDialog(self, 'Кликните в любом месте поля для добавления начальной точки', 'Добавить начальную точку', wx.OK_DEFAULT)
        #dlg.ShowModal()
        self.add_menu.Delete(ADD_START_POINT)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseClick)

    def onAddEndPoint(self, event):
        # Событие на добавление конечной точки
        #dlg = wx.MessageDialog(self, 'Кликните в любом месте поля для добавления конечной точки', 'Добавить конечную точку', wx.OK_DEFAULT)
        #dlg.ShowModal()
        self.add_menu.Delete(ADD_END_POINT)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseClick)

    def onAddObstacle(self, event):
        # Событие на добавление препятствий
        #if len(self.obstacles) == 0:
            #dlg = wx.MessageDialog(self, 'Кликните в двух любых местах поля для добавления препятствия в виде прямоугольника (эти две точки - диагональ прямоугольника)', 'Добавить препятствие', wx.OK_DEFAULT)
            #dlg.ShowModal()
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseClick)

    def onMouseClick(self, event):
        # Событие на получение координат мыши при клике по сцене
        pos = event.GetPosition()
        if pos.x < 20:
            pos.x = 20
        if pos.x > 20 + 1144:
            pos.x = 20 + 1144
        if pos.y < 20:
            pos.y = 20
        if pos.y > 20 + 702:
            pos.y = 20 + 702
        if self.add_menu.FindItemById(ADD_START_POINT) == None and self.start_point_pos == (-1, -1):
            self.start_point_pos = (pos.x, pos.y)
            wx.CallLater(10, self.onPaintDot)
            self.Unbind(event=wx.EVT_LEFT_DOWN)
        elif self.add_menu.FindItemById(ADD_END_POINT) == None and self.end_point_pos == (-1, -1):
            self.end_point_pos = (pos.x, pos.y)
            wx.CallLater(10, self.onPaintDot)
            self.Unbind(event=wx.EVT_LEFT_DOWN)
        else:
            self.obstacle.append((pos.x, pos.y))
            if len(self.obstacle) == 2:
                self.obstacles.append(self.obstacle)
                wx.CallLater(10, self.onPaintRect)
                self.obstacle = []
                self.Unbind(event=wx.EVT_LEFT_DOWN)

    def onPaintBorder(self, event):
        # Событие на отрисовку границы поля, в пределах которого будут все объекты
        dc = wx.PaintDC(self)
        self.btm_dc.SetPen(wx.Pen(wx.BLACK, 2))
        self.btm_dc.SetBrush(wx.Brush(wx.GREY_BRUSH))
        self.btm_dc.DrawRectangle(-1, -1, 1187, 745)
        self.btm_dc.DrawRectangle(18, 18, 1147, 705)
        dc.Blit(0, 0, 1200, 800, self.btm_dc, 0, 0)

    def onPaintDot(self):
        # Событие на отрисовку начальной/конечной точки
        dc = wx.ClientDC(self)
        self.btm_dc.SetPen(wx.Pen(wx.RED, 15))
        if self.start_point_pos != (-1, -1):
            if self.end_point_pos == (-1, -1):
                self.btm_dc.DrawLine(self.start_point_pos[0], self.start_point_pos[1], self.start_point_pos[0], self.start_point_pos[1])
            else:
                self.btm_dc.DrawLine(self.start_point_pos[0], self.start_point_pos[1], self.start_point_pos[0], self.start_point_pos[1])
                self.btm_dc.DrawLine(self.end_point_pos[0], self.end_point_pos[1], self.end_point_pos[0], self.end_point_pos[1])
        elif self.end_point_pos != (-1, -1):
            self.btm_dc.DrawLine(self.end_point_pos[0], self.end_point_pos[1], self.end_point_pos[0], self.end_point_pos[1])
        dc.Blit(0, 0, 1200, 800, self.btm_dc, 0, 0)

    def onPaintRect(self):
        # Событие на отрисовку препятствия в виде прямоугольника
        dc = wx.ClientDC(self)
        self.btm_dc.SetPen(wx.Pen(wx.BLUE, 1))
        self.btm_dc.SetBrush(wx.Brush(wx.BLUE))
        obstacle = self.obstacles[len(self.obstacles) - 1]
        x = min(obstacle[0][0], obstacle[1][0]) + 1
        y = min(obstacle[0][1], obstacle[1][1]) + 1
        len_x = max(obstacle[0][0], obstacle[1][0]) - x - 1
        len_y = max(obstacle[0][1], obstacle[1][1]) - y - 1
        self.btm_dc.DrawRectangle(x, y, len_x, len_y)
        wx.CallLater(10, self.onPaintDot)
        dc.Blit(0, 0, 1200, 800, self.btm_dc, 0, 0)

    def onLaunchRRT(self, event):
        # Построение вершин дерева, если заданы начальная и конечная точки
        if self.start_point_pos == (-1, -1) or self.end_point_pos == (-1, -1):
            dlg = wx.MessageDialog(self, 'Сначала нужно добавить начальную и конечную точки', 'Ошибка', wx.OK_DEFAULT)
            dlg.ShowModal()
        else:
            # Ввод количества итераций цикла фукнции RRT
            dlg = wx.TextEntryDialog(self, 'Введите количество итераций', 'Ввод данных', '1000')
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                try:
                    iterations_num = int(dlg.GetValue())
                    if iterations_num <= 0:
                        dlg_err = wx.MessageDialog(self, 'Неверное количество итераций', 'Ошибка', wx.OK_DEFAULT)
                        dlg_err.ShowModal()
                        return
                    self.iterations_num = iterations_num
                except Exception as e:
                    dlg_err = wx.MessageDialog(self, 'Неверное количество итераций', 'Ошибка', wx.OK_DEFAULT)
                    dlg_err.ShowModal()
                    return
            else:
                return
            # Ввод размера шага (размера) ветви
            dlg = wx.TextEntryDialog(self, 'Введите размер шага\n(Размер поля 1164×702)', 'Ввод данных', '30')
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                try:
                    step_size = int(dlg.GetValue())
                    if step_size <= 0:
                        dlg_err = wx.MessageDialog(self, 'Неверный размер шага', 'Ошибка', wx.OK_DEFAULT)
                        dlg_err.ShowModal()
                        return
                    self.step_size = step_size
                except Exception as e:
                    dlg_err = wx.MessageDialog(self, 'Неверный размер шага', 'Ошибка', wx.OK_DEFAULT)
                    dlg_err.ShowModal()
                    return
            else:
                return
            # Отрисовка построенного дерева дерева
            dc = wx.ClientDC(self)
            self.btm_dc.SetBrush(wx.Brush(wx.TRANSPARENT_BRUSH))
            self.btm_dc.SetPen(wx.Pen('#fdc073', 3, wx.LONG_DASH))
            if self.step_size < 15:
                step = 15
            elif self.step_size > 30:
                step = 30
            else:
                step = self.step_size
            self.btm_dc.DrawRectangle(self.end_point_pos[0] - step - 1, self.end_point_pos[1] - step - 1, step*2 + 3, step*2 + 3)
            self.btm_dc.SetPen(wx.Pen(wx.RED, 15))
            self.btm_dc.DrawLine(self.end_point_pos[0], self.end_point_pos[1], self.end_point_pos[0], self.end_point_pos[1])
            dc.Blit(0, 0, 1200, 800, self.btm_dc, 0, 0)
            self.rrt = RRT.RRTAlgorithm(self.start_point_pos, self.end_point_pos, self.iterations_num, self.step_size, self.obstacles)
            self.rrt.RRT()
            for p1 in self.rrt.tree_nodes:
                for p2 in p1.children:
                    self.btm_dc.SetPen(wx.Pen('#ffffff', 3))
                    self.btm_dc.DrawLine(p1.x, p1.y, p2.x, p2.y)
                    self.btm_dc.SetPen(wx.Pen(wx.RED, 15))
                    self.btm_dc.DrawLine(self.start_point_pos[0], self.start_point_pos[1], self.start_point_pos[0], self.start_point_pos[1])
                    self.btm_dc.DrawLine(self.end_point_pos[0], self.end_point_pos[1], self.end_point_pos[0], self.end_point_pos[1])
                    dc.Blit(0, 0, 1200, 800, self.btm_dc, 0, 0)
                    time_sleep = 0.1 / self.iterations_num
                    #time.sleep(time_sleep)
            self.btm_dc.SetPen(wx.Pen(wx.BLACK, 5))
            dots = self.rrt.definePointsInGoalRadius()
            if len(dots) != 0:
                self.best_path_flag = True
            dlg = wx.MessageDialog(self, 'Все пути построены', 'Готово', wx.OK_DEFAULT)
            dlg.ShowModal()

    def onLaunchBestPath(self, event):
        # Построение и отрисовка кратчайшего пути по вершинам дерева, если те уже построены
        if self.rrt != None and self.best_path_flag == True:
            dc = wx.ClientDC(self)
            best_path = self.rrt.buildBestPath()
            for i in range(len(best_path) - 1):
                self.btm_dc.SetPen(wx.Pen(wx.GREEN, 5))
                self.btm_dc.DrawLine(best_path[i][0], best_path[i][1], best_path[i+1][0], best_path[i+1][1])
                self.btm_dc.SetPen(wx.Pen(wx.RED, 15))
                self.btm_dc.DrawLine(self.start_point_pos[0], self.start_point_pos[1], self.start_point_pos[0], self.start_point_pos[1])
                dc.Blit(0, 0, 1200, 800, self.btm_dc, 0, 0)
                time.sleep(0.1)
            self.btm_dc.SetPen(wx.Pen(wx.GREEN, 5))
            self.btm_dc.DrawLine(best_path[len(best_path) - 1][0], best_path[len(best_path) - 1][1], self.end_point_pos[0], self.end_point_pos[1])
            self.btm_dc.SetPen(wx.Pen(wx.RED, 15))
            self.btm_dc.DrawLine(self.end_point_pos[0], self.end_point_pos[1], self.end_point_pos[0], self.end_point_pos[1])
            dc.Blit(0, 0, 1200, 800, self.btm_dc, 0, 0)
            dlg = wx.MessageDialog(self, 'Кратчайший путь построен', 'Готово', wx.OK_DEFAULT)
            dlg.ShowModal()
        elif self.best_path_flag == False:
            dlg = wx.MessageDialog(self, 'Не удалось построить кратчайший путь', 'Ошибка', wx.OK_DEFAULT)
            dlg.ShowModal()
        else:
            dlg = wx.MessageDialog(self, 'Сначала запустите построение всех путей', 'Ошибка', wx.OK_DEFAULT)
            dlg.ShowModal()



app = wx.App()

frame = MyFrame(None, 'RRT algorithm')
frame.Show()

app.MainLoop()

