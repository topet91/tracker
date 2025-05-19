import pytest
from pages.saby_main_page import SabyMainPage
from pages.saby_contacts_page import SabyContactsPage
from pages.tensor_main_page import TensorMainPage
from pages.tensor_about_page import TensorAboutPage
from config.config import BASE_URL
from utils.logger import setup_logger
import os

logger = setup_logger(__name__,
                      os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "..", "logs", "test_scenario_1.log"))


@pytest.mark.usefixtures("driver")
class TestScenario1:
    def test_tensor_navigation_and_images(self, driver):
        try:
            logger.info("Запуск теста сценария 1")
            # Инициализация страницы Saby
            logger.debug("Инициализация объекта SabyMainPage")
            saby_page = SabyMainPage(driver)

            # Открытие базового URL
            logger.info(f"Открываем страницу: {BASE_URL}")
            saby_page.open(BASE_URL)
            logger.debug(f"Текущий URL после открытия: {driver.current_url}")

            # Переход в раздел "Контакты"
            logger.info("Переходим в раздел 'Контакты'")
            saby_page.go_to_contacts()
            logger.debug(f"Текущий URL после перехода в 'Контакты': {driver.current_url}")

            # Инициализация страницы контактов
            logger.debug("Инициализация объекта SabyContactsPage")
            contacts_page = SabyContactsPage(driver)

            # Клик по баннеру Tensor
            logger.info("Кликаем по баннеру Tensor")
            contacts_page.click_tensor_banner()
            logger.debug(f"Текущий URL после клика по баннеру Tensor: {driver.current_url}")

            # Инициализация главной страницы Tensor
            logger.debug("Инициализация объекта TensorMainPage")
            tensor_page = TensorMainPage(driver)

            # Проверка блока "Сила в людях"
            logger.info("Проверяем блок 'Сила в людях'")
            tensor_page.verify_power_in_people_block()
            logger.debug("Блок 'Сила в людях' успешно проверен")

            # Переход на страницу "О нас"
            logger.info("Переходим на страницу 'О нас'")
            tensor_page.navigate_to_about()
            logger.debug(f"Текущий URL после перехода на страницу 'О нас': {driver.current_url}")

            # Инициализация страницы "О нас"
            logger.debug("Инициализация объекта TensorAboutPage")
            about_page = TensorAboutPage(driver)

            # Проверка согласованности изображений в разделе "Работа"
            logger.info("Проверяем согласованность размеров изображений в разделе 'Работа'")
            about_page.verify_work_images_consistency()
            logger.debug("Изображения в разделе 'Работа' согласованы")

            logger.info("Тест сценария 1 успешно завершен")
        except Exception as e:
            logger.error(f"Ошибка в тесте: {str(e)}")
            logger.debug(f"Скриншот сохранен как 'error_screenshot.png'")
            driver.save_screenshot("error_screenshot.png")
            raise