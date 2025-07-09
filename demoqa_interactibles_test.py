from playwright.sync_api import expect, Page

def test_selectable(page: Page):
    page.goto("https://demoqa.com/selectable")

    page.locator(".list-group-item").filter(has_text="Cras justo odio").click()
    expect(page.locator(".list-group-item").filter(has_text="Cras justo odio")).to_contain_class("active")
    page.locator(".list-group-item").filter(has_text="Cras justo odio").click()
    expect(page.locator(".list-group-item").filter(has_text="Cras justo odio")).not_to_contain_class("active")

    page.locator(".list-group-item").filter(has_text="Dapibus ac facilisis in").click()
    expect(page.locator(".list-group-item").filter(has_text="Dapibus ac facilisis in")).to_contain_class("active")
    page.locator(".list-group-item").filter(has_text="Dapibus ac facilisis in").click()
    expect(page.locator(".list-group-item").filter(has_text="Dapibus ac facilisis in")).not_to_contain_class("active")

    page.locator(".list-group-item").filter(has_text="Morbi leo risus").click()
    expect(page.locator(".list-group-item").filter(has_text="Morbi leo risus")).to_contain_class("active")
    page.locator(".list-group-item").filter(has_text="Morbi leo risus").click()
    expect(page.locator(".list-group-item").filter(has_text="Morbi leo risus")).not_to_contain_class("active")

    page.locator(".list-group-item").filter(has_text="Porta ac consectetur ac").click()
    expect(page.locator(".list-group-item").filter(has_text="Porta ac consectetur ac")).to_contain_class("active")
    page.locator(".list-group-item").filter(has_text="Porta ac consectetur ac").click()
    expect(page.locator(".list-group-item").filter(has_text="Porta ac consectetur ac")).not_to_contain_class("active")

    page.click("#demo-tab-grid")
    expect(page.locator("#demo-tabpane-grid")).to_be_visible()

    page.locator("#row1 .list-group-item").filter(has_text="One").click()
    expect(page.locator("#row1 .list-group-item").filter(has_text="One")).to_contain_class("active")
    page.locator("#row1 .list-group-item").filter(has_text="One").click()
    expect(page.locator("#row1 .list-group-item").filter(has_text="One")).not_to_contain_class("active")

    grid_items = page.locator("#demo-tabpane-grid .grid-container .list-group-item")
    for i in range(grid_items.count()):
        grid_items.nth(i).click()
        expect(grid_items.nth(i)).to_contain_class("active")
        grid_items.nth(i).click()
        expect(grid_items.nth(i)).not_to_contain_class("active")
