import unittest
from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from os import system

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def document_initialised(driver):
    return driver.execute_script("return initialised")


class ECommerceTest(unittest.TestCase):
    """Pruebas automatizadas para la compra de productos"""
    driver = None
    wait = None

    def setUp(self):
        """ Inicializa las opciones para empezar el testing de la pagina"""

        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(options=options)
        self.driver.timeouts.page_load = 60
        self.driver.timeouts.implicit_wait = 10
        self.driver.maximize_window()

        self.driver.get("https://www.udemy.com")

        self.wait = WebDriverWait(self.driver, 60)

    def test_buy_course(self):
        """
        Busca en la categoria desarrollo los cursos de un rating de mas de 3.5
            y que su duracion sea corta, selecciona el curso de SCRUM y lo compra (
                para proceder con la compra debe registrarse
            ), el caso de prueba termina cuando aparece el boton de confirma compra (
                checkout
            )
        """
        try:
            self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Desarrollo"))
            )

            self.driver.find_element(By.LINK_TEXT, "Desarrollo").click()

            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@value='3.5']/parent::label")))

            self.driver.find_element(
                By.XPATH, "//input[@value='3.5']/parent::label").click()

            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@value='extraShort']/parent::label")))

            self.driver.find_element(
                By.XPATH, "//input[@value='extraShort']/parent::label").click()

            self.wait.until(
                EC.element_to_be_clickable(
                    (By.LINK_TEXT, "Fundamentos de SCRUM, metodología ágil gestión de proyectos"))
            )

            self.driver.find_element(
                By.LINK_TEXT, "Fundamentos de SCRUM, metodología ágil gestión de proyectos").click()

            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='buy-button buy-box--buy-box-item--1Qbkl buy-box--buy-button--1mpz_']/descendant::button"))
            )

            self.driver.find_element(
                By.XPATH, "//div[@class='buy-button buy-box--buy-box-item--1Qbkl buy-box--buy-button--1mpz_']/descendant::button").click()

            self.wait.until(
                EC.presence_of_element_located(
                    (By.NAME, "fullname"))
            )

            fullname = self.driver.find_element(By.NAME, "fullname")

            fullname.send_keys('Pepito Perez')

            email = self.driver.find_element(By.NAME, "email")

            email.send_keys('<solo_cambiar_esto>@mail.com')

            password = self.driver.find_element(By.NAME, "password")

            password.send_keys('#asdf!q123')

            self.driver.find_element(
                By.XPATH, "//span[text()='Regístrate']/parent::button").click()

            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//span[text()='Complete Checkout']"))
            )

            actual = self.driver.find_element(
                By.XPATH, "//span[text()='Complete Checkout']").text

            expected = "Complete Checkout"

            self.assertEqual(actual, expected)
        except TimeoutException:
            print("El elemento no ha sido encontrado dentro del contexto actual")

    def tearDown(self):
        """
        Cierra el navegador cuando termina las pruebas
        """
        self.driver.quit()
        # pass


if __name__ == '__main__':
    unittest.main()
