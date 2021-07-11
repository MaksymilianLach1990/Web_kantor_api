from flask import Flask, render_template, request
import requests


app = Flask(__name__)
app.config['ENV'] = 'development'
response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
file = response.json()
rates = file[0]['rates']
codes = []
value = 0
for name in file[0]['rates']:
    codes.append(name['code'])

def exchange_price(value, currency):
    price = 0
    for ask in rates:
        if ask['code'] == currency:
            price = ask['ask']
            break
    return round((float(value) * float(price)), 2)


@app.route('/exchange', methods=['GET', 'POST'])
def exchange():
    if request.method == 'POST':
        data = request.form
        value = data.get('value')
        print(value)
        currency = data.get('codes')

        if int(value) >= 0 and currency in codes:
            answer = exchange_price(value, currency)
            return render_template("answer.html", value=value, currency=currency, answer=answer)


    return render_template("exchange.html", rates=rates, codes=codes)






if __name__ == "__main__":
    app.run(debug=True)
