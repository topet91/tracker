# pages/tensor_about_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import setup_logger
import os

class TensorAboutPage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = setup_logger(__name__,
                                 os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             "..", "logs", "tensor_about_page.log"))
        self.working_images = (By.CSS_SELECTOR, "div.tensor_ru-About__block3-image-wrapper img")

    def verify_work_images_consistency(self):
        """Проверяет, что все изображения в разделе 'Работаем' имеют одинаковый размер."""
        self.logger.info("Проверяем размеры изображений в разделе 'Работаем'")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        images = WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located(self.working_images))
        if not images:
            self.logger.error("Изображения не найдены")
            raise AssertionError("Изображения не найдены")
        sizes = [(int(img.get_attribute("naturalWidth")), int(img.get_attribute("naturalHeight")))
                 for img in images]
        first_size = sizes[0]
        assert all(size == first_size for size in sizes), f"Изображения имеют разные размеры: {sizes}"
        self.logger.info("Все изображения имеют одинаковый размер")