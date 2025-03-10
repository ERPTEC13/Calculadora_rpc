from concurrent import futures
import grpc
import calculator_pb2
import calculator_pb2_grpc

class CalculatorService(calculator_pb2_grpc.CalculatorServicer):
    def log_request(self, operacao, numero1, numero2, resultado):
        """Log de cada solicitação do cliente de forma estruturada e detalhada."""
        print("--------- Serviço RPC (Servidor) ---------")
        print("Cliente solicita:")
        print(f"Operação de {operacao} para {numero1:.2f} e {numero2:.2f}")
        print(f"Resultado da {operacao.lower()}: {resultado:.2f}")
        print("-----------------------------------------\n")

    def Add(self, request, context):
        resultado = request.number1 + request.number2
        self.log_request("Adição", request.number1, request.number2, resultado)
        return calculator_pb2.OperationResponse(result=resultado)

    def Subtract(self, request, context):
        resultado = request.number1 - request.number2
        self.log_request("Subtração", request.number1, request.number2, resultado)
        return calculator_pb2.OperationResponse(result=resultado)

    def Multiply(self, request, context):
        resultado = request.number1 * request.number2
        self.log_request("Multiplicação", request.number1, request.number2, resultado)
        return calculator_pb2.OperationResponse(result=resultado)

    def Divide(self, request, context):
        if request.number2 == 0:
            resultado = float('inf')  # Representando divisão por zero como infinito
            self.log_request("Divisão por Zero", request.number1, request.number2, resultado)
        else:
            resultado = request.number1 / request.number2
            self.log_request("Divisão", request.number1, request.number2, resultado)
        return calculator_pb2.OperationResponse(result=resultado)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor em execução na porta 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
