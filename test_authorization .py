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

class BaseTest:
   
    def open_main_page(self, driver):
        # Открыть главную страницу
        driver.get("https://qa-desk.stand.praktikum-services.ru/")
        time.sleep(2)
    
    def wait_for_element(self, driver, locator, timeout=10):
        # Ожидание элемента
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
    
    def wait_for_element_visible(self, driver, locator, timeout=10):
        # Ожидание видимости элемента
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def element_exists(self, driver, locator, timeout=5):
        # Проверка наличия элемента
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_displayed(self, driver, locator):
        # Проверка отображения элемента
        try:
            return driver.find_element(*locator).is_displayed()
        except NoSuchElementException:
            return False
        

class TestLoginLogout(BaseTest):
    # Тест Login пользователя
    
    def test_successful_login(self, driver):
      
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
        
        # 5. Проверить: переход на главную страницу
        time.sleep(2)
        
        # Проверить наличие кнопки «Разместить объявление»
        post_ad_btn = self.wait_for_element(driver, PostAdPageLocators.POST_AD_BUTTON)
        assert post_ad_btn.is_displayed(), "Не удалось вернуться на главную страницу"
        
        # Проверить: отображается кнопка профиля
        assert self.is_element_displayed(driver, PostAdPageLocators.USER_PROFILE_BUTTON), "Кнопка профиля не отображается"
        
        # Проверить: НЕ отображается кнопка «Вход и регистрация»
        assert not self.element_exists(driver, AuthorizationPageLocators.ENTER_REGISTRATION_BUTTON, timeout=3), "Кнопка 'Вход и регистрация' все еще отображается"
    
    def test_logout(self, driver):
        # Logout пользователя

        # 1. Авторизоваться
        self.test_successful_login(driver)
        
        # 2. Нажать кнопку «Выйти»
        logout_btn = self.wait_for_element(driver, AuthorizationPageLocators.LOGOUT_BUTTON)
        logout_btn.click()
        
        time.sleep(2)
        
        # 3. Проверить: кнопка профиля больше не отображается
        assert not self.element_exists(driver, PostAdPageLocators.USER_PROFILE_BUTTON, timeout=3), "Кнопка профиля все еще отображается"
        
        # Проверить: отображается кнопка «Вход и регистрация»
        assert self.is_element_displayed(driver, AuthorizationPageLocators.ENTER_REGISTRATION_BUTTON), "Кнопка 'Вход и регистрация' не отображается"
        
        # Проверить: кнопка «Выйти» не отображается
        assert not self.element_exists(driver, AuthorizationPageLocators.LOGOUT_BUTTON, timeout=3), "Кнопка 'Выйти' все еще отображается"
