def steam_query(query):
	#page = requests.get(search, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
	page = requests.get(query)
	soup = BeautifulSoup(page.content, "html.parser")
	top_sellers = soup.find("div", id = "TopSellersRows")
	top_sellers_item = top_sellers.find_all("a", class_ = "tab_item")

	return top_sellers_item
pass