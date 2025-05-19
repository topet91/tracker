import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.saby_main_page import SabyMainPage
from config.config import BASE_URL
from utils.logger import setup_logger
import os

logger = setup_logger(__name__,
                     os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "logs", "test_scenario_2.log"))

@pytest.mark.usefixtures("driver")
class TestScenario2:
    def test_change_region(self, driver):
        try:
            logger.info("Запуск теста сценария 2 ")
            saby_page = SabyMainPage(driver)
            saby_page.open(BASE_URL)
            saby_page.go_to_contacts()
            # Проверяем текущий регион
            region_span = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/span/span'))
            )
            logger.debug(f"Текущий регион: {region_span.text}")
            # Меняем регион
            saby_page.click_region()
            # Проверяем изменения
            WebDriverWait(driver, 15).until(
                EC.url_to_be("https://saby.ru/contacts/41-kamchatskij-kraj?tab=clients")
            )
            assert driver.current_url == "https://saby.ru/contacts/41-kamchatskij-kraj?tab=clients", "URL не соответствует ожидаемому"
            logger.info("URL соответствует ожидаемому")
            # Проверяем совпадения слова "Камчатка" на странице
            page_source = driver.page_source.lower()
            assert "камчатка" in page_source, "Слово 'Камчатка' не найдено на странице"
            logger.info("Слово 'Камчатка' найдено на странице")
            partners = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.sbisru-Contacts-List__col"))
            )
            assert len(partners) > 0, "Список партнеров пуст"
            logger.info("Список партнеров обновлен")
        except Exception as e:
            logger.error(f"Ошибка в тесте: {str(e)}")
            driver.save_screenshot("error_screenshot.png")
            raise