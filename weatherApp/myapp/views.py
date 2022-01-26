import attr
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Create your views here.

def get_html_content(request):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    city = request.GET.get('city')
    city=city.replace(' ','+')
    html_content = session.get(f'https://www.google.com/search?q=weather+in+{city}').text
    return html_content

def home(request):

    weather_data = None
    if 'city' in request.GET:
        #fetch data
        
        html_content = get_html_content(request)

        soup = BeautifulSoup(html_content, "html.parser")
        weather_data = dict()

        weather_data['region'] = soup.find("span", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text

        weather_data['temp_now'] = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text

        weather_data['dayhour'], weather_data['weather_now'] = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text.split('\n')
       
    return render(request,'myapp/home.html',{'weather': weather_data})
