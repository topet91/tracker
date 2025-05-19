import pytest
import os
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (StaleElementReferenceException,
                                        NoSuchElementException,
                                        TimeoutException)
from pages.saby_main_page import SabyMainPage
from config.config import BASE_URL, DOWNLOAD_DIR
from utils.logger import setup_logger
import time

logger = setup_logger(__name__,
                      os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "..", "logs", "test_scenario_3.log"))


def tab_is_active_or_clickable(driver, xpath, active_class='controls-TabButton__inner--selected'):
    """Кастомное ожидание для вкладок: проверяет активное состояние или кликабельность"""
    try:
        element = driver.find_element(By.XPATH, xpath)
        if not element.is_displayed():
            return False

        parent = element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'controls-TabButton')][1]")

        if active_class in parent.get_attribute("class"):
            return element
        if element.is_enabled():
            return element
        return False
    except (StaleElementReferenceException, NoSuchElementException):
        return False


@pytest.mark.usefixtures("driver")
class TestScenario3:
    def test_download_plugin(self, driver):
        try:
            logger.info("Запуск теста сценария 3")
            saby_page = SabyMainPage(driver)
            saby_page.open(BASE_URL)
            saby_page.go_to_download()

            # Ожидание полной загрузки страницы
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            # Обработка скачивания файла
            download_link = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//a[contains(@class, 'sbis_ru-DownloadNew-loadLink__link') and contains(text(), 'Exe')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_link)

            file_size_text = download_link.text
            expected_size_mb = float(re.search(r"(\d+\.\d+)", file_size_text).group())
            download_link.click()
            logger.info("Кликнули по ссылке для скачивания EXE")

            # Проверка скачивания
            downloaded_file = os.path.join(DOWNLOAD_DIR, "sbisplugin-setup-web.exe")
            logger.info(f"Ожидаем файл: {downloaded_file}")
            # Отладка: выводим содержимое папки загрузки
            for _ in range(60):
                # Проверяем все файлы в папке
                files_in_dir = os.listdir(DOWNLOAD_DIR)
                logger.debug(f"Содержимое папки {DOWNLOAD_DIR}: {files_in_dir}")
                # Проверяем наличие временных файлов .crdownload
                crdownload_files = [f for f in files_in_dir if f.endswith('.crdownload')]
                if crdownload_files:
                    logger.debug(f"Найдены временные файлы загрузки: {crdownload_files}")

                if os.path.exists(downloaded_file):
                    actual_size_mb = os.path.getsize(downloaded_file) / (1024 * 1024)
                    assert abs(actual_size_mb - expected_size_mb) < 0.5, \
                        f"Размер файла {actual_size_mb:.2f} МБ не соответствует ожидаемому {expected_size_mb} МБ"
                    logger.info(f"Файл скачан и равен заявленному на сайте размеру: {actual_size_mb:.2f} МБ")
                    return
                time.sleep(1)
            # Если файл не скачался, выводим финальное содержимое папки
            files_in_dir = os.listdir(DOWNLOAD_DIR)
            logger.error(f"Файл не скачался. Содержимое папки {DOWNLOAD_DIR}: {files_in_dir}")
            raise AssertionError("Файл не скачался")

        except TimeoutException as e:
            logger.error(f"Timeout ошибка: {str(e)}")
            driver.save_screenshot("timeout_error.png")
            raise
        except Exception as e:
            logger.error(f"Ошибка в тесте: {str(e)}")
            driver.save_screenshot("error_screenshot.png")
            raise