from playwright.sync_api import expect, Page
import time

def test_accordion(page: Page):
    page.goto("https://demoqa.com/accordian")

    page.click("#section1Heading")
    expect(page.locator("#section1Content p")).to_contain_text("Lorem Ipsum is simply dummy text")
    page.click("#section1Heading")

    page.click("#section2Heading")
    expect(page.locator("#section2Content")).to_contain_text("Contrary to popular belief")
    page.click("#section2Heading")

    page.click("#section3Heading")
    expect(page.locator("#section3Content p")).to_contain_text("It is a long established")
    page.click("#section3Heading")

def test_autofill(page: Page):
    page.goto("https://demoqa.com/auto-complete")

    inp1 = page.locator("#autoCompleteMultipleInput")
    
    inp1.fill("Gree")
    page.locator("div[id^='react-select-2-option']").filter(has_text="Green").click()
    inp1.fill("Blue")
    page.locator("div[id^='react-select-2-option']").filter(has_text="Blue").click()
    inp1.fill("Blac")
    page.locator("div[id^='react-select-2-option']").filter(has_text="Black").click()

    expect(page.locator(".auto-complete__multi-value")).to_have_count(3)

    page.locator(".auto-complete__multi-value__remove").nth(1).click()
    expect(page.locator(".auto-complete__multi-value")).to_have_count(2)

    inp2 = page.locator("#autoCompleteSingleInput")
    inp2.fill("Yello")

    page.locator("div[id^='react-select-3-option']").filter(has_text="Yellow").click()
    expect(page.locator(".auto-complete__single-value")).to_have_text("Yellow")

def test_date(page: Page):
    page.goto("https://demoqa.com/date-picker")

    date = page.locator("#datePickerMonthYearInput")
    date.click()
    date.fill("06/02/2025")
    page.keyboard.press("Enter")
    assert date.input_value() == "06/02/2025"

    time = page.locator("#dateAndTimePickerInput")
    time.click()

    page.locator(".react-datepicker__day").nth(4).click()

    page.locator(".react-datepicker__time-list-item").filter(has_text="12:00").click()

    assert "July 3, 2025" in time.input_value()
    assert "12:00 PM" in time.input_value()

def test_slider(page: Page):
    page.goto("https://demoqa.com/slider")

    slider = page.locator("input[type='range']")

    old = page.locator("#sliderValue").input_value()
    slider.bounding_box()
    slider.hover()
    page.mouse.down()
    page.mouse.move(slider.bounding_box()["x"] + 50, slider.bounding_box()["y"])

    def wait_for_change(locator, old_value, timeout = 5):
        start_time = time.time()
        while time.time() - start_time < timeout:
            current = locator.input_value()
            if current != old_value:
                return
            time.sleep(0.1)
        raise "Value did not change"

    wait_for_change(page.locator("#sliderValue"), old)
    page.screenshot(path="slider_test.png", full_page=True)
    assert int(page.locator("#sliderValue").input_value()) < 30

def test_progress(page: Page):
    page.goto("https://demoqa.com/progress-bar")

    page.click("#startStopButton")
    page.wait_for_function("() => document.querySelector('.progress-bar').textContent.includes('3')")
    page.screenshot(path="progress_30.png", full_page=True)
    page.click("#startStopButton")
    assert page.locator(".progress-bar").text_content() != "0%"
    page.click("#startStopButton")
    page.wait_for_function("() => document.querySelector('.progress-bar').textContent.trim() === '100%'")
    assert page.locator(".progress-bar").text_content() == "100%"
    page.screenshot(path="progress_100.png", full_page=True)
    page.click("#resetButton")
    page.wait_for_function("() => document.querySelector('.progress-bar').textContent.trim() === '0%'")
    assert page.locator(".progress-bar").text_content() == "0%"

def test_tabs(page: Page):
    page.goto("https://demoqa.com/tabs")

    assert "Lorem Ipsum is simply dummy text" in page.locator("#demo-tabpane-what").text_content()

    page.click("#demo-tab-origin")
    page.wait_for_selector("#demo-tabpane-origin[aria-hidden='false']")
    assert "Contrary to popular belief" in page.locator("#demo-tabpane-origin").text_content()
    page.screenshot(path="tab1.png")
    
    page.click("#demo-tab-use")
    page.wait_for_selector("#demo-tabpane-use[aria-hidden='false']")
    assert "It is a long established fact" in page.locator("#demo-tabpane-use").text_content()
    page.screenshot(path="tab2.png")

    expect(page.locator("#demo-tab-more")).to_be_disabled()

def test_tips(page: Page):
    page.goto("https://demoqa.com/tool-tips")

    button = page.locator("#toolTipButton")
    button.hover()
    expect(page.locator(".tooltip-inner")).to_have_text("You hovered over the Button")
    page.mouse.move(0, 0)
    expect(page.locator(".tooltip-inner")).not_to_be_visible()
    
    page.locator("#toolTipTextField").hover()
    expect(page.locator(".tooltip-inner")).to_have_text("You hovered over the text field")
    page.mouse.move(0, 0)
    expect(page.locator(".tooltip-inner")).not_to_be_visible()

    
    page.locator("#texToolTopContainer a:nth-child(1)").hover()
    expect(page.locator(".tooltip-inner")).to_have_text("You hovered over the Contrary")
    page.mouse.move(0, 0)
    expect(page.locator(".tooltip-inner")).not_to_be_visible()
    
    page.locator("#texToolTopContainer a:nth-child(2)").hover()
    expect(page.locator(".tooltip-inner")).to_have_text("You hovered over the 1.10.32")

def test_menu(page: Page):
    page.goto("https://demoqa.com/menu")

    page.locator("ul#nav > li:has-text('Main Item 2')").hover()
    page.locator("ul#nav > li:has-text('SUB SUB LIST »')").hover()

    expect(page.locator("ul#nav > li:has-text('Sub Sub Item 1')")).to_be_visible()
    expect(page.locator("ul#nav > li:has-text('Sub Sub Item 2')")).to_be_visible()


def test_select(page: Page):
    page.goto("https://demoqa.com/select-menu")

    page.click("#withOptGroup")
    page.locator("div[id^='react-select-2-option-']").filter(has_text="A root option").click()
    expect(page.locator("#withOptGroup")).to_contain_text("A root option")

    page.click("#selectOne")
    page.locator("div[id^='react-select-3-option-']").filter(has_text="Mrs.").click()
    expect(page.locator("#selectOne")).to_contain_text("Mrs.")

    page.select_option("#oldSelectMenu", "3")
    assert page.locator("#oldSelectMenu").input_value() == "3"
    

    input_field = page.locator("#react-select-4-input")

    input_field.fill("Green")
    page.keyboard.press("Enter")

    input_field.fill("Blue")
    page.keyboard.press("Enter")

    input_field.fill("Black")
    page.keyboard.press("Enter")

    assert page.locator(".css-1rhbuit-multiValue").count() == 3

    cars = page.locator("#cars")
    cars.select_option(["audi", "volvo"])
    selected = cars.evaluate("el => Array.from(el.selectedOptions).map(o => o.value)")
    assert "audi" in selected and "volvo" in selected
