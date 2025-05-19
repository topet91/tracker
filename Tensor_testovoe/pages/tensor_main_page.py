from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import setup_logger
import os

class TensorMainPage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = setup_logger(__name__,
                                 os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             "..", "logs", "tensor_main_page.log"))
        self.power_in_people_block = (By.XPATH, "//p[contains(text(), 'Сила в людях')]")
        self.more_details_link = (By.XPATH, "//p[contains(text(), 'Сила в людях')]/ancestor::div[contains(@class, 'tensor_ru-Index__card')]//a[contains(@href, '/about')]")

    def verify_power_in_people_block(self):
        """Проверяет наличие блока 'Сила в людях'."""
        self.logger.info("Проверяем блок 'Сила в людях'")
        # Сначала прокручиваем страницу до конца, чтобы загрузить элементы
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Затем прокручиваем к конкретному элементу
        block = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.power_in_people_block))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", block)
        # Ожидаем видимости элемента
        block = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(self.power_in_people_block))
        self.logger.debug(f"Найден элемент с текстом: {block.text}")
        assert "Сила в людях" in block.text, f"Блок 'Сила в людях' не найден. Текст элемента: {block.text}"
        self.logger.info("Блок 'Сила в людях' найден")

    def navigate_to_about(self):
        """Переходит по ссылке 'Подробнее'."""
        self.logger.info("Кликаем по ссылке 'Подробнее'")
        link = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.more_details_link))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
        try:
            link.click()
        except:
            self.logger.warning("Обычный клик не сработал, используем JavaScript")
            self.driver.execute_script("arguments[0].click();", link)
        WebDriverWait(self.driver, 15).until(EC.url_to_be("https://tensor.ru/about"))
        self.logger.info("Перешли в раздел 'О компании'")