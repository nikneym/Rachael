def kitapyurdu_query(query):
	search  = "https://www.kitapyurdu.com/index.php?route=product/search&filter_name=" + query + "&fuzzy=0&filter_in_stock=1"
	page = requests.get(search, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})

	search_soup = BeautifulSoup(page.content, "html.parser")
	product_items = search_soup.find_all("div", class_ = "product-cr")

	return product_items
pass