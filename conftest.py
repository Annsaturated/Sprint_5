import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    #Фикстура для создания и закрытия драйвера Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    
    yield driver
    
    driver.quit()