# Tests cartsave functionality - save and load
import re, random
from playwright.sync_api import Page, expect
from conftest import CART_SAVE_MAIL, SITE_URL, extract_price

# Tests saving saved cart
def test_cart_save(page : Page):
    page.goto(SITE_URL)
    
    for x in range(5): # do it few times
        homepage_items = page.locator(".item .info .cart_insert_button") # Pick item cart buttons on page
        selected_item = homepage_items.all()[random.randint(0, homepage_items.count()-1)] #pick random item
        selected_item.click() #click on the item (add to cart)

    page.locator(".topbar_cart_info").click() #navigate to cart

    page.locator(".cartsavebutton").all()[1].click() #push second button (save cart)
    expect(page).to_have_url(re.compile(".*cartsave")) #check if redirected to cart save page

    page.locator("#content input[name='mail']").fill(CART_SAVE_MAIL) #fill in email
    page.locator("#content input[name='newsletter_agree']").uncheck() #UNcheck newsletter
    page.locator("#content input[type='submit']").click() #save cart

    expect(page.locator("#content .ok")).to_be_visible() #detect success message


# Tests loading saved cart
def test_cart_load(page : Page):
    page.goto(SITE_URL + "vypis.php?out=cartload")

    page.locator("#content input[name='mail']").fill(CART_SAVE_MAIL) #fill in detail
    page.locator("#content input[type='submit']").click() #send the form

    
    cart_sum_start = extract_price(page.locator(".topbar_cart_info_td.cost").inner_text()) # read cart total from header
    assert cart_sum_start.is_integer
    page.locator(".profile_savedcarts_table .main_button").first.click() #Click on first main button -> Add whole cart

    cart_sum_end = extract_price(page.locator(".topbar_cart_info_td.cost").inner_text()) # read cart total from header - after adding
    assert cart_sum_end.is_integer

    assert cart_sum_end > cart_sum_start