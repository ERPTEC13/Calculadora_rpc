from flask import Flask, render_template, request, redirect, url_for
import calculator_pb2
import calculator_pb2_grpc
import grpc

app = Flask(__name__)

# Função para conectar ao servidor gRPC
def get_calculator_response(number1, number2, operation):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        request = calculator_pb2.OperationRequest(number1=number1, number2=number2)
        
        if operation == 'add':
            response = stub.Add(request)
        elif operation == 'subtract':
            response = stub.Subtract(request)
        elif operation == 'multiply':
            response = stub.Multiply(request)
        elif operation == 'divide':
            response = stub.Divide(request)
        else:
            response = None

        return response.result if response else "Operação inválida"

# Rota principal para exibir a calculadora
@app.route("/")
def index():
    return render_template("index.html", result=None)

# Rota para processar o cálculo
@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        number1 = float(request.form["number1"])
        number2 = float(request.form["number2"])
        operation = request.form["operation"]
        
        # Chamar a função para enviar a solicitação ao servidor gRPC
        result = get_calculator_response(number1, number2, operation)
        
        return render_template("index.html", result=result)
    except Exception as e:
        return render_template("index.html", result=f"Erro: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
