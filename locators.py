from selenium.webdriver.common.by import By

class AuthorizationPageLocators:
    #Локаторы для авторизации пользователя и создания аккаунта
    ENTER_REGISTRATION_BUTTON = (By.XPATH, '//button[text()="Вход и регистрация"]')
    EMAIL_FIELD = (By.XPATH, '//input[@name="email"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@name="password"]')
    LOGIN_BUTTON = (By.XPATH, '//button[@type="submit" and text()="Войти"]')
    NO_ACCOUNT_BUTTON = (By.XPATH, '//button[text()="Нет аккаунта"]')
    LOGOUT_BUTTON = (By.XPATH, '//button[text()="Выйти"]')

class RegistrationPageLocators:
    #Локаторы для регистрации пользователя и создания аккаунта
    ALREADY_HAVE_ACCOUNT_BUTTON = (By.XPATH, '//button[text()="Уже есть аккаунт"]')
    CREATE_ACCOUNT_BUTTON = (By.XPATH, '//button[text()="Создать аккаунт"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@name="password"]')
    LOGIN_BUTTON = (By.XPATH, '//button[@type="submit" and text()="Войти"]')
    REPEAT_PASSWORD_FIELD = (By.XPATH, '//input[@name="submitPassword"]')
    EMAIL_ERROR_FIELD = (By.XPATH, '//div[contains(@class, "input_inputError__fLUP9")]//input[@name="email"]')
    ERROR_TEXT = (By.XPATH, '//span[text()="Ошибка"]')
    PASSWORD_ERROR_FIELD = (By.XPATH, '//div[contains(@class, "input_inputError__fLUP9")]//input[@name="password"]')
    REPEAT_PASSWORD_ERROR_FIELD = (By.XPATH, '//div[contains(@class, "input_inputError__fLUP9")]//input[@name="submitPassword"]')

class PostAdPageLocators:
    #Локаторы для размещения объявления
    POST_AD_BUTTON = (By.XPATH, '//button[text()="Разместить объявление"]')
    NAME_FIELD = (By.XPATH, '//input[@name="name"]')
    DESCRIPTION_FIELD = (By.XPATH, '//textarea[@placeholder="Описание товара"]')
    PRICE_FIELD = (By.XPATH, '//input[@name="price"]')
    CITY_DROPDOWN = (By.CSS_SELECTOR, 'button.dropDownMenu_arrowDown__pfGL1')
    CITY_OPTION_SPB = (By.CSS_SELECTOR, 'button.dropDownMenu_btn__o8ARs')
    NEW_CONDITION_RADIO = (By.XPATH, '//div[contains(@class, "radioUnput_inputActive__eC-HY")]')
    USED_CONDITION_RADIO = (By.XPATH, '//div[contains(@class, "radioUnput_inputRegular__FbVbr")]')
    CATEGORY_DROPDOWN = (By.CSS_SELECTOR, 'button.dropDownMenu_arrowDown__pfGL1')
    CATEGORY_TECH_BUTTON = (By.XPATH, '//button[.//span[text()="Технологии"]]')
    PUBLISH_BUTTON = (By.XPATH, '//button[text()="Опубликовать"]')
    USER_PROFILE_BUTTON = (By.XPATH, '//button[@class="circleSmall"]')
    AUTH_MODAL_TITLE = (By.XPATH, '//h1[text()="Чтобы разместить объявление, авторизуйтесь"]')
    AD_TITLE_CSS = (By.CSS_SELECTOR, 'h2.h2')




