from playwright.sync_api import expect, Page

def test_form(page: Page):
    page.goto("https://demoqa.com/automation-practice-form")

    page.fill("#firstName", "Gin")
    page.fill("#lastName", "Jin")
    page.fill("#userEmail", "mail@mail.com")
    page.click("label[for='gender-radio-3']")
    page.fill("#userNumber", "7896178273")

    page.click("#dateOfBirthInput")
    page.fill("#dateOfBirthInput", "09 Jan 2025")
    page.press("#dateOfBirthInput", "Enter")

    page.fill("#subjectsInput", "Physics")
    page.press("#subjectsInput", "Enter")

    page.wait_for_selector("label[for='hobbies-checkbox-1']")
    page.click("label[for='hobbies-checkbox-1']")
    page.click("label[for='hobbies-checkbox-2']")

    page.set_input_files("#uploadPicture", "sampleFile.jpeg")
    uploaded_file = page.locator("#uploadPicture").evaluate("el => el.files[0]?.name")
    assert uploaded_file == "sampleFile.jpeg"

    page.fill("#currentAddress", "nowhere here")

    page.locator("#state").scroll_into_view_if_needed()
    page.click("#state")
    page.locator("div[id^='react-select-3-option-']").filter(has_text="NCR").click()

    page.click("#city")
    page.locator("div[id^='react-select-4-option-']").filter(has_text="Delhi").click()

    page.click("#submit")

    expect(page.locator("#example-modal-sizes-title-lg")).to_have_text("Thanks for submitting the form")
    expect(page.locator("td").nth(1)).to_contain_text("Gin Jin")

    page.screenshot(path="form_result.png", full_page=True)
    page.click("#closeLargeModal")
