# pages/saby_contacts_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import setup_logger
import os

class SabyContactsPage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = setup_logger(__name__,
                                 os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             "..", "logs", "saby_contacts_page.log"))
        # Уточненный селектор для баннера Тензор на основе предоставленного HTML
        self.tensor_banner = (By.CSS_SELECTOR, "a.sbisru-Contacts__logo-tensor")

    def click_tensor_banner(self):
        """Кликает по баннеру Тензор и переключается на новую вкладку."""
        self.logger.info("Кликаем по баннеру Тензор")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Проверяем, сколько элементов находит селектор
        banners = self.driver.find_elements(*self.tensor_banner)
        self.logger.debug(f"Найдено элементов с селектором баннера: {len(banners)}")
        for i, banner in enumerate(banners):
            href = banner.get_attribute("href")
            self.logger.debug(f"Баннер {i+1}: href={href}, текст={banner.text}")

        # Ожидаем кликабельности баннера
        banner = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.tensor_banner))
        href = banner.get_attribute("href")
        self.logger.info(f"Кликаем по баннеру с href={href}")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", banner)

        original_window = self.driver.current_window_handle
        try:
            banner.click()
        except Exception as e:
            self.logger.warning(f"Обычный клик не сработал: {str(e)}, используем JavaScript")
            self.driver.execute_script("arguments[0].click();", banner)

        # Ждем открытия новой вкладки
        WebDriverWait(self.driver, 15).until(EC.number_of_windows_to_be(2))
        self.logger.info(f"Количество вкладок: {len(self.driver.window_handles)}")

        # Переключаемся на новую вкладку
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break

        # Ждем нужный URL в новой вкладке
        WebDriverWait(self.driver, 15).until(EC.url_to_be("https://tensor.ru/"))
        self.logger.info(f"Текущий URL: {self.driver.current_url}")

        # Возвращаемся к исходной вкладке и закрываем ее
        self.driver.switch_to.window(original_window)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.logger.info("Перешли на страницу Тензор и закрыли предыдущую")