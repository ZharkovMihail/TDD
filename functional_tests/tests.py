from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase


MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """тест нового посетителя"""

    def setUp(self) -> None:
        """установка"""
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """демонтаж"""
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """ожидать строку в таблице списка"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        """тест: можно начать список и получить его позже"""
        # Василий пронюхал что появился ах****ый сайт со списком неотложных дел, блекджеком и шлюхами
        # ну и решил почекать его домашнюю страницу
        self.browser.get(self.live_server_url)

        # Он убеждается что заголовок и шапка страницы про неотложные дела
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # ему предлогоается ввести элемент списка
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        # набирает в текстовом поле "купить угольки для кэлыча"
        input_box.send_keys('купить угольки для кэлыча')

        # после ENTER страница обновляется и появляется список с одним пунктом: "1: купить угольки для кэлыча"
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: купить угольки для кэлыча')

        # текстовое поле предлагает ввести ещё дело
        # Вася вводит "Раскумарить плотную забивочку"
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Раскумарить плотную забивочку')
        input_box.send_keys(Keys.ENTER)

        # Страница обновляется и показывает список с двумя задачами
        self.wait_for_row_in_list_table('1: купить угольки для кэлыча')
        self.wait_for_row_in_list_table('2: Раскумарить плотную забивочку')

        self.fail('Закончить тест')
        # Васе интересно запомнит ли сайт его ценные планы. Он видит, что сайт сгенерировал для него уникальный
        # URL-адрес с пояснением зачем это

        # Вася чекает ссылку, и рад что это не сайт со слатами где макака ловит банан, а его список дел

        # довольный, идет запускать катку в доте
