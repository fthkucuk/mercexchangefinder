import os
import jpype
import jpype.imports
from jpype.types import *
import time
import threading
import pyautogui
from concurrent.futures import ThreadPoolExecutor

# JAR dosyasının yolunu ayarla
sikulix_path = "sikulixapi-2.0.5-win.jar"

# JVM başlat
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[sikulix_path])

# SikuliX sınıflarını import et
from org.sikuli.script import Screen, Pattern, Location, Key, Region

BASE_PATH = "C:\\Users\\\Fatih\\Desktop\\project\\total-battle-automation\\images"

# Resimlerin bulunduğu dizinler
IMAGE_PATH = os.path.join(BASE_PATH, "crypt")  # Görsellerin bulunduğu dizin

# Screen nesnesi oluşturuluyor
screen = Screen()

def get_center_region():
    # Ekran boyutlarını al
    screen_width = screen.w
    screen_height = screen.h

    # Ortadaki bölgenin boyutları
    region_width = 700  # Genişlik
    region_height = 500  # Yükseklik

    # Ortadaki bölgenin sol üst köşesi
    x = (screen_width - region_width) // 2
    y = (screen_height - region_height) // 2

    # Region (alan) oluştur
    return Region(x, y, region_width, region_height)

# Fare hareketini sürekli simüle et
def prevent_sleep():
    while True:
        pyautogui.move(100, 0)  # Fareyi sağa hareket ettir
        time.sleep(60 * 5)  # 5 dakika bekle
        pyautogui.move(-100, 0)  # Fareyi sola hareket ettir
        time.sleep(60 * 5)  # 5 dakika daha bekle

# Resimleri yükleyip ekranın tamamında arayalım
def load_images(image_folder_path):
    images = {}
    image_files = [f for f in os.listdir(image_folder_path) if f.endswith('.png')]
    for image_file in image_files:
        image_path = os.path.join(image_folder_path, image_file)
        pattern = Pattern(image_path).similar(0.9)
        images[image_file] = pattern
    return images

def click_image(image_name, image_pattern):
    if screen.exists(image_pattern):
        print(f"Found: {image_name}. Clicking...")
        match = screen.find(image_pattern)
        click_location = match.getTarget()
        screen.click(click_location)
        print(f"Clicked at coordinates: ({click_location.getX()}, {click_location.getY()})")
        return True
    return False

def click_on_coordinates(selected_folders):
    if not isinstance(selected_folders, list):
        selected_folders = [selected_folders]  # Tek bir klasör verilirse listeye dönüştür

    center_region = get_center_region()  # Ortadaki kareyi al

    for folder in selected_folders:
        folder_path = os.path.join(IMAGE_PATH, folder)

        # Klasörün varlığını kontrol et
        if not os.path.exists(folder_path):
            print(f"Error: Folder '{folder_path}' does not exist.")
            continue

        # Resimleri yükle
        images = load_images(folder_path)

        # Paralel olarak resimleri kontrol et
        found = False
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(click_image_in_region, image_name, image_pattern, center_region): image_name
                       for image_name, image_pattern in images.items()}
            for future in futures:
                if future.result():  # Eğer bir eşleşme bulunursa
                    found = True
                    break

        if found:
            return True  # Eşleşme bulunduğunda işlemi sonlandır

    print(f"No matching images found in folders: {selected_folders}")
    return False  # Hiçbir eşleşme bulunamadıysa False döndür


def click_image_in_region(image_name, image_pattern, region):
    print(f"Searching for: {image_name} in the center region.")
    if region.exists(image_pattern):
        print(f"Found: {image_name} in the center region. Clicking...")
        match = region.find(image_pattern)  # Görselin bulunduğu konumu al
        click_location = match.getTarget()  # Hedef konumunu al
        screen.click(click_location)  # Görselin bulunduğu koordinata tıklama
        print(f"Clicked at coordinates: ({click_location.getX()}, {click_location.getY()})")
        return True
    return False

def click_watchtower():
    watchtower_coordinates = (691, 929)
    screen.click(Location(watchtower_coordinates[0], watchtower_coordinates[1]))
    print("Clicked on Watchtower icon.")

def click_crypts_and_arenas():
    crypts_coordinates = (683, 455)
    screen.click(Location(crypts_coordinates[0], crypts_coordinates[1]))
    print("Clicked on Crypts and Arenas.")

def click_go_button():
    go_button_coordinates = (1212, 468)
    screen.click(Location(go_button_coordinates[0], go_button_coordinates[1]))
    print("Clicked Go button.")

def click_explore():
    explore_button_coordinates = (1134, 769)
    screen.click(Location(explore_button_coordinates[0], explore_button_coordinates[1]))
    print("Clicked Explore button.")

def check_visual_on_screen():
    target_image = Pattern(os.path.join(IMAGE_PATH, "carter.png")).similar(0.7)
    
    retries = 0  # Deneme sayısını sıfırlıyoruz
    while retries < 3:
        if screen.exists(target_image):  # Görseli bulursa
            print("Target image found on screen.")
            retries = 0  # Görsel bulunduğunda denemeleri sıfırla
            time.sleep(2)  # Görseli bulduğunda kısa bir süre bekleyelim ve işlem devam etsin
        else:
            print("Target image not found. Retrying...")
            retries += 1  # Deneme sayısını arttır
            time.sleep(2)  # Görsel kaybolduğunda 2 saniye bekleyip tekrar deneyelim
    
    if retries == 3:
        print("Target image still not found after 3 retries.")
        return False  # 3 denemede de görsel bulunmazsa False döndürüyoruz

    return True

def check_advertisement():
    advertisement_image = Pattern(os.path.join(IMAGE_PATH, "advertisement.png")).similar(0.7)
    if screen.exists(advertisement_image):
        print("Advertisement found on screen. Closing it...")
        screen.type(Key.ESC)
        time.sleep(1)
        return True
    return False

def automate():
    while True:
        # Reklam kontrolü yapılır
        if check_advertisement():
            print("Advertisement closed. Restarting the process...")
            continue

        try:
            click_watchtower()
            time.sleep(1)

            click_crypts_and_arenas()
            time.sleep(1)

            click_go_button()
            time.sleep(1)

            # Koordinatları tıklama
            if not click_on_coordinates(["25"]):
                print("No matching images found. Restarting the process...")
                continue  # Hiçbir eşleşme bulunmadıysa döngü başa döner

            click_explore()
            time.sleep(1)

            # Single tıklama yapılacak koordinata tıkla
            single_click_coordinates = (1237, 111)
            screen.click(Location(single_click_coordinates[0], single_click_coordinates[1]))
            print("Single left click performed at specified coordinates.")
    
            time.sleep(1)

            # Double tıklama yapılacak koordinata tıkla
            double_click_coordinates = (1125, 450)
            for _ in range(5):  # Çift tıklama döngüsü
                screen.click(Location(double_click_coordinates[0], double_click_coordinates[1]))
                time.sleep(0.2)  # Çift tıklama arasında kısa bir bekleme
            print("Double left click performed at specified coordinates.")

            # Görselin varlığı kontrol edilir
            if not check_visual_on_screen():  # 3 defa görsel yoksa başa dönecek
                print("Target image not found after 3 retries. Restarting the process...")
                continue

        except Exception as e:
            print(f"Error occurred: {e}. Restarting the process...")

# Ana fonksiyonu başlat
if __name__ == "__main__":
    threading.Thread(target=prevent_sleep, daemon=True).start()
    automate()
