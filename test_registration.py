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


class TestRegistration(BaseTest):
    # Тест регистрация пользователя
    
    def test_successful_registration(self, driver):
        
        # 1. Открыть главную страницу
        self.open_main_page(driver)
        
        # 2. Нажать кнопку «Вход и регистрация»
        enter_btn = self.wait_for_element(driver, AuthorizationPageLocators.ENTER_REGISTRATION_BUTTON)
        enter_btn.click()
        
        # 3. Нажать кнопку «Нет аккаунта»
        no_account_btn = self.wait_for_element(driver, AuthorizationPageLocators.NO_ACCOUNT_BUTTON)
        no_account_btn.click()
        
        # 4. Заполнить все поля формы регистрации
        email_field = self.wait_for_element(driver, AuthorizationPageLocators.EMAIL_FIELD)
        email_field.send_keys(f"test_user_{int(time.time())}@gmail.com")
        
        password_field = self.wait_for_element(driver, RegistrationPageLocators.PASSWORD_FIELD)
        password_field.send_keys("Password123")
        
        repeat_password_field = self.wait_for_element(driver, RegistrationPageLocators.REPEAT_PASSWORD_FIELD)
        repeat_password_field.send_keys("Password123")
        
        # 5. Нажать кнопку «Создать аккаунт»
        create_btn = self.wait_for_element(driver, RegistrationPageLocators.CREATE_ACCOUNT_BUTTON)
        create_btn.click()
        
        # 6. Проверить: переход на главную страницу
        time.sleep(2)
        
        # Проверить наличие кнопки «Разместить объявление»
        post_ad_btn = self.wait_for_element(driver, PostAdPageLocators.POST_AD_BUTTON)
        assert post_ad_btn.is_displayed(), "Не удалось вернуться на главную страницу"
        
        # Проверить: отображается кнопка профиля (аватар)
        assert self.is_element_displayed(driver, PostAdPageLocators.USER_PROFILE_BUTTON), "Кнопка профиля не отображается"
        
        # Проверить: НЕ отображается кнопка «Вход и регистрация»
        assert not self.element_exists(driver, AuthorizationPageLocators.ENTER_REGISTRATION_BUTTON, timeout=3), "Кнопка 'Вход и регистрация' все еще отображается"
    
    def test_registration_invalid_email(self, driver):
        # Регистрация пользователя с email не по маске

        # 1. Открыть главную страницу
        self.open_main_page(driver)
        
        # 2. Нажать кнопку «Вход и регистрация»
        enter_btn = self.wait_for_element(driver, AuthorizationPageLocators.ENTER_REGISTRATION_BUTTON)
        enter_btn.click()
        
        # 3. Нажать кнопку «Нет аккаунта»
        no_account_btn = self.wait_for_element(driver, AuthorizationPageLocators.NO_ACCOUNT_BUTTON)
        no_account_btn.click()
        
        # 4. Заполнить поле Email формы регистрации (невалидный email)
        email_field = self.wait_for_element(driver, AuthorizationPageLocators.EMAIL_FIELD)
        email_field.send_keys("invalid-email")  # Невалидный email
        
        # 5. Нажать кнопку «Создать аккаунт»
        create_btn = self.wait_for_element(driver, RegistrationPageLocators.CREATE_ACCOUNT_BUTTON)
        create_btn.click()
        
        time.sleep(2)
        
        # 6. Проверить: поля выделены красным (проверяем, что мы остались на странице регистрации)
        assert self.is_element_displayed(driver, RegistrationPageLocators.CREATE_ACCOUNT_BUTTON), "Форма закрылась"
        
        email_error_elements = driver.find_elements(*RegistrationPageLocators.EMAIL_ERROR_FIELD)
        assert len(email_error_elements) > 0, "Поле Email НЕ выделено красным"
        print(f"Поле Email выделено красным (найдено элементов: {len(email_error_elements)})")

        password_error_elements = driver.find_elements(*RegistrationPageLocators.PASSWORD_ERROR_FIELD)
        assert len(password_error_elements) > 0, "Поле 'Пароль' НЕ выделено красным"
        print(f"Поле 'Пароль' выделено красным (найдено элементов: {len(password_error_elements)})")

        repeat_password_error_elements = driver.find_elements(*RegistrationPageLocators.REPEAT_PASSWORD_ERROR_FIELD)
        assert len(repeat_password_error_elements) > 0, "Поле 'Повторите пароль' НЕ выделено красным"
        print(f"Поле 'Повторите пароль' выделено красным (найдено элементов: {len(repeat_password_error_elements)})")

        # 7. Проверить: под полем email отображается сообщение "Ошибка"
        
        error_elements = driver.find_elements(*RegistrationPageLocators.ERROR_TEXT)
        assert len(error_elements) > 0, "Сообщение 'Ошибка' НЕ отображается"

    def test_registration_existing_user(self, driver):
        # Регистрация уже существующего пользователя

        # 1. Открыть главную страницу
        self.open_main_page(driver)
        
        # 2. Нажать кнопку «Вход и регистрация»
        enter_btn = self.wait_for_element(driver, AuthorizationPageLocators.ENTER_REGISTRATION_BUTTON)
        enter_btn.click()
        
        # 3. Нажать кнопку «Нет аккаунта»
        no_account_btn = self.wait_for_element(driver, AuthorizationPageLocators.NO_ACCOUNT_BUTTON)
        no_account_btn.click()
        
        # 4. Заполнить все поля данными существующего пользователя
        existing_email = "123ann@mail.ru"
        
        email_field = self.wait_for_element(driver, AuthorizationPageLocators.EMAIL_FIELD)
        email_field.send_keys(existing_email)
        
        password_field = self.wait_for_element(driver, RegistrationPageLocators.PASSWORD_FIELD)
        password_field.send_keys("qwerty11")
        
        repeat_password_field = self.wait_for_element(driver, RegistrationPageLocators.REPEAT_PASSWORD_FIELD)
        repeat_password_field.send_keys("qwerty11")
        
        # 5. Нажать кнопку «Создать аккаунт»
        create_btn = self.wait_for_element(driver, RegistrationPageLocators.CREATE_ACCOUNT_BUTTON)
        create_btn.click()
        
        time.sleep(2)
        
        # 6. Проверить: поля Email, «Пароль», «Повторите пароль» выделены красным

        assert self.is_element_displayed(driver, RegistrationPageLocators.CREATE_ACCOUNT_BUTTON), "Форма закрылась"
       
        email_error_elements = driver.find_elements(*RegistrationPageLocators.EMAIL_ERROR_FIELD)
        assert len(email_error_elements) > 0, "Поле Email НЕ выделено красным"
        print(f"Поле Email выделено красным (найдено элементов: {len(email_error_elements)})")

        password_error_elements = driver.find_elements(*RegistrationPageLocators.PASSWORD_ERROR_FIELD)
        assert len(password_error_elements) > 0, "Поле 'Пароль' НЕ выделено красным"
        print(f"Поле 'Пароль' выделено красным (найдено элементов: {len(password_error_elements)})")

        repeat_password_error_elements = driver.find_elements(*RegistrationPageLocators.REPEAT_PASSWORD_ERROR_FIELD)
        assert len(repeat_password_error_elements) > 0, "Поле 'Повторите пароль' НЕ выделено красным"
        print(f"Поле 'Повторите пароль' выделено красным (найдено элементов: {len(repeat_password_error_elements)})")

        # 7. Проверить: под полем email отображается сообщение "Ошибка"
        
        error_elements = driver.find_elements(*RegistrationPageLocators.ERROR_TEXT)
        assert len(error_elements) > 0, "Сообщение 'Ошибка' НЕ отображается"