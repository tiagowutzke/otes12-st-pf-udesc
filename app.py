import os

from flask import Flask, request, jsonify, render_template

from tdd.test import Test
from broker.broker import Broker
from database.database_adapter import DatabaseAdapter

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# pages
index = '/'
index_test = '/test'
new_project = '/new-project'
test_factor = '/test-factor'
general_system_features = '/general-system-features'

# broker pattern
broker_route = "/broker"


@app.route(index)
def index_function():
    return render_template('index.html')


@app.route(index_test)
def index_test_function():
    return render_template('index_test.html')


@app.route(new_project)
def new_project_function():
    return render_template('new_project.html')


@app.route(test_factor)
def test_factor_function():
    return render_template('test_factor.html')


@app.route(general_system_features)
def general_system_features_function():
    database = DatabaseAdapter()
    result, projects = database.select_all('projetos', '*')
    database.close()
    return render_template('general_system_features.html', rows=projects)


@app.route(broker_route, methods=['GET', 'PUT', 'DELETE'])
def broker_function():
    payload = request.get_json(force=True)

    response = Broker(
        request_type=request.method,
        microservice=payload.get('microservice'),
        payload=payload.get('payload')
    ).broker_services()

    return jsonify(response)


@app.route('/tdd')
def tdd_function():
    payload = request.get_json(force=True)

    tdd = Test().test_medidas_projeto(
        real_finish=payload.get('real_finish'),
        plan_finish=payload.get('plan_finish'),
        real_begin=payload.get('real_begin'),
        expected=payload.get('expected'),
    )

    return jsonify(tdd)


@app.route('/tdd-test-factor?<payload>', methods=['GET'])
def tdd_test_factor_function():
    payload = request.get_json(force=True)

    tdd = Test().test_fator_teste(
        linhas_teste=payload.get('test_lines'),
        linhas_prod=payload.get('test_prod'),
        expected=payload.get('expected')
    )
    print(tdd)
    return jsonify(tdd)


if __name__ == "__main__":
    from environ import set_environ_variables
    set_environ_variables()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

