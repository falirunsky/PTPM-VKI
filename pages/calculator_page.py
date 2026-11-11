from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    URL = "https://www.globalsqa.com/angularJs-protractor/SimpleCalculator/"

    _FIRST_INPUT = (By.CSS_SELECTOR, "input[ng-model='a']")
    _SECOND_INPUT = (By.CSS_SELECTOR, "input[ng-model='b']")
    _OPERATION_SELECT = (By.CSS_SELECTOR, "select[ng-model='operation']")
    _RESULT = (By.CSS_SELECTOR, "b.result")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self._FIRST_INPUT))
        return self

    def enter_first_number(self, value):
        field = self.wait.until(EC.element_to_be_clickable(self._FIRST_INPUT))
        field.clear()
        field.send_keys(str(value))
        return self

    def enter_second_number(self, value):
        field = self.wait.until(EC.element_to_be_clickable(self._SECOND_INPUT))
        field.clear()
        field.send_keys(str(value))
        return self

    def select_operation(self, operation):
        element = self.wait.until(EC.presence_of_element_located(self._OPERATION_SELECT))
        Select(element).select_by_visible_text(operation)
        return self

    def get_result(self):
        result = self.wait.until(EC.visibility_of_element_located(self._RESULT))
        return result.text.strip()

    def calculate(self, first, second, operation):
        self.enter_first_number(first)
        self.select_operation(operation)
        self.enter_second_number(second)
        self.wait.until(
            EC.text_to_be_present_in_element(self._RESULT, "=")
        )
        return self.get_result()