# pages/saby_main_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import setup_logger
import os

class SabyMainPage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = setup_logger(__name__,
                                 os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             "..", "logs", "saby_main_page.log"))
        self.contacts_menu = (By.CSS_SELECTOR, "li.sbisru-Header__menu-item-1")
        self.contacts_link = (By.CSS_SELECTOR, "a.sbisru-link[href*='contacts']")
        self.region_selector = (By.XPATH, '//*[@id="container"]/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/span/span')
        self.kamchatka_region = (By.XPATH, '//*[@id="popup"]/div[2]/div/div/div/div/div[2]/div/ul/li[43]/span/span')
        self.download_link = (By.CSS_SELECTOR, "a[href*='/download']")

    def open(self, url):
        """Открывает страницу по указанному URL."""
        self.logger.info(f"Открываем страницу: {url}")
        self.driver.get(url)
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.logger.info("Страница загружена")

    def go_to_contacts(self):
        """Переходит в раздел 'Контакты'."""
        self.logger.info("Переходим в раздел 'Контакты'")
        menu = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.contacts_menu))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", menu)
        menu.click()
        link = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.contacts_link))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", link)
        link.click()
        WebDriverWait(self.driver, 15).until(EC.url_contains("contacts"))
        self.logger.info("Успешно перешли в раздел 'Контакты'")

    def click_region(self):
        """Открывает выбор региона и выбирает Камчатский край."""
        self.logger.info("Кликаем по текущему региону")
        region = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.region_selector))
        # Прокручиваем к элементу с учетом возможного фиксированного хедера
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region)
        # Добавляем дополнительную прокрутку вниз, чтобы избежать перекрытия хедера
        self.driver.execute_script("window.scrollBy(0, -100);")
        try:
            region.click()
        except Exception as e:
            self.logger.warning(f"Обычный клик не сработал: {str(e)}, используем JavaScript")
            self.driver.execute_script("arguments[0].click();", region)
        # Ожидаем появления выпадающего списка регионов
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="popup"]')))
        self.logger.info("Выбираем Камчатский край")
        kamchatka = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.kamchatka_region))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", kamchatka)
        try:
            kamchatka.click()
        except Exception as e:
            self.logger.warning(f"Обычный клик на Камчатский край не сработал: {str(e)}, используем JavaScript")
            self.driver.execute_script("arguments[0].click();", kamchatka)
        WebDriverWait(self.driver, 15).until(
            EC.url_to_be("https://saby.ru/contacts/41-kamchatskij-kraj?tab=clients")
        )
        self.logger.info("Регион изменен на Камчатский край, URL обновлен")

    def go_to_download(self):
        """Переходит в раздел 'Скачать локальные версии'."""
        self.logger.info("Переходим в раздел 'Скачать локальные версии'")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        link = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.download_link))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", link)
        link.click()
        WebDriverWait(self.driver, 15).until(EC.url_contains("download"))
        self.logger.info("Успешно перешли в раздел скачивания")