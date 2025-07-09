from playwright.sync_api import expect, Page, BrowserContext

def test_text_box(page: Page):
    page.goto("https://demoqa.com/text-box")

    page.fill("#userName", "Nobody")
    page.fill("#userEmail", "mail@mail.com")
    page.fill("#currentAddress", "here")
    page.fill("#permanentAddress", "nowhere")
    page.click("#submit")
    expect(page.locator("#output")).to_contain_text("Nobody")
    page.screenshot(path="text_box.png", full_page=True)

def test_check_box(page: Page):
    page.goto("https://demoqa.com/checkbox")

    page.click("button[title='Toggle']")

    page.locator("label[for='tree-node-desktop']").locator("..").locator("button[title='Toggle']").click()
    page.locator("label[for='tree-node-documents']").locator("..").locator("button[title='Toggle']").click()
    page.locator("label[for='tree-node-downloads']").locator("..").locator("button[title='Toggle']").click()

    ids = ["tree-node-desktop", "tree-node-documents", "tree-node-downloads"]
    for id in ids:
        page.locator(f"label[for='{id}'] span.rct-checkbox").click()
        assert page.locator(f"#{id}").is_checked()

    
    expect(page.locator("#result")).to_contain_text("You have selected :")
    page.screenshot(path="check_box.png", full_page=True)

def test_radio_button(page: Page):
    page.goto("https://demoqa.com/radio-button")

    page.click("label[for='yesRadio']")
    expect(page.locator("span.text-success")).to_contain_text("Yes")
    assert page.locator("label[for='yesRadio']").is_checked()

    page.click("label[for='impressiveRadio']")
    expect(page.locator("span.text-success")).to_contain_text("Impressive")
    assert page.locator("label[for='impressiveRadio']").is_checked()

    # page.click("label[for='noRadio']")
    assert page.locator("label[for='noRadio']").is_disabled()

    page.screenshot(path="radio_button_test.png", full_page=True)

    
def test_table(page: Page):
    page.goto("https://demoqa.com/webtables")

    expect(page.locator(".rt-tbody .rt-tr-group")).to_have_count(10)

    page.click("#addNewRecordButton")
    page.fill("#firstName", "Gin")
    page.fill("#lastName", "Jin")
    page.fill("#userEmail", "mail@email.com")
    page.fill("#age", "30")
    page.fill("#salary", "50000")
    page.fill("#department", "Consulting")
    page.screenshot(path="table_test1.png", full_page=True)
    page.click("button[type='submit']")
    expect(page.locator(".rt-tbody")).to_contain_text("Gin")
    rows = page.locator(".rt-tbody .rt-tr-group")
    row_count = rows.count()
    for i in range(row_count):
        row_text = rows.nth(i).inner_text()
        print(f"Строка {i + 1}: {row_text}")
        with open("table_test.txt", "a", -1, "UTF-8") as file:
            file.write(f"Строка {i + 1}: {row_text}")
    page.screenshot(path="table_test2.png", full_page=True)

def test_buttons(page: Page):
    page.goto("https://demoqa.com/buttons")
    page.dblclick("#doubleClickBtn")
    expect(page.locator("#doubleClickMessage")).to_contain_text("double click")

    page.click("#rightClickBtn", button="right")
    expect(page.locator("#rightClickMessage")).to_contain_text("right click")

    page.locator("button[type='button']").nth(3).click()
    expect(page.locator("#dynamicClickMessage")).to_contain_text("dynamic click")

def test_links(page: Page, context: BrowserContext):
    page.goto("https://demoqa.com/links")

    with context.expect_page() as link_page:
        page.click("#simpleLink")

    new_page = link_page.value
    new_page.wait_for_load_state()
    assert "DEMOQA" in new_page.title()
    new_page.close()

    with context.expect_page() as link_tab:
        page.click("#dynamicLink")

    an_page = link_tab.value
    an_page.wait_for_load_state()
    assert "DEMOQA" in an_page.title()
    an_page.close()

    page.click("#created")
    expect(page.locator("#linkResponse")).to_contain_text("201")
    page.click("#no-content")
    expect(page.locator("#linkResponse")).to_contain_text("204")
    page.click("#moved")
    expect(page.locator("#linkResponse")).to_contain_text("301")
    page.click("#bad-request")
    expect(page.locator("#linkResponse")).to_contain_text("400")
    page.click("#unauthorized")
    expect(page.locator("#linkResponse")).to_contain_text("401")
    page.click("#forbidden")
    expect(page.locator("#linkResponse")).to_contain_text("403")
    page.click("#invalid-url")
    expect(page.locator("#linkResponse")).to_contain_text("404")
    
def test_img_link(page: Page, context: BrowserContext):
    page.goto("https://demoqa.com/broken")
    ok_pic = page.locator("img").nth(0).element_handle()
    is_broken = page.evaluate(
        """img => !img.complete || img.naturalWidth === 0""",
        ok_pic
    )
    assert not(is_broken), "First pic is okay"

    broken_pic = page.locator("img").nth(1).element_handle()
    is_broken = page.evaluate("""img => !img.complete || img.naturalWidth === 0""", broken_pic)

    assert broken_pic, "Second pic is broken"

    pics = page.locator("img")

    for i in range(pics.count()):
        pic = pics.nth(i).element_handle()
        if pic:
            is_broken = page.evaluate("""img => !img.complete || img.naturalWidth === 0""", pic)
            pic_src = pic.get_attribute("src")
            if (is_broken): print(f"Picture {pic_src} is broken")

    page.click("a[href='http://demoqa.com']")

    page.wait_for_load_state()
    assert "DEMOQA" in page.title()
    page.go_back()

    response = page.request.get("http://the-internet.herokuapp.com/status_codes/500")
    assert response.status == 500

    links = page.locator("a")
    for i in range(links.count()):
        href = links.nth(i).get_attribute("href")
        if href:
            response = page.request.get(href)
            print(response.status)


def test_download(page: Page):
    page.goto("https://demoqa.com/upload-download")
    with page.expect_download() as download_info:
        page.click("#downloadButton")
   
    download = download_info.value
    save_path = download.suggested_filename
    download.save_as(save_path)

    upload = "table_test.txt"

    page.set_input_files("#uploadFile", upload)

    what_uploaded = page.locator("#uploadedFilePath").text_content()
    assert "table_test.txt" in what_uploaded

def test_dynamic(page: Page):
    page.goto("https://demoqa.com/dynamic-properties")

    expect(page.locator("#enableAfter")).to_be_enabled(timeout=7000)

    expect(page.locator("#visibleAfter")).to_be_visible(timeout=7000)

    expect(page.locator("#colorChange")).to_have_class(
        "mt-4 text-danger btn btn-primary", timeout=7000
    )