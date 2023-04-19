## 날씨 정보 가져 오기 ##
from bs4 import BeautifulSoup
from datetime import datetime
import requests




error_message = {'Null Input':'''<!DOCTYPE html>
                <html>
                    <body>
                        <h1>Null Input Error: <br>멍청아 검색어를 입력하라고</h1>
                        <form action="/">
                            <button type = 'submit'>홈으로 돌아가기</button>
                        </form>
                    </body>
                </html>''', 

                'Wrong Input':'''<!DOCTYPE html>
                <html>
                    <body>
                        <h1>Wrong Input Error:<br>다시 입력해보세요.<br>입력예시: 대구 북구 동천동</h1>
                        <form action="/">
                            <button type = 'submit'>홈으로 돌아가기</button>
                        </form>
                    </body>
                </html>''', 

                'Inner Error':'''<!DOCTYPE html>
                <html>
                    <body>
                        <h1>Inner Error:<br>개발자가 오류냄 ㅅㄱ<br>개발자 연락처: 01090300735</h1>
                        <form action="/">
                            <button type = 'submit'>홈으로 돌아가기</button>
                        </form>
                    </body>
                </html>'''}

weather_by_time = []
all_data = {}
location = ''


# cnt = 0



def timeconv(time):

    if int(time[0]) > 12:
        pm = int(time[0]) % 12
        time[0] = pm
        return f'오후 {time[0]}:{time[1]}'
    else:
        return f'오전 {time[0]}:{time[1]}'
 


def give_data(query):
    global all_data, location, weather_by_time

    clar = False
    url = 'https://search.naver.com/search.naver?query='+query.strip().replace(' ','+')+'+날씨'
    now = datetime.now().strftime('%H %M').split()
    print(url)
    
    
    weather_by_time = []
    other_data = {}
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    location = soup.find('div', {'class':'title_area _area_panel'}).find('h2',{'class':'blind'}).text
    
    try: # 오타 정정 코드
        clarify = soup.find('div', {'class':'suggest_wrap'}).find('strong',{'class':'source'}).text
        print(clarify)
        clar = True
        all_data['지역'] = f'{clarify.split()[0]} {location}'
    except:
        pass
        
    
    try:
        # define data
        temp = soup.find('div', {'class':'temperature_text'}).text.strip()[5:]
        status = soup.find('span', {'class':'weather before_slash'}).text
        air = soup.find('ul', {'class':'today_chart_list'})
        air_info = air.find_all('a')
        max_temp = soup.find('span', {'class':'highest'}).text[4:]
        min_temp = soup.find('span', {'class':'lowest'}).text[4:]
        location = soup.find('div', {'class':'title_area _area_panel'}).find('h2',{'class':'blind'}).text
        compare = soup.find('div', {'class':'temperature_info'}).find(('span', {'class':'temperature up'})).text
        feel_temp = soup.find('div', {'class':'temperature_info'}).find(('dd', {'class':'desc'})).text
        weather_icon = soup.find('div', {'class':'weather_info'}).find(('i', {'class':'wt_icon ico_wt1'}))
        by_time = soup.find('div', {'class':'graph_inner _hourly_weather'}).find('ul')
        by_time_info = soup.find_all('li', {'class':'_li'})
        loc = f'{location}'
        #image_link = image_target['style'].split('url(')[1].split(')')[0]

        #weather_image_link = image_tag['style']
        #tail_location = soup.find('div', {'class':'title_area _area_panel'}).find('h2',{'class':'blind'}).text
        
        #head_location = soup.find('div', {'class': 'filter_cont'}).find('li', {'aria-selected': 'true'}).text
        #tail_location = soup.find('div', {'class':'title_area _area_panel'}).find('h2',{'class':'blind'}).text
        #location = f'{head_location.split()[0]} {tail_location}'
        
        #fhw = soup.find('dl', {'class':'summary_list'}).text.strip()      #.find('dd', {'class':'desc'}
        
        # 기타 데이터
        for i in air_info:
            others = i.text.strip().split()
            other_data[others[0]] = others[1] # create dict
    
        if others[0] == '일몰':
            whatsun = '일몰'
        else:
            whatsun = '일출'
         
        fine_dust = other_data['미세먼지']
        ult_fine_dust = other_data['초미세먼지']
        uv = other_data['자외선']
        sun = others[1]

        # 오타 정정 처리
        if clar == False:
            all_data['지역'] = loc
            clar = True
        else:
            pass

        # 날씨 비교
        if compare[1] == '높아요':
            compare_change = f'{compare.split()[0]}↑'
        else:
            compare_change = f'{compare.split()[0]}↓'

        # 시간별 데이터

        print('*** Weather by Time ***')
        cnt = 0
        for i in by_time_info:
            cnt+=1
            if cnt >= 24:
                break
            else:
                data_by_time = i.text.strip().split() # 시간별 날씨
                weather_by_time.append({'시간':data_by_time[0],'날씨':data_by_time[1],'온도':data_by_time[2]})
                #print(f'{data_by_time[0]}| \t 날씨:{data_by_time[1]} \t 기온:{data_by_time[2]}')

        # visualization
        for i in weather_by_time:
            print('\t')
            for key, value in i.items():
                print(key,':', value)
        print('='*30)



        content = ''
        for i in weather_by_time:

            hour = i['시간']
            w_icon = i['날씨']
            degree = i['온도']

            content = content + f'''
            <li class="_li">
              <dl class="graph">
                <dt class = hour>
                  <em>{hour}</em>
                </dt>
                <dd class = wt>{w_icon}</dd>
                <dd class = degree>{degree}</dd>
              </dl>
            </li>
            '''


        
        # gethering data
        all_data.update({'현재시각': timeconv(now),\
                        '현재기온': temp[:-1],\
                        '최고':max_temp,\
                        '최저':min_temp,\
                        '날씨':status,\
                        '미세먼지':fine_dust,\
                        '초미세먼지':ult_fine_dust,\
                        '자외선':uv,\
                        '어제보다':compare_change,\
                        '체감온도':feel_temp,\
                        '시간별':weather_by_time,\
                        '그래프':content,\
                        whatsun:sun})
                        
        print('='*30)
        for key, value in all_data.items():
            if key == '시간별':
                break
            print(key, ':', value)
        print('='*30)
        
        return all_data
    
    
    except Exception as e:
        if e == AttributeError:
            return error_message['Wrong Input']
        
        else:
            print(e)
            return error_message['Inner error']
       
    

    
        


    

