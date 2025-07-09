from playwright.sync_api import expect, Page, Dialog, BrowserContext

def test_windows(page: Page, context: BrowserContext):
    page.goto("https://demoqa.com/browser-windows")
    
    with context.expect_page() as new_tab:
        page.click("#tabButton")
    new_page = new_tab.value
    new_page.wait_for_load_state()
    expect(new_page.locator("h1")).to_have_text("This is a sample page")
    new_page.close()

    with context.expect_page() as new_win:
        page.click("#windowButton")
    new_window = new_win.value
    new_window.wait_for_load_state()
    expect(new_window.locator("h1")).to_have_text("This is a sample page")
    new_window.close()

    with context.expect_page() as new_popup:
        page.click("#messageWindowButton")
    popup = new_popup.value
    popup.wait_for_load_state()
    content = popup.evaluate("() => document.body.textContent")
    assert "Knowledge increases by sharing but not by saving." in content
    popup.close()

def test_alerts(page: Page):
    page.goto("https://demoqa.com/alerts")

    def handle_alert(dialog: Dialog):
        assert dialog.message == "You clicked a button"
        dialog.accept()
    page.once("dialog", handle_alert)
    page.click("#alertButton")

    def handle_timer(dialog: Dialog):
        assert dialog.message == "This alert appeared after 5 seconds"
        dialog.accept()
    page.once("dialog", handle_timer)
    page.click("#timerAlertButton")
    page.wait_for_timeout(6000)

    def handle_confirm(dialog: Dialog):
        assert dialog.message == "Do you confirm action?"
        dialog.dismiss()
    page.once("dialog", handle_confirm)
    page.click("#confirmButton")
    expect(page.locator("#confirmResult")).to_contain_text("Cancel")

    def handle_prompt(dialog: Dialog):
        assert dialog.message == "Please enter your name"
        dialog.accept("Gin Jin")
    page.once("dialog", handle_prompt)
    page.click("#promtButton")
    expect(page.locator("#promptResult")).to_contain_text("Gin Jin")

def test_frames(page: Page):
    page.goto("https://demoqa.com/frames")
       
    frame1 = page.frame_locator("#frame1")
    header1 = frame1.locator("h1").text_content()
    assert "This is a sample page" in header1

    frame2 = page.frame_locator("#frame2")
    header2 = frame2.locator("h1").text_content()
    assert "This is a sample page" in header2

def test_child_frames(page: Page):
    page.goto("https://demoqa.com/nestedframes")

    parent = page.frame_locator("#frame1")
    text_parent = parent.locator("body").text_content()
    assert "Parent frame" in text_parent

    child = parent.frame_locator("Iframe")

    assert "Child Iframe" in child.locator("p").text_content()

def test_modals(page: Page):
    page.goto("https://demoqa.com/modal-dialogs")

    page.click("#showSmallModal")
    expect(page.locator("div.modal-body")).to_contain_text("This is a small modal. It has very less content")
    page.click("#closeSmallModal")

    page.click("#showLargeModal")
    expect(page.locator("div.modal-body")).to_contain_text("Lorem Ipsum")
    page.click("#closeLargeModal")