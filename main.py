# main.py
import math
import matplotlib.pyplot as plt
from harita import GlobalHarita
from sensor import LidarSensoru
from planner import AStarPlanner

class OtonomSimulasyon:
    def __init__(self):
        self.dunya = GlobalHarita()
        self.lidar = LidarSensoru(menzil=10.0) # 10 metre menzilli Lidar
        self.planner = AStarPlanner()

        # Araç Durumu (Ackermann Kinematiği için)
        self.x = 10.0
        self.y = 50.0
        self.yaw = 0.0
        self.speed = 2.0
        self.steering_angle = 0.0
        self.L = 2.0
        self.dt = 0.5 # Zaman adımı

        self.goal = [45, 25]
        
        # Robotun EN BAŞTA BİLDİĞİ ENGELLER (Boş küme, gezdikçe dolduracak)
        self.robotun_haritasi = set() 

    def update_pose(self, hedef_nokta):
        """ Hedefe doğru Ackermann sürüş fiziği uygulayan basit yönelim """
        dx = hedef_nokta[0] - self.x
        dy = hedef_nokta[1] - self.y
        hedef_yaw = math.atan2(dy, dx)
        
        # Basit bir direksiyon açısı hesaplama
        hata_yaw = hedef_yaw - self.yaw
        self.steering_angle = max(min(hata_yaw, 0.5), -0.5)

        # Fiziği güncelle (Senin yazdığın Ackermann denklemleri)
        self.x += self.speed * math.cos(self.yaw) * self.dt
        self.y += self.speed * math.sin(self.yaw) * self.dt
        self.yaw += (self.speed / self.L) * math.tan(self.steering_angle) * self.dt

    def calistir(self):
        plt.figure(figsize=(7, 7))

        while math.hypot(self.goal[0] - self.x, self.goal[1] - self.y) > 2.0:
            # 1. SENSÖRÜ ÇALIŞTIR: Etraftaki engelleri tara
            yeni_engeller = self.lidar.tara(self.x, self.y, self.dunya.engeller_seti)
            
            # Eğer yeni bir engel keşfettiysek robotun haritasına ekle
            if yeni_engeller - self.robotun_haritasi:
                self.robotun_haritasi.update(yeni_engeller)
            
            # 2. ROTA PLANLA: Sadece bildiğin engelleri hesaba katarak A* çalıştır
            yol = self.planner.yol_bul([self.x, self.y], self.goal, self.robotun_haritasi)
            
            if not yol:
                print("Yol tıkandı, alternatif rota bulunamıyor!")
                break

            # 3. HAREKET ET: Rota üzerindeki bir sonraki noktaya doğru aracı sür
            sonraki_hedef = yol[1] if len(yol) > 1 else self.goal
            self.update_pose(sonraki_hedef)

            # 4. ÇİZİM VE ANİMASYON
            plt.clf()
            # Tüm dünyadaki gerçek engeller (Kırmızı)
            plt.plot(self.dunya.ox, self.dunya.oy, ".r", alpha=0.2)
            # Robotun şu ana kadar Keşfettiği Engeller (Siyah - Parlak)
            if self.robotun_haritasi:
                kx, ky = zip(*self.robotun_haritasi)
                plt.plot(kx, ky, ".k")
            
            # Rota, Robot ve Hedef
            plt.plot([p[0] for p in yol], [p[1] for p in yol], "-b", label="Anlık Dinamik Rota")
            plt.plot(self.x, self.y, "og", markersize=10, label="Araç (Duscart)")
            plt.plot(self.goal[0], self.goal[1], "xb", markersize=12, label="Hedef")
            
            plt.grid(True)
            plt.axis("equal")
            plt.legend()
            plt.pause(0.05)

        plt.show()

if __name__ == "__main__":
    sim = OtonomSimulasyon()
    sim.calistir()
