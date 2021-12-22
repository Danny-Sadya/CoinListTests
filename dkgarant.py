import time
import sys
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
import json
import os


class Scraper:
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_extension(r"extension_1_8_2_0.crx")
        options.add_argument(r"--load_extension=C:\PyProjects\ScrapingProjects\Tests\extension_1_8_2_0.crx")
        options.add_argument("--start-maximized")
        self.driver = uc.Chrome(options=options)
        self.driver.set_page_load_timeout(30)

    def run(self):
        try:
            self.driver.get('https://dkgarant.ru/kontakty/')
            time.sleep(3)
            siteKey = self.driver.find_element(
                By.XPATH, '//div[@class="wpcf7-form-control g-recaptcha wpcf7-recaptcha"]'
                ).get_attribute('data-sitekey')
            print(f'Site Key: {siteKey}')
            current_url = str(self.driver.current_url)
            print('current url: ' + str(current_url))
            sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
            api_key = os.getenv('APIKEY_2CAPTCHA', 'eec356a415a0734ede2e5308ad911d46')
            print('api_key: ' + str(api_key))
            solver = TwoCaptcha(api_key)
            result_token = solver.recaptcha(
                sitekey=siteKey,
                url=current_url
            )
            answer = result_token['code']
            print('result_token: ' + str(answer))
            self.driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "{}";'.format(answer))
            print('\n\nРабота окончена, можете ввести любые данные в поля '
                  'вместо имени и телефона и попробовать отправить форму')
            print('Не нужно нажимать на капчу, она уже решена, иначе сервисы Гугл её перезапустят')

        except Exception as ex:
            print("There's some error")
        finally:
            input("Для завершения работы нажмите ENTER... Тогда браузер закроется")
            self.driver.close()
            self.driver.quit()


if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
