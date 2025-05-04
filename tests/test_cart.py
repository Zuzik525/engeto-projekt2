# Tests around buying - shown items, add to cart
import re, random
from playwright.sync_api import Page, expect
from conftest import SITE_URL, extract_price


# Tests whether there are at least some items for sale on the homepage
def test_homepage_contains_sellable_items(page : Page):
    page.goto(SITE_URL)
    assert page.locator(".item .info .cart_insert_button").count() > 0

# Tests whether there are actions available, and some items for sale there
def test_actions(page : Page):
    page.goto(SITE_URL + "vypis.php?out=action")
    assert page.locator(".actionlist a").count() > 0 #there are actions listed
    assert page.locator(".item .info .cart_insert_button").count() > 0 #there are books for sale listed

# Tests adding to cart - click on some item, put in cart, show box, and cart price updated
def test_add_to_cart(page: Page):
    page.goto(SITE_URL)
    homepage_items = page.locator(".item .picture a") # Pick any item picture
    selected_item = homepage_items.all()[random.randint(0, homepage_items.count()-1)] #pick random item
    selected_item.click() #click on the item

    expect(page).to_have_url(re.compile(".*/detail/.*")) #check if redirected to detail page

    cart_sum_start = extract_price(page.locator(".topbar_cart_info_td.cost").inner_text()) # read cart total from header
    assert cart_sum_start.is_integer
    item_cost = extract_price(page.locator(".buy_form_cont_desktop .pricetable .ourprice").inner_text()) # read item price
    assert item_cost.is_integer

    page.locator(".buy_form_cont_desktop #detail_buy_button").click() # add to cart

    expect(page.locator("#footer .alert_box")).to_be_visible() #Check the bottom alert box was shown
    page.locator("#footer .alert_box a.link_mark").click() #follow to cart

    cart_sum_end = extract_price(page.locator(".topbar_cart_info_td.cost").inner_text()) # read updated cart total from header - after adding
    assert cart_sum_end.is_integer

    assert cart_sum_end == (cart_sum_start + item_cost) # Check if total matches when item was added
