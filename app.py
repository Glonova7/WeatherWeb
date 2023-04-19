from flask import Flask, render_template, request
from weather_get_data import give_data, error_message, all_data, weather_by_time


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        return error_message['Null Input']    
    else:
        try:
            give_data(query)    
            return render_template('result.html',\
                                    temp=all_data['현재기온'], weather=all_data['날씨'],\
                                    location = all_data['지역'],time = all_data['현재시각'],\
                                    dust = all_data['미세먼지'], ult_dust = all_data['초미세먼지'],\
                                    uv = all_data['자외선'],compare = all_data['어제보다'],\
                                    feel_temp = all_data['체감온도'], content = all_data['그래프'])
        except TypeError as Te:
            print('TypeError:', Te)
            return error_message['Wrong Input']
        except KeyError as Ke:
            print('KeyError:', Ke)
            return error_message['Wrong Input']
        except AttributeError as Ae:
            print('AttributeError:', Ae)
            return error_message['Wrong Input']
        except Exception as e:
            print('InnerError:',e)
            return error_message['Inner Error']
        




if __name__== "__main__":
	    app.run(port=5000, debug = True)