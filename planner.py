# planner.py
import math
import heapq

class YolDugumu:
    def __init__(self, x, y, cost=0):
        self.x = x
        self.y = y
        self.cost = cost

class AStarPlanner:
    def __init__(self):
        # 8 yönlü hareket matrisi (Yatay, dikey ve çaprazlar)
        self.hareketler = [
            YolDugumu(1, 0, 1), YolDugumu(0, 1, 1),
            YolDugumu(-1, 0, 1), YolDugumu(0, -1, 1),
            YolDugumu(1, 1, math.sqrt(2)), YolDugumu(1, -1, math.sqrt(2)),
            YolDugumu(-1, 1, math.sqrt(2)), YolDugumu(-1, -1, math.sqrt(2))
        ]

    def h(self, s, g):
        """ Manhattan heuristiği """
        return abs(s.x - g.x) + abs(s.y - g.y)

    def yol_bul(self, start_pos, goal_pos, bilinen_engeller):
        start_x, start_y = int(round(start_pos[0])), int(round(start_pos[1]))
        goal_x, goal_y = int(round(goal_pos[0])), int(round(goal_pos[1]))

        open_list = []
        # Öncelik kuyruğu için (f_skor, x, y) şeklinde push edilir
        heapq.heappush(open_list, (0, start_x, start_y))
        geldi = {}
        g_skor = {(start_x, start_y): 0}

        while open_list:
            _, x, y = heapq.heappop(open_list)
            
            if (x, y) == (goal_x, goal_y):
                break

            for h in self.hareketler:
                nx, ny = x + h.x, y + h.y
                
                # Eğer komşu nokta robotun bildiği engeller listesindeyse geç
                if (nx, ny) in bilinen_engeller:
                    continue

                yeni_g = g_skor[(x, y)] + h.cost
                if (nx, ny) not in g_skor or yeni_g < g_skor[(nx, ny)]:
                    g_skor[(nx, ny)] = yeni_g
                    f = yeni_g + self.h(YolDugumu(nx, ny), YolDugumu(goal_x, goal_y))
                    heapq.heappush(open_list, (f, nx, ny))
                    geldi[(nx, ny)] = (x, y)

        # Rota oluşturma geri izleme (Backtracking)
        yol = []
        node = (goal_x, goal_y)
        if node not in geldi: 
            return [] # Yol bulunamadıysa boş liste döner
            
        while node != (start_x, start_y):
            yol.append(node)
            node = geldi[node]
        yol.append((start_x, start_y))
        yol.reverse()
        return yol
