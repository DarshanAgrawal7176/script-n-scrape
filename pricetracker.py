# import required files and modules
import requests
from bs4 import BeautifulSoup
import smtplib
import time
import json

#Open the params.json file
with open('params.json','r') as file:
    params = json.load(file)
    
headers = {
    "User-Agent": params['User-Agent']
}

# function to check if the price has dropped below 20,000
def check_price(soup, prev_price=0):
  
    #TODO 1: Fetch the Product Title (it should be a string) using the soup object
    #<START>
    title = soup.find('span', id='productTitle')
    #<END>

    #TODO 2: Fetch the Price using the Soup Object. It should also be a string
    #<START>
    price = soup.find("span", {"class": "a-price-whole"})
    print(price)
    #<END>
    
    #converting the string amount to float
    if price:
        price_text = price.get_text(strip=True)
        price_text = ''.join(filter(str.isdigit, price_text))
        converted_price = float(price_text) if price_text else 0.0
    else:
        converted_price = 0.0
    
    print(f"Price of the product: {converted_price}")
    
    if prev_price == 0:
        send_mail(converted_price, below_budget=False)
    elif converted_price < params['Target_Price']:
        send_mail(converted_price, below_budget=True)
    else:
        diff = prev_price - converted_price
        send_mail(diff, below_budget=False)
    
    return converted_price

# function that sends an email if the prices fell down
def send_mail(diff,below_budget=True):
  
  if below_budget:
    
    server = smtplib.SMTP('smtp.gmail.com', 587)    
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(params["Sender_Email"], params["Sender_Email_Password"])   #enter sender email id and sender email id password

    subject = 'Price Update!!!'
    URL = params["URL"]
    body = f"Check the amazon link {URL}"

    msg = f"Subject: {subject}\n\n{body}"
    
    server.sendmail(
      params["Sender_Email"],   # enter sender email id
      params["Reciever_Email"], # enter receiver email id
      msg                   # message that is to be sent
    )
    #print a message to check if the email has been sent
    print('Hey Email has been sent')
    # quit the server
    server.quit()

  if not below_budget:

    if (diff<0):
      subject = f'Price Has Risen By {(-1*diff)}!'
      URL = params["URL"]
      body = f"Check the amazon link {URL}"
    elif(diff>0):
      subject = f'Price Has Fallen By {diff}!'
      URL = params["URL"]
      body = f"Check the amazon link {URL}"   
    
    else:
       return # if the no price change, then do not send mail
        
    print('Price is still higher than Target Price')
    server = smtplib.SMTP('smtp.gmail.com', 587)    
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(params["Sender_Email"], params["Sender_Email_Password"])   #enter sender email id and sender email id password
      
    msg = f"Subject: {subject}\n\n{body}"
    
    server.sendmail(
      params["Sender_Email"],   # enter sender email id
      params["Receiver_Email"], # enter receiver email id
      msg                   # message that is to be sent
    )
    #print a message to check if the email has been sent
    print('Hey, an Email has been sent')
    # quit the server
    server.quit()
    
#loop that allows the program to regularly check for prices
prev_price = 0 

while(True):

  # send a request to fetch HTML of the page
  #TODO 3: Fetch the response oject from URL and headers specified in params.json using requests library
  #<START>
  # Fetch the webpage
  response = requests.get("https://www.amazon.in/OnePlus-Snapdragon-Stainless-Sapphire-Frequency/dp/B0CVQ5H9M3/ref=pd_ci_mcx_pspc_dp_d_2_i_2?pd_rd_w=PpK1E&content-id=amzn1.sym.b5387062-d66f-4264-a2b3-7498b12700ed&pf_rd_p=b5387062-d66f-4264-a2b3-7498b12700ed&pf_rd_r=EBVWNZ5VPQ4Z3D1HHAP2&pd_rd_wg=mVTve&pd_rd_r=12b9d159-627c-44a7-a1f2-e3968ec55fca&pd_rd_i=B0CVQ5H9M3", headers=headers)
  #<END>

  # create the soup object  
  #<TODO 4: Parse the response into a bs4 soup object using appropriate parser and encoding and store it in an object named soup
  # Parse the HTML
  soup = BeautifulSoup(response.content, "html.parser")
  #<END>

  prev_price = check_price(soup, prev_price)
  time.sleep(params['Time_Interval']) # the time after which you want the program to check the price in seconds. It is currently set to 1 day


