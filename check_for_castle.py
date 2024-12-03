import os
import jpype
import jpype.imports
from jpype.types import *
import time
import winsound

# JAR dosyasının yolunu ayarla
sikulix_path = "sikulixapi-2.0.5-win.jar"

# JVM başlat
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[sikulix_path])

# SikuliX sınıflarını import et
from org.sikuli.script import Screen, Pattern, Region

# Ekran nesnesi oluştur
screen = Screen()

# Resimlerin bulunduğu klasör
image_directory = "C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\castle"

# Resimleri bir kez yükleyip bellekte tutmak için global bir liste
loaded_images = []

def load_images():
    """Bu fonksiyon tüm resim dosyalarını bir kez yükleyip bellekte tutar."""
    try:
        # Klasördeki tüm .png dosyalarını al
        image_files = [f for f in os.listdir(image_directory) if f.endswith('.png')]

        # Her bir resim dosyasını Pattern olarak yükle ve belleğe ekle
        for image_file in image_files:
            image_path = os.path.join(image_directory, image_file)
            pattern = Pattern(image_path)
            loaded_images.append((image_file, pattern))

        print(f"{len(loaded_images)} resim yüklendi.")
    except Exception as e:
        print(f"Resimler yüklenirken hata oluştu: {e}")

def search_for_castle():
    """Yüklü resimleri ekranda arar ve sonuç döner."""
    try:
        # Yüklü resimler üzerinde tarama yap
        for image_file, pattern in loaded_images:
            if screen.exists(pattern,0.1):
                print(f"Kale bulundu - {image_file}")
                # Alarm sesi çal
                winsound.Beep(1000, 500)
                return True

        # Hiçbir kale bulunamazsa
        print("Kale bulunamadı")
        return False

    except Exception as e:
        print(f"Kale arama sırasında hata oluştu: {e}")
        return False

def main():
    # Başlangıçta resimleri bir kez yükle
    load_images()

    # Sürekli olarak kale arama döngüsü
    while True:
        if search_for_castle():
            print("Kale bulundu, aramaya devam ediliyor.")
        else:
            # 0.1 saniye bekledikten sonra tekrar ara
            time.sleep(0.1)

# Ana scripti çalıştır
if __name__ == "__main__":
    main()

# JVM'i kapat
jpype.shutdownJVM()
