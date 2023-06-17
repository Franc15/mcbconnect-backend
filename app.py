from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/api/v1')
def get_root():
    return jsonify({'message': 'Hello world from MCB Connect!'})


@app.route('/api')
def get_api():
    hello_dict = {'en': 'Hello', 'es': 'Hola'}
    lang = request.args.get('lang')
    return jsonify(hello_dict[lang])

app.run(use_reloader=True, debug=False)