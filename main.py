import requests
from bs4 import BeautifulSoup
import smtplib

MY_EMAIL = "Your email"
MY_PASSWORD = "Your password"
# import lxml

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",

}
query_endpoint = "https://www.amazon.in/dp/B07PBBRWFG/ref=s9_acsd_hps_bw_c2_x_0_i?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-3&pf_rd_r=JMBDDTR1MHGJRGGPA6NG&pf_rd_t=101&pf_rd_p=ed8068a8-8735-4eaf-933d-b76046676be6&pf_rd_i=18590956031"
response = requests.get(url=query_endpoint, headers=headers)
contents = response.text

soup = BeautifulSoup(contents, 'html.parser')

price = float(soup.find(name='span', id="priceblock_ourprice").getText().split()[1])
product_title = soup.find(name='span', id="productTitle").getText().strip()
print(price, product_title)

message = f"{product_title} costs you just ₹{price}\n{query_endpoint}"
if price < 1000.00:
    with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs='receiver email address',
                            msg=f"Subject:Amazon price alert!!\n\n{message}".encode('utf-8'))
