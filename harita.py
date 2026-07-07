# harita.py
class GlobalHarita:
    def __init__(self):
        self.ox = []
        self.oy = []
        self.olustur()
        # main.py'ın set işlemleri için set tipinde koordinat eşleşmesi
        self.engeller_seti = set(zip(self.ox, self.oy))

    def olustur(self):
        # Dış sınır duvarları (-10 ile 60 arası kare alan)
        for i in range(-10, 61):
            self.ox.append(i); self.oy.append(-10.0)
            self.ox.append(60.0); self.oy.append(i)
            self.ox.append(i); self.oy.append(60.0)
            self.ox.append(-10.0); self.oy.append(i)

        # Görselde gördüğün iç engeller (Dikey duvarlar)
        # Sol alt taraftaki dikey engel
        for i in range(-10, 20):
            self.ox.append(15.0); self.oy.append(i)
        
        # Sağ üst taraftaki dikey engel
        for i in range(20, 41):
            self.ox.append(40.0); self.oy.append(i)
