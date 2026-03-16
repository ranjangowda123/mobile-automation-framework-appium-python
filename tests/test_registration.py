import allure
import pytest

from pages.account_creation_page import AccountCreationPage
from pages.choose_exam_page import ChooseExamPage
from pages.diagnostic_test_page import DiagnosticTestPage
from pages.home_page import HomePage
from pages.listening_page import ListeningPage
from pages.personalize_experience_page import PersonalizeExperiencePage
from pages.profile_details_page import ProfileDetailsPage
from pages.reading_page import ReadingPage
from pages.speaking_writing_page import SpeakingWritingPage
from utils.data_reader import get_test_data

data = get_test_data()
class TestRegister:

    # Test metadata
    @allure.epic("Registration")
    @allure.feature("Sign Up")
    @allure.story("Valid Sign Up")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("New user registration flow")
    @allure.description("Verify that a new user can successfully register and reach the home page after completing diagnostic test flow.")
    @pytest.mark.parametrize("user",data["Users"][0])
    @pytest.mark.regression
    def test_login(self,driver,user):

        email = user['email']
        allure.dynamic.parameter("email",email)
        profile = data['profile_details']
        firstname = profile['fname']
        lastname = profile['lname']
        language = profile['language']
        score = data['score']

        account_creation_page = AccountCreationPage(driver)
        profile_details_page = ProfileDetailsPage(driver)
        choose_exam_page = ChooseExamPage(driver)
        personalize_page = PersonalizeExperiencePage(driver)
        diagnostic_page = DiagnosticTestPage(driver)
        speak_and_write = SpeakingWritingPage(driver)
        reading_page = ReadingPage(driver)
        listen_page = ListeningPage(driver)
        home_page = HomePage(driver)

        with allure.step("Click Google sign up and choose email"):
            account_creation_page.click_on_google_button()
            account_creation_page.wait_for_choose_account_popup()
            account_creation_page.choose_email_for_registration(email)
            account_creation_page.wait_for_choose_account_popup()

        with allure.step("Enter profile details"):
            profile_details_page.enter_first_name(firstname)
            profile_details_page.enter_last_name(lastname)
            profile_details_page.click_on_calender_btn()
            profile_details_page.select_date()
            profile_details_page.enter_language(language)
            profile_details_page.click_on_next_button()

        with allure.step("Select exam"):
            choose_exam_page.wait_for_selecting_exam()
            choose_exam_page.selecting_exam()
            choose_exam_page.choosing_exam()
            profile_details_page.click_on_next_button()

        with allure.step("Personalize experience"):
            personalize_page.wait_for_personalize_screen()
            personalize_page.select_country_button()
            personalize_page.choose_country_and_week()
            personalize_page.previously_attended_and_desired_score(score)
            personalize_page.click_on_continue_button()

        with allure.step("Start diagnostic test"):
            diagnostic_page.wait_for_diagnostic_test_page()
            diagnostic_page.click_on_speak_and_write()
            diagnostic_page.wait_for_diagnostic_write_page()
            diagnostic_page.enter_answers()
            profile_details_page.click_on_next_button()

        with allure.step("Complete speaking section"):
            diagnostic_page.wait_for_diagnostic_speaking()
            diagnostic_page.wait_for_diagnostic_test_page()
            speak_and_write.start_mic()
            speak_and_write.mic_stop()
            speak_and_write.click_on_submit()

        with allure.step("Complete reading section"):
            diagnostic_page.wait_for_diagnostic_test_page()
            reading_page.click_on_reading()
            reading_page.start_reading_section()

        with allure.step("Complete listening section"):
            diagnostic_page.wait_for_diagnostic_test_page()
            listen_page.click_on_listen()
            listen_page.wait_for_listening_screen()
            listen_page.start_listening_section()

        with allure.step("Verify user reaches home page after registration"):
            home_page.wait_for_score_page()
            home_page.scroll_till_home_btn_click()
            home_page.verify_new_registration()