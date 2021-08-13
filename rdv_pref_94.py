from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
import smtplib, ssl
import time

from config import*

class RDVPREF94():

    """
    Class pour essayer de trouver un rdv
    """
    def __init__(self):
        self.browser = self.__create_browser_obj()

    def __create_browser_obj(self):
        options = Options()
        #options.headless = True

        fp = webdriver.FirefoxProfile()
        fp.set_preference("general.useragent.override", UserAgent().random)
        fp.update_preferences()

        return webdriver.Firefox(options=options, firefox_profile=fp)

    def get_changement_adresse_rdv(self):
        """
        """
        self.browser.get(RDV_CAD_PAGE_1)

        time.sleep(5)

        #STEP 1: get list of guichets
        elements_guichet    = self.browser.find_elements_by_xpath("//fieldset[@id='fchoix_Booking']/p[@class='Bligne']/input")
        num_guichets        = len(elements_guichet)
        print(f"Number of guichets : {num_guichets}")

        #loop through list of guichets
        for i in range(num_guichets-1, -1, -1):

            # Default case, rdv is present
            rdv_present = True

            self.browser.get(RDV_CAD_PAGE_1)
            print(f"Guichet number : {i+1}")
            time.sleep(5)

            #STEP 2: click on the `i`th guichet
            element = self.browser.find_elements_by_xpath("//fieldset[@id='fchoix_Booking']/p[@class='Bligne']/input")[i]
            element.click()
            time.sleep(5)
            print(4)

            # STEP 3: click next
            self.browser.find_element_by_xpath("//input[@class='Bbutton']").click()

            time.sleep(5)
            print(5)

            # STEP 4: look for unavailabilty
            message = self.browser.find_element_by_xpath("//form[@id='FormBookingCreate']").text
            for ignore_msg in RDV_CAD_UNAVAILABLE_TEXT:
                if ignore_msg in message:
                    print("rien trouvé")
                    rdv_present = False
                    break

            if rdv_present:
                print(message)
                self.send_email_notif(i, message)

    def loop_rdv_find_executor(self):
        """
        """
        counter = 1
        while True:
            try:
                self.get_changement_adresse_rdv()
            except:
                self.__do_double_refresh()
            if counter%5 == 0:
                self.browser.close()
                self.browser = self.__create_browser_obj()

            counter +=1
            time.sleep(LOOP_INTERVAL)

    def __do_double_refresh(self):
        """
        Method pour faire double refresh
        """
        self.browser.get(RDV_CAD_PAGE_1)
        time.sleep(5)

        #twice
        self.browser.refresh()
        self.browser.refresh()

    def send_email_notif(self, guichet_num, message):
        """
        Methode pour envoyer un email
        """
        sent_from   = froming_user
        to          = toing_user
        subject     = f'RDV DISPO at Guichet {guichet_num+1} '
        body        = message.encode('utf-8')

        email_text = """\
        Subject: %s\n
        
        %s
        """ % (subject, body)

        try:

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(froming_user, froming_password)
            server.sendmail(sent_from, to, email_text)
            server.close()

            print('Email sent!')

        except Exception as e:
            print(f"[Exception] - {e}")

