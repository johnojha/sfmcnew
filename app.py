from twilio.rest import Client
from flask import Flask, jsonify, request
from flask_cors import CORS

import random
import http.client, urllib.parse, urllib.error, json

application = app = Flask(__name__)
CORS(app)

account_sid = 'AC320e696ec10b592a64bc614ffcf81c1c'
auth_token = '7b792eab5b495ae11ed31ba5bea398d8'

client = Client(account_sid, auth_token)

params = urllib.parse.urlencode({'bot': 'x1592563667910'})
headers = {
    'Content-Type': 'application/json',
    'x-auth-token': '0c38934e5a1e957394af6af7bc668d823eb6796a12038deb5e06d3964f7a81e2',
    'Host': 'app.yellowmessenger.com'
}


@app.route('/')
def index():
    return jsonify({
        'success': True,
        'message': 'This is index route!'
    })


@app.route('/sendMessage', methods=['POST'])
def send_message():
    if request.method == 'POST':
        received_data = request.get_json()
        print(received_data)
        try:
            arguments = received_data.get('inArguments')
            name = str(arguments[2]['Name'])
            number = '+' + str(arguments[1]['Phone'])
            message = 'Hi ' + name + ', \n' + str(arguments[0]['Message'])

            if number is None:
                print('Number not received!')
                return jsonify({
                    'success': False,
                    'error_message': 'Please provide the number!'
                })

            if arguments is None:
                print('In Arguments not received!')
                return jsonify({
                    'success': False,
                    'error_message': 'No message attribute received!'
                })

            response = client.messages.create(to=number, from_='+12053950462', body=message)

        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e),
                'error_route': '/sendMessage'
            })

        return jsonify({
            'success': True,
            'message': 'Successfully Executed Action!',
            'message_id': response.sid,
            'message_body': response.body,
            'sent_date': response.date_created,
            'sent_from': response.from_,
            'sent_to': response.to,
            'cost': response.price,
            'number_of_segments': response.num_segments,
            'direction': response.direction
        })


@app.route('/sendWhatsappText', methods=['POST'])
def send_whatsapp_text():
    if request.method == 'POST':
        try:
            received_data = request.get_json()

            print(received_data)

            otp = random.randint(100000, 999999)
            
            arguments = received_data.get('inArguments')
            name = str(arguments[1]['Name'])
            number = 'whatsapp:+' + str(arguments[0]['Phone'])
            message = 'Your SFMC Testing pin code is ' + str(otp)

            if number is None:
                print('Number not received!')
                return jsonify({
                    'success': False,
                    'error_message': 'Please provide the number!'
                })

            if arguments is None:
                print('In Arguments not received!')
                return jsonify({
                    'success': False,
                    'error_message': 'No message attribute received!'
                })

            response = client.messages.create(to=number, from_='whatsapp:+12053950462', body=message)

        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e),
                'error_route': '/sendWhatsapp'
            })

        return jsonify({
            'success': True,
            'message': 'Successfully Executed Action!',
            'message_id': response.sid,
            'message_body': response.body,
            'sent_date': response.date_created,
            'sent_from': response.from_,
            'sent_to': response.to,
            'cost': response.price,
            'number_of_segments': response.num_segments,
            'direction': response.direction
        })


@app.route('/sendWhatsapp', methods=['POST'])
def send_whatsapp():
    if request.method == 'POST':
        try:
            received_data = request.get_json()
            print('Received Data', received_data)
            arguments = received_data.get('inArguments')

            number = arguments[0]['Phone']
            name = arguments[1]['Name']

            request_body = json.dumps({
                "body": {
                    "to": number,
                    "ttl": 200000,
                    "type": "template",
                    "template": {
                        "namespace": "95610748_ad07_4389_8b93_373d536063f0",
                        "language": {
                            "policy": "deterministic",
                            "code": "en"
                        },
                        "name": "precautionary_measures",
                        "components": [
                            {
                                "type": "header",
                                "parameters": [
                                    {
                                        "type": "image",
                                        "image": {
                                            "link": "https://linkpicture.com/q/precautions.jpg"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            })

            conn = http.client.HTTPSConnection('app.yellowmessenger.com')
            conn.request("POST", "/integrations/whatsapp/send?%s" % params, body=request_body, headers=headers)
            response = conn.getresponse()
            response_data = json.loads(response.read().decode('ascii'))
            conn.close()

        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'something went wrong!'
            })

        return response_data


if __name__ == '__main__':
    app.run(debug=True)
