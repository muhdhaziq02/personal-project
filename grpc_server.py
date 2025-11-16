# grpc_server.py
from concurrent import futures
import time
import grpc
import services_pb2
import services_pb2_grpc

# --- Helper Functions ---
def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

# --- Service Implementation ---
class ComparatorServicer(services_pb2_grpc.ComparatorServicer):

    def ProcessData(self, request, context):
        # 1. Map (square) and Reduce (sum)
        mapped = [n * n for n in request.numbers]
        reduced = sum(mapped)
        return services_pb2.Number(value=reduced)

    def GetWordCount(self, request, context):
        # 2. Word Count
        words = request.content.split()
        counts = {}
        for word in words:
            counts[word] = counts.get(word, 0) + 1
        return services_pb2.WordCountResponse(counts=counts)

    def GetMinMax(self, request, context):
        # 3. Find Min/Max
        return services_pb2.MinMaxResponse(min=min(request.numbers), max=max(request.numbers))

    def GetSorted(self, request, context):
        # 4. Sort Numbers
        asc = sorted(request.numbers)
        desc = sorted(request.numbers, reverse=True)
        return services_pb2.SortedResponse(ascending=asc, descending=desc)

    def GetPrimes(self, request, context):
        # 5. List Primes
        primes = [n for n in request.numbers if is_prime(n)]
        return services_pb2.NumberList(numbers=primes)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_ComparatorServicer_to_server(ComparatorServicer(), server)
    server.add_insecure_port('[::]:50051') # Port for gRPC
    print("Starting gRPC server on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()