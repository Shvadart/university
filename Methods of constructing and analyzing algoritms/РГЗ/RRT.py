import random
import math
import sys


class TreeNode:
    # Вершина дерева
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.children = []
        self.parent = parent


class RRTAlgorithm:
    def __init__(self, start, goal, iterations_num, step_size, obstacles):
        # Инициализация дерева
        self.start = start
        self.goal = goal
        self.step_size = step_size
        self.iterations_num = iterations_num
        self.obstacles = obstacles
        self.tree_nodes = []
        self.tree_nodes.append(TreeNode(self.start[0], self.start[1], None))

    def randPoint(self):
        # Генерация случайной точки
        flag = True
        while flag:
            point = (random.randint(20, 1164), random.randint(20, 722))
            flag = False
            for node in self.tree_nodes:
                if node.x == point[0] and node.y == point[1]:
                    flag = True
        return point

    def ifInObstacle(self, p):
        # Проверка: находится ли точка внутри препятствия
        for obstacle in self.obstacles:
            left_border = min(obstacle[0][0], obstacle[1][0])
            up_border = max(obstacle[0][1], obstacle[1][1])
            right_border = max(obstacle[0][0], obstacle[1][0])
            bottom_border = min(obstacle[0][1], obstacle[1][1])
            if p[0] > left_border and p[0] < right_border and p[1] < up_border and p[1] > bottom_border:
                return True
        return False

    def ifCollision(self, p1, p2):
        # Проверка: есть ли коллизия между отрезком и заданными препятствиями (если да, вернет еще препятствие)
        for obstacle in self.obstacles:
            p_border1 = (min(obstacle[0][0], obstacle[1][0]), min(obstacle[0][1], obstacle[1][1]))
            p_border2 = (min(obstacle[0][0], obstacle[1][0]), max(obstacle[0][1], obstacle[1][1]))
            p_border3 = (max(obstacle[0][0], obstacle[1][0]), max(obstacle[0][1], obstacle[1][1]))
            p_border4 = (max(obstacle[0][0], obstacle[1][0]), min(obstacle[0][1], obstacle[1][1]))
            x1 = p1[0]
            y1 = p1[1]
            x2 = p2[0]
            y2 = p2[1]
            if self.linesCollisionPoint(x1, y1, x2, y2, p_border1[0], p_border1[1], p_border2[0], p_border2[1]) != (-1, -1) or \
                self.linesCollisionPoint(x1, y1, x2, y2, p_border2[0], p_border2[1], p_border3[0], p_border3[1]) != (-1, -1) or \
                self.linesCollisionPoint(x1, y1, x2, y2, p_border3[0], p_border3[1], p_border4[0], p_border4[1]) != (-1, -1) or \
                self.linesCollisionPoint(x1, y1, x2, y2, p_border4[0], p_border4[1], p_border1[0], p_border1[1]) != (-1, -1):
                return [True, obstacle]
        return [False, '']

    def linesCollisionPoint(self, x1, y1, x2, y2, x3, y3, x4, y4):
        # Проверка: пересечение двух отрезков (если да, вернет точку пересечения, если нет - (-1, -1))
        if y2 - y1 != 0:
            q = (x2 - x1) / (y1 - y2)
            s = (x3 - x4) + (y3 - y4)*q
            if s == 0:
                return (-1, -1)
            f = (x3 - x1) + (y3 - y1)*q
            k = f / s
        else:
            if y3 - y4 == 0:
                return (-1, -1)
            k = (y3 - y1) / (y3 - y4)
        p_x = x3 + (x4 - x3)*k
        p_y = y3 + (y4 - y3)*k
        if p_x <= max(x1, x2) and p_x >= min(x1, x2) and p_y <= max(y1, y2) and p_y >= min(y1, y2) \
            and p_x <= max(x3, x4) and p_x >= min(x3, x4) and p_y <= max(y3, y4) and p_y >= min(y3, y4):
            return (p_x, p_y)
        else:
            return (-1, -1)

    def nearestPointFromTree(self, p):
        # Вовзращает ближайшую вершину из дерева к точке (либо вершина, либо точка на ветви)
        # Поиск ближайшей вершины
        min_length_to_node = 1000000000
        min_node = None
        if len(self.tree_nodes) == 1:
            return [(self.tree_nodes[0].x, self.tree_nodes[0].y), 'first_point']
        for node in self.tree_nodes:
            length = math.sqrt(abs(node.x - p[0])**2 + abs(node.y - p[1])**2)
            if length < min_length_to_node:
                min_length_to_node = length
                min_node = node
        # Поиск ближайшей точки на ветви между потомками ближайшей вершины и этой вершины
        coef = 1000
        min_length_to_child_edge = 1000000000
        min_child = None
        min_point_on_child_edge = None
        if len(min_node.children) != 0:
            for child in min_node.children:
                vector = (child.x - min_node.x, child.y - min_node.y)
                perpend_vector = (vector[1]*coef, -vector[0]*coef)
                additional_p = (p[0] + perpend_vector[0], p[1] + perpend_vector[1])
                if self.linesCollisionPoint(p[0], p[1], additional_p[0], additional_p[1], min_node.x, min_node.y, child.x, child.y) == (-1, -1):
                    additional_p = (p[0] - perpend_vector[0], p[1] - perpend_vector[1])
                intersection_p = self.linesCollisionPoint(p[0], p[1], additional_p[0], additional_p[1], min_node.x, min_node.y, child.x, child.y)
                length = math.sqrt(abs(intersection_p[0] - p[0])**2 + abs(intersection_p[1] - p[1])**2)
                if length < min_length_to_child_edge:
                    min_length_to_child_edge = length
                    min_child = child
                    min_point_on_child_edge = intersection_p
        # Поиск ближайшей точки на ветви между "отцом" ближайшей вершины и этой вершины
        min_length_to_parent_edge = 1000000000
        intersection_p = None
        if min_node.parent != None:
            vector = (min_node.x - min_node.parent[0], min_node.y - min_node.parent[1])
            perpend_vector = (vector[1]*coef, -vector[0]*coef)
            additional_p = (p[0] + perpend_vector[0], p[1] + perpend_vector[1])
            if self.linesCollisionPoint(p[0], p[1], additional_p[0], additional_p[1], min_node.x, min_node.y, min_node.parent[0], min_node.parent[1]) == (-1, -1):
                additional_p = (p[0] - perpend_vector[0], p[1] - perpend_vector[1])
            intersection_p = self.linesCollisionPoint(p[0], p[1], additional_p[0], additional_p[1], min_node.x, min_node.y, min_node.parent[0], min_node.parent[1])
            length = math.sqrt(abs(intersection_p[0] - p[0]) ** 2 + abs(intersection_p[1] - p[1]) ** 2)
            if length < min_length_to_parent_edge:
                min_length_to_parent_edge = length
        # Возвращаем ближайшую точку дерева (либо точка вершины, либо точка на ветви между отцом и вершиной, либо точка на ветви между вершиной и потомком)
        if min_length_to_node <= min_length_to_child_edge and min_length_to_node <= min_length_to_parent_edge:
            return [(round(min_node.x), round(min_node.y)), 'node_point']
        elif min_length_to_child_edge <= min_length_to_parent_edge:
            return [(round(min_point_on_child_edge[0]), round(min_point_on_child_edge[1])), 'child_edge', min_child]
        else:
            return [(round(intersection_p[0]), round(intersection_p[1])), 'parent_edge', min_node]

    def steerToPoint(self, p1, p2):
        # Возвращает точку на луче [p1, p2) с некоторым заданным шагом такую, что не будет коллизии
        vector = (p2[0] - p1[0], p2[1] - p1[1])
        vector_length = math.sqrt(vector[0]**2 + vector[1]**2)
        if vector_length <= 1:
            return (-1, -1)
        new_vector = (vector[0] * self.step_size / vector_length, vector[1] * self.step_size / vector_length)
        new_point = (p1[0] + new_vector[0], p1[1] + new_vector[1])
        if new_point[0] < 20 or new_point[0] > 1164 or new_point[1] < 20 or new_point[1] > 722:
            return (-1, -1)
        if self.ifCollision(p1, new_point)[0] == False:
            return (round(new_point[0]), round(new_point[1]))
        else:
            x = new_point[0]
            y = new_point[1]
            obstacle = self.ifCollision(p1, new_point)[1]
            left_border1 = (min(obstacle[0][0], obstacle[1][0]), min(obstacle[0][1], obstacle[1][1]))
            left_border2 = (min(obstacle[0][0], obstacle[1][0]), max(obstacle[0][1], obstacle[1][1]))
            up_border1 = left_border2
            up_border2 = (max(obstacle[0][0], obstacle[1][0]), max(obstacle[0][1], obstacle[1][1]))
            right_border1 = up_border2
            right_border2 = (max(obstacle[0][0], obstacle[1][0]), min(obstacle[0][1], obstacle[1][1]))
            bottom_border1 = right_border2
            bottom_border2 = left_border1
            border_lines = [[left_border1, left_border2], [up_border1, up_border2], [right_border1, right_border2], [bottom_border1, bottom_border2]]
            min_length = 1000000
            new_x = x
            new_y = y
            for border in border_lines:
                point = self.linesCollisionPoint(p1[0], p1[1], x, y, border[0][0], border[0][1], border[1][0], border[1][1])
                if point != (-1, -1):
                    length = math.sqrt(abs(p1[0] - point[0])**2 + abs(p1[1] - point[1])**2)
                    if length < min_length:
                        min_length = length
                        new_x = point[0]
                        new_y = point[1]
            return (round(new_x), round(new_y))

    def RRT(self):
        # Основная функция алгоритма, которая строит дерево
        for k in range(self.iterations_num):
            rand_p = self.randPoint()
            nearest_p = self.nearestPointFromTree(rand_p)
            steer = self.steerToPoint(nearest_p[0], rand_p)
            while steer == (-1, -1) or steer[0] < 20 or steer[0] > 1164 or steer[1] < 20 or steer[1] > 722 \
                    or nearest_p[0][0] < 20 or nearest_p[0][0] > 1164 or nearest_p[0][1] < 20 or nearest_p[0][1] > 722 \
                    or self.ifCollision(nearest_p[0], steer)[0] == True:
                rand_p = self.randPoint()
                nearest_p = self.nearestPointFromTree(rand_p)
                steer = self.steerToPoint(nearest_p[0], rand_p)
            if self.ifInObstacle(nearest_p[0]) == True or self.ifInObstacle(steer) == True:
                k -= 1
                continue
            if nearest_p[1] == 'first_point':
                new_node = TreeNode(steer[0], steer[1], (self.tree_nodes[0].x, self.tree_nodes[0].y))
                self.tree_nodes[0].children.append(new_node)
                self.tree_nodes.append(new_node)
            elif nearest_p[1] == 'node_point':
                new_node = TreeNode(steer[0], steer[1], (nearest_p[0][0], nearest_p[0][1]))
                for i in range(len(self.tree_nodes)):
                    if self.tree_nodes[i].x == nearest_p[0][0] and self.tree_nodes[i].y == nearest_p[0][1]:
                        self.tree_nodes[i].children.append(new_node)
                        break
                self.tree_nodes.append(new_node)
            else:
                child = nearest_p[2]
                parent = None
                for i in range(len(self.tree_nodes)):
                    if self.tree_nodes[i].x == child.x and self.tree_nodes[i].y == child.y:
                        parent = self.tree_nodes[i].parent
                        #self.tree_nodes[i].parent = nearest_p[0]
                        break
                for i in range(len(self.tree_nodes)):
                    if self.tree_nodes[i].x == parent[0] and self.tree_nodes[i].y == parent[1]:
                        new_node_for_nearest = TreeNode(nearest_p[0][0], nearest_p[0][1], (parent[0], parent[1]))
                        new_node_for_nearest.children.append(child)
                        new_node_for_steer = TreeNode(steer[0], steer[1], (new_node_for_nearest.x, new_node_for_nearest.y))
                        new_node_for_nearest.children.append(new_node_for_steer)
                        self.tree_nodes[i].children.append(new_node_for_nearest)
                        self.tree_nodes.append(new_node_for_nearest)
                        self.tree_nodes.append(new_node_for_steer)
                        break

    def definePointsInGoalRadius(self):
        # Возвращает ближайшие точки к целевой, лежащие в некотором радиусе
        nearest_p = self.nearestPointFromTree(self.goal)
        if self.step_size < 15:
            step = 15
        elif self.step_size > 30:
            step = 30
        else:
            step = self.step_size
        left_border = self.goal[0] - step
        up_border = self.goal[1] + step
        right_border = self.goal[0] + step
        bottom_border = self.goal[1] - step
        points = []
        for node in self.tree_nodes:
            if node.x >= left_border and node.x <= right_border and node.y <= up_border and node.y >= bottom_border:
                if self.ifCollision((node.x, node.y), self.goal)[0] == False and self.ifInObstacle((node.x, node.y)) == False and self.ifInObstacle(self.goal) == False:
                    if (node.x, node.y) not in points:
                        points.append((node.x, node.y))
        if self.ifCollision(nearest_p[0], self.goal)[0] == False and self.ifInObstacle(nearest_p[0]) == False and self.ifInObstacle(self.goal) == False:
            if nearest_p[0] not in points:
                points.append(nearest_p[0])
        if nearest_p[0] in points:
            if nearest_p[1] == 'node_point':
                return points
            else:
                for node in self.tree_nodes:
                    if node.x == nearest_p[0][0] and node.y == nearest_p[0][1]:
                        return points
                child = nearest_p[2]
                parent = None
                for i in range(len(self.tree_nodes)):
                    if self.tree_nodes[i].x == child.x and self.tree_nodes[i].y == child.y:
                        parent = self.tree_nodes[i].parent
                        #self.tree_nodes[i].parent = nearest_p[0]
                        break
                for i in range(len(self.tree_nodes)):
                    if self.tree_nodes[i].x == parent[0] and self.tree_nodes[i].y == parent[1]:
                        new_node = TreeNode(nearest_p[0][0], nearest_p[0][1], (parent[0], parent[1]))
                        new_node.children.append(child)
                        for j in range(len(self.tree_nodes[i].children)):
                            if self.tree_nodes[i].children[j].x == child.x and self.tree_nodes[i].children[j].y == child.y:
                                self.tree_nodes[i].children[j] = new_node
                                #self.tree_nodes[i].children.append(new_node)
                                break
                        self.tree_nodes.append(new_node)
                        break
                return points
        return points

    def buildBestPath(self):
        # Строит кратчайший путь из начальной к целевой точке
        nearest_points_to_goal = self.definePointsInGoalRadius()
        if len(nearest_points_to_goal) == 0:
            return None
        paths = []
        paths_weights = []
        for point in nearest_points_to_goal:
            p = point
            path = [p]
            weight = 0
            while p != self.start:
                for node in self.tree_nodes:
                    if node.x == p[0] and node.y == p[1]:
                        weight += math.sqrt(abs(node.x - node.parent[0])**2 + abs(node.y - node.parent[1])**2)
                        p = node.parent
                path.insert(0, p)
            paths.append(path)
            paths_weights.append(weight)
        min_weight = 1000000000
        min_weight_ind = 0
        for i in range(len(paths_weights)):
            if paths_weights[i] < min_weight:
                min_weight = paths_weights[i]
                min_weight_ind = i
        return paths[min_weight_ind]