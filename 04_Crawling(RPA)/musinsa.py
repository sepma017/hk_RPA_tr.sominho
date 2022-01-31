import requests
from bs4 import BeautifulSoup
from tqdm import tqdm_notebook

all_page_products = []

def get_total_page():
    url = "https://search.musinsa.com/ranking/best?u_cat_cd=002"
    html_page = requests.get(url).content
    soup = BeautifulSoup(html_page, 'html.parser')
    total_page = soup.select_one("#goodsRankForm > div.right_contents.hover_box > div.boxed-list-wrapper.rank-shop > div.thumbType_box.box > span.pagingNumber > span.totalPagingNum").text
    total_page = int(total_page)
    return total_page

def get_musinsa_product(category="002"):
    total_page = get_total_page()
    for page in tqdm_notebook(range(1, total_page+1)):
        url = "https://search.musinsa.com/ranking/best?mainCategory=002&page={}".format(page)

        html_page = requests.get(url.format(page)).content
        soup = BeautifulSoup(html_page, 'html.parser')
        products = soup.select("#goodsRankList > li")
        
        for product in products:

            # 상품 id
            product_id = product['data-goods-no']
            img_url = product.select_one("img.lazyload").get("data-original")
            product_brand = product.select_one("p.item_title").text
            product_detail_url = product.select_one("p.list_info > a").get("href")
            product_name = product.select_one("p.list_info").text.strip()
            product_price = product.select_one("p.price").text.split()
            product_price = float(product_price[-1].replace(",", "").replace("원", ""))
            start_count_elem = product.select_one("p.point > span.count")
            if start_count_elem:
                star_count = int(start_count_elem.text.replace(",", ""))
            else:
                star_count = 0

            item = {
                "product_id": product_id,
                "img_url": img_url,
                "product_brand":product_brand.strip(),
                "product_detail_url":product_detail_url,
                "product_name":product_name.strip(),
                "product_price":product_price,
                "star_count":star_count
            }

            all_page_products.append(item)
            
    return all_page_products
