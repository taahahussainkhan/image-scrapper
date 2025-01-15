from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import requests


options = Options()
options.add_argument("--headless") 
options.add_argument("--disable-gpu")

URL = 'https://unsplash.com/'

try:
    driver  = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()))
    driver.get(URL)
    
    time.sleep(10)
    
    height = 0
    for i in range(15):
        height = height + 500
        driver.execute_script(f"window.scrollTo(0,{height})")
        time.sleep(1)
    
    image_tags = driver.find_elements(By.XPATH," //img[@class ='tzC2N fbGdz cnmNG']")
    print("Number of images found: ", len(image_tags))

    
    image_urls = [img.get_attribute('src') for img in image_tags if 'images' in img.get_attribute('src')]
    
    for url in image_urls:
        print(url)

except Exception as e:
    print("An error has occured", e)
    
finally:
    try:
        for index,url in enumerate(image_urls):
            response = requests.get(url, stream=True)
            
            with open(f'image-{index+1}.jpg', 'wb') as file:
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)
        
        
    except Exception as error:
        print("An error occured while downloading images", error)

    finally:
        driver.close()