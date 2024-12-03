import jpype
import jpype.imports
from jpype.types import *
import time
import csv
import os

# JAR dosyasının yolunu ayarla
sikulix_path = "sikulixapi-2.0.5-win.jar"

# JVM başlat
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[sikulix_path])

# SikuliX sınıflarını import et
from org.sikuli.script import Screen, Pattern, Location, Key

# Ekran nesnesi oluştur
screen = Screen()

def wait_for_loading(image_path, timeout=70):
    """
    Sayfa yüklendi mi diye bir bekleme fonksiyonu.
    """
    if screen.exists(image_path, timeout):
        return True
    else:
        print(f"Beklenen sayfa {timeout} saniye içinde yüklenemedi: {image_path}")
        return False

def click_with_offset(image_path, offset_x=0, offset_y=0):
    """
    Görselin bulunduğu noktaya sapma ile tıkla.
    """
    try:
        region = screen.find(image_path)
        target_location = region.getTarget().offset(Location(offset_x, offset_y))
        screen.hover(target_location)  # Mouse'u hedef noktaya getir
        time.sleep(0.3)  # Tıklama öncesi kısa bekleme süresi
        screen.click(target_location)  # Hedefe tıkla
        print(f"{image_path} tıklandı.")
    except Exception as e:
        print(f"{image_path} tıklanırken hata oluştu: {e}")

def login_to_game():
    try:
        # Login butonuna tıkla
        if screen.exists("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\login_button.png", 60):
            screen.click("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\login_button.png")
        
        # Email alanına tıkla ve yaz
        if screen.exists("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\email_field.png", 30):
            click_with_offset("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\email_field.png")
            screen.type("fthkucuk@hotmail.com")
        
        # Şifre alanına tıkla ve yaz
        if screen.exists("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\password_field.png", 30):
            click_with_offset("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\password_field.png")
            screen.type("Ztfk2013")
        
        # Login işlemini tamamla
        if screen.exists("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\login_submit_button.png", 30):
            click_with_offset("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\login_submit_button.png")

        print("Login işlemi tamamlandı.")

        # Bonus sales sayfasının gelmesi ve yüklenmesi için biraz bekle
        if wait_for_loading("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\bonus_sales_close_button.png", 150):
            print("Bonus sales sayfası geldi, kapatılıyor.")
            click_with_offset("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\bonus_sales_close_button.png")

    except Exception as e:
        print(f"Giriş sırasında hata oluştu: {e}")

def navigate_to_map():
    try:
        # Haritaya gitme butonu
        if screen.exists("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\map_button.png", 60):
            click_with_offset("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\map_button.png")
        
        # Eğer bonus sales sayfası tekrar çıkarsa çarpıya tıkla
        if screen.exists("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\bonus_sales_close_button.png", 60):
            click_with_offset("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\bonus_sales_close_button.png")
        
        print("Harita sayfasına gidildi.")
    except Exception as e:
        print(f"Haritaya giderken hata oluştu: {e}")

def clear_and_enter_text(field_image, text, offset_x=30):
    """
    Giriş alanını temizleyip yeni metni girme fonksiyonu.
    """
    if screen.exists(field_image, 30):
        pattern = Pattern(field_image).targetOffset(offset_x, 0)  # Sağ tarafa 30 piksel ofset
        screen.click(pattern)  # Ayarlanan ofsetle tıklama
        
        # Mevcut metni silmek için BACKSPACE tuşuna basın
        screen.type("a", Key.CTRL)  # Tüm metni seç
        screen.type(Key.BACKSPACE)  # Seçilen metni sil
        screen.type(text)  # Yeni metni gir

def enter_coordinates_and_search(kingdom, x, y):
    try:
        # Koordinat simgesine tıkla
        if screen.exists("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\coordinate_icon.png", 60):
            screen.click("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\coordinate_icon.png")
        
        # Krallık alanına tıkla, temizle ve numarayı yaz
        clear_and_enter_text("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\kingdom_field.png", str(kingdom))
        
        # X koordinat alanına tıkla, temizle ve değeri yaz
        clear_and_enter_text("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\x_field.png", str(x))
        
        # Y koordinat alanına tıkla, temizle ve değeri yaz
        clear_and_enter_text("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\y_field.png", str(y))
        
        # "Git" (Search) butonuna tıkla
        if screen.exists("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\go_button.png", 30):
            screen.click("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\go_button.png")

        print(f"Koordinatlar girildi: Krallık: {kingdom}, X: {x}, Y: {y}")

    except Exception as e:
        print(f"Koordinat girilirken hata oluştu: {e}")

def check_protection_shield(city_image):
    """
    Şehrin koruma kalkanı olup olmadığını kontrol et.
    """
    if screen.exists(city_image):
        print(f"{city_image} koruma kalkanı var.")
    else:
        print(f"{city_image} koruma kalkanı yok.")

def process_city_coordinates(file_path):
    """
    CSV dosyasını oku ve her bir şehir koordinatına git.
    """
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            kingdom = row['krallik']
            x = row['x']
            y = row['y']
            city_image = row['city_image']
            
            # Şehre git
            enter_coordinates_and_search(kingdom, x, y)
            
            # Şehrin koruma kalkanını kontrol et
            city_image_path = os.path.join("C:\\Users\\fthku\\OneDrive\\Desktop\\project\\total-battle-automation\\images\\cities\\", city_image)
            check_protection_shield(city_image_path)
            
            # Her şehir kontrolünden sonra 15 saniye bekle
            time.sleep(15)

def main():
    login_to_game()
    navigate_to_map()

    # Şehir koordinatlarını işleyin
    process_city_coordinates("city_coordinates.csv")

# Ana scripti çalıştır
if __name__ == "__main__":
    main()

# JVM'i kapat
jpype.shutdownJVM()
