# sensor.py
import math

class LidarSensoru:
    def __init__(self, menzil=10.0):
        self.menzil = menzil 

    def tara(self, arac_x, arac_y, global_engeller):
        """ Aracın menziline giren engelleri tespit eden fonksiyon """
        tespit_edilenler = set()
        for ex, ey in global_engeller:
            # Öklid mesafesi hesabı
            mesafe = math.hypot(ex - arac_x, ey - arac_y)
            if mesafe <= self.menzil:
                # Koordinat sisteminin tam oturması için tam sayıya yuvarlayarak ekleme yapıyoruz
                tespit_edilenler.add((int(round(ex)), int(round(ey))))
        return tespit_edilenler
