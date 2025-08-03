from web_browser_utils import open_website_and_get_texts

url = "https://www.wix.com/"
texts = open_website_and_get_texts(url)

for t in texts[:20]:
    print("•", t)
