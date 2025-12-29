import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from locators import (
    AuthorizationPageLocators,
    RegistrationPageLocators,
    PostAdPageLocators
)
from test_authorization import BaseTest

class TestAdvertisement(BaseTest):
    # тесты на создание объявления

    def test_create_ad_unauthenticated(self, driver):
        #Создание объявления неавторизованным пользователем

        # 1. Открыть главную страницу
        self.open_main_page(driver)

        # 2. Нажать кнопку «Разместить объявление»
        post_ad_btn = self.wait_for_element(driver, PostAdPageLocators.POST_AD_BUTTON)
        post_ad_btn.click()
        
        time.sleep(2)
        
        # 3. Проверить: отображается модальное окно с заголовком «Чтобы разместить объявление, авторизуйтесь».
        
        modal_elements = driver.find_elements(*PostAdPageLocators.AUTH_MODAL_TITLE)
        assert len(modal_elements) > 0, "Модальное окно с заголовком не отображается"

    def test_create_ad_authenticated(self, driver):
        # Создание объявления авторизованным пользователем

        # 1. Открыть главную страницу
        self.open_main_page(driver)
        
        # 2. Нажать кнопку «Вход и регистрация»
        enter_btn = self.wait_for_element(driver, AuthorizationPageLocators.ENTER_REGISTRATION_BUTTON)
        enter_btn.click()
        
        # 3. Заполнить все поля формы авторизации
        test_email = "123ann@mail.ru" 
        test_password = "qwerty11"   
        
        email_field = self.wait_for_element(driver, AuthorizationPageLocators.EMAIL_FIELD)
        email_field.send_keys(test_email)
        
        password_field = self.wait_for_element(driver, AuthorizationPageLocators.PASSWORD_FIELD)
        password_field.send_keys(test_password)
        
        # 4. Нажать кнопку «Войти»
        login_btn = self.wait_for_element(driver, AuthorizationPageLocators.LOGIN_BUTTON)
        login_btn.click()
        
        # Ждем перезагрузки и появления элемента заново
        time.sleep(3)

        # 5. Нажать кнопку «Разместить объявление»
        post_ad_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(PostAdPageLocators.POST_AD_BUTTON)
    )
        post_ad_btn.click()
        time.sleep(3)
    
        # 6. Заполнить все поля формы
        ad_name = f"Новое объявление {int(time.time())}"
        
        name_field = self.wait_for_element(driver, PostAdPageLocators.NAME_FIELD)
        name_field.send_keys(ad_name)
        
        description_field = self.wait_for_element(driver, PostAdPageLocators.DESCRIPTION_FIELD)
        description_field.send_keys("Новогодние носки")
        
        price_field = self.wait_for_element(driver, PostAdPageLocators.PRICE_FIELD)
        price_field.send_keys("100500")
        
        # 7. Выбрать город из Dropdown
        city_dropdown = self.wait_for_element(driver, PostAdPageLocators.CITY_DROPDOWN)
        city_dropdown.click()
        time.sleep(1)
    
        # Используем локатор для выбора Санкт-Петербурга
        city_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(PostAdPageLocators.CITY_OPTION_SPB)
    )
        city_option.click()
        time.sleep(1)
        
        # 8. Выбрать из Dropdown «Категорию»
        category_dropdown = self.wait_for_element(driver, PostAdPageLocators.CATEGORY_DROPDOWN)
        category_dropdown.click()
        time.sleep(1)

        # Используем локатор для выбора категории "Технологии"
        category_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(PostAdPageLocators.CATEGORY_TECH_BUTTON)
    )
        category_option.click()
        time.sleep(2)
        
        # 9. Выбрать RadioButton «Состояние товара»
        try:
            new_condition = driver.find_element(*PostAdPageLocators.NEW_CONDITION_RADIO)
            new_condition.click()
        except:
            used_condition = driver.find_element(*PostAdPageLocators.USED_CONDITION_RADIO)
            used_condition.click()
        
        # 10. Нажать кнопку «Опубликовать»
        publish_btn = self.wait_for_element(driver, PostAdPageLocators.PUBLISH_BUTTON)
        publish_btn.click()
        
        time.sleep(4)
        
        # 11. Перейти в профиль пользователя
        profile_btn = self.wait_for_element(driver, PostAdPageLocators.USER_PROFILE_BUTTON)
        profile_btn.click()
        time.sleep(4)
        
        # 12. Проверить: в блоке «Мои объявления» отображается созданное объявление.
       
        my_ad_elements = driver.find_elements(*PostAdPageLocators.AD_TITLE_CSS)
    
        assert len(my_ad_elements) > 0, "В блоке 'Мои объявления' нет объявлений"

        found_ad = None
        for ad_element in my_ad_elements:
            if ad_element.text == ad_name:
                found_ad = ad_element
                break
    
        assert found_ad is not None, f"Объявление с названием '{ad_name}' не найдено в профиле"
