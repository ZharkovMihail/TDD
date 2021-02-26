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

        # Васе интересно запомнит ли сайт его ценные планы. Он видит, что сайт сгенерировал для него уникальный
        # URL-адрес с пояснением зачем это

        # Вася чекает ссылку, и рад что это не сайт со слатами где макака ловит банан, а его список дел

        # довольный, идет запускать катку в доте

    def test_multiple_users_can_startlists_at_different_urls(self):
        """тест: многочиленные пользователи могут начать списки по разным url"""
        # Вася начинает новый список
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('купить угольки для кэлыча')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: купить угольки для кэлыча')

        # Он видит что его список имеет уникальный url
        vasy_list_url = self.browser.current_url
        self.assertRegex(vasy_list_url, '/lists/.+')

        # Теперь новый пользователь Семен заходт на сайт

        # # Используем новый сеанс браузера, чтобы никакая информация Васи не прошла через куки

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Семён посещает домашнюю страницу. Нет никаких признаков списка Васи
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('купить угольки для кэлыча', page_text)

        # Семен начинает новый список, вводя новый элемент.
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('сдать на права')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: сдать на права')

        # Семён получает уникальный URL
        semen_list_url = self.browser.current_url
        self.assertRegex(semen_list_url, '/lists/.+')
        self.assertNotEqual(semen_list_url, vasy_list_url)

        # опять нет ни слида списка васи
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('купить угольки для кэлыча', page_text)
        self.assertIn('сдать на права', page_text)

        # довольные, идут в пати в дотку
