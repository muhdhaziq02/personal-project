# client.py
import grpc
import requests
import time
import services_pb2
import services_pb2_grpc

# --- Server Addresses (using Docker service names) ---
GRPC_SERVER = 'grpc-server:50051'
REST_SERVER = 'http://rest-server:5000'
NUM_RUNS = 5

# --- Test Data (now global constants) ---
TEST_NUMBERS = [5, 1, 9, 3, 7]
TEST_TEXT = "hello world this is a test hello world"

# --- gRPC Client Functions ---
# (These just call the stub)
def call_grpc_process(stub):
    return stub.ProcessData(services_pb2.NumberList(numbers=TEST_NUMBERS))

def call_grpc_wordcount(stub):
    return stub.GetWordCount(services_pb2.Text(content=TEST_TEXT))

def call_grpc_minmax(stub):
    return stub.GetMinMax(services_pb2.NumberList(numbers=TEST_NUMBERS))

def call_grpc_sort(stub):
    return stub.GetSorted(services_pb2.NumberList(numbers=TEST_NUMBERS))

def call_grpc_primes(stub):
    return stub.GetPrimes(services_pb2.NumberList(numbers=TEST_NUMBERS))

# --- REST Client Functions ---
# (These call the endpoint and return the .json() result)
def call_rest_process():
    response = requests.post(f"{REST_SERVER}/process", json={"numbers": TEST_NUMBERS})
    return response.json()

def call_rest_wordcount():
    response = requests.post(f"{REST_SERVER}/wordcount", json={"content": TEST_TEXT})
    return response.json()

def call_rest_minmax():
    response = requests.post(f"{REST_SERVER}/minmax", json={"numbers": TEST_NUMBERS})
    return response.json()

def call_rest_sort():
    response = requests.post(f"{REST_SERVER}/sort", json={"numbers": TEST_NUMBERS})
    return response.json()

def call_rest_primes():
    response = requests.post(f"{REST_SERVER}/primes", json={"numbers": TEST_NUMBERS})
    return response.json()

# --- Helper function to run and time a function ---
def time_and_run(func, *args):
    times = []
    result = None
    for _ in range(NUM_RUNS):
        start = time.perf_counter()
        result = func(*args) # Call the function
        end = time.perf_counter()
        times.append(end - start)
    
    avg_time = (sum(times) / NUM_RUNS) * 1000 # in milliseconds
    return avg_time, result


def run_benchmarks():
    print("Waiting for servers to be ready...", flush=True)
    time.sleep(5) 

    grpc_results = {}
    rest_results = {}
    service_order = ['ProcessData', 'WordCount', 'MinMax', 'Sort', 'Primes']
    
    # --- Print Input Data ---
    print("\n" + "="*50, flush=True)
    print("--- Input Data ---", flush=True)
    print(f"Numbers: {TEST_NUMBERS}")
    print(f"Text:    '{TEST_TEXT}'")
    print("="*50 + "\n", flush=True)

    print("\n--- Running Program Processes ---", flush=True)

    # --- gRPC Processes ---
    print("\n--- gRPC Processes ---", flush=True)
    try:
        with grpc.insecure_channel(GRPC_SERVER) as channel:
            stub = services_pb2_grpc.ComparatorStub(channel)
            
            # 1. ProcessData
            avg_time, result = time_and_run(call_grpc_process, stub)
            grpc_results['ProcessData'] = avg_time
            print("1. MapReduce (Map: n*n, Reduce: sum)")
            print(f"   Input:   {TEST_NUMBERS}")
            print(f"   Process: {[n*n for n in TEST_NUMBERS]}")
            print(f"   Result:  {result.value}\n")

            # 2. WordCount
            avg_time, result = time_and_run(call_grpc_wordcount, stub)
            grpc_results['WordCount'] = avg_time
            print("2. WordCount")
            print(f"   Input:  '{TEST_TEXT}'")
            print(f"   Result: {dict(result.counts)}\n")

            # 3. MinMax
            avg_time, result = time_and_run(call_grpc_minmax, stub)
            grpc_results['MinMax'] = avg_time
            print("3. Min/Max")
            print(f"   Input:  {TEST_NUMBERS}")
            print(f"   Result: Min={result.min}, Max={result.max}\n")

            # 4. Sort
            avg_time, result = time_and_run(call_grpc_sort, stub)
            grpc_results['Sort'] = avg_time
            print("4. Sort")
            print(f"   Input:      {TEST_NUMBERS}")
            print(f"   Ascending:  {list(result.ascending)}")
            print(f"   Descending: {list(result.descending)}\n")

            # 5. Primes
            avg_time, result = time_and_run(call_grpc_primes, stub)
            grpc_results['Primes'] = avg_time
            print("5. Primes")
            print(f"   Input:  {TEST_NUMBERS}")
            print(f"   Result: {list(result.numbers)}\n")
            
    except Exception as e:
        print(f"gRPC Error: {e}", flush=True)

    # --- REST Processes ---
    print("\n--- REST Processes ---", flush=True)
    try:
        # 1. ProcessData
        avg_time, result_json = time_and_run(call_rest_process)
        rest_results['ProcessData'] = avg_time
        print("1. MapReduce (Map: n*n, Reduce: sum)")
        print(f"   Input:   {TEST_NUMBERS}")
        print(f"   Process: {[n*n for n in TEST_NUMBERS]}")
        print(f"   Result:  {result_json['value']}\n")

        # 2. WordCount
        avg_time, result_json = time_and_run(call_rest_wordcount)
        rest_results['WordCount'] = avg_time
        print("2. WordCount")
        print(f"   Input:  '{TEST_TEXT}'")
        print(f"   Result: {result_json['counts']}\n")

        # 3. MinMax
        avg_time, result_json = time_and_run(call_rest_minmax)
        rest_results['MinMax'] = avg_time
        print("3. Min/Max")
        print(f"   Input:  {TEST_NUMBERS}")
        print(f"   Result: Min={result_json['min']}, Max={result_json['max']}\n")

        # 4. Sort
        avg_time, result_json = time_and_run(call_rest_sort)
        rest_results['Sort'] = avg_time
        print("4. Sort")
        print(f"   Input:      {TEST_NUMBERS}")
        print(f"   Ascending:  {result_json['ascending']}")
        print(f"   Descending: {result_json['descending']}\n")

        # 5. Primes
        avg_time, result_json = time_and_run(call_rest_primes)
        rest_results['Primes'] = avg_time
        print("5. Primes")
        print(f"   Input:  {TEST_NUMBERS}")
        print(f"   Result: {result_json['numbers']}\n")
        
    except Exception as e:
        print(f"REST Error: {e}", flush=True)


    # --- Print Formatted Benchmark Table ---
    print("\n\n" + "="*50, flush=True)
    print("--- Running Benchmarks (Average of 5 runs) ---", flush=True)
    print("All times in milliseconds (ms)\n", flush=True)

    longest_name = max(len(s) for s in service_order)

    # Print gRPC Results
    print("--- gRPC ---", flush=True)
    for i, name in enumerate(service_order):
        time_val = grpc_results.get(name)
        if time_val is not None:
            print(f"{i+1}. {name:<{longest_name}}: {time_val:9.4f} ms", flush=True)
        else:
            print(f"{i+1}. {name:<{longest_name}}: FAILED", flush=True)

    # Print REST Results
    print("\n--- REST ---", flush=True)
    for i, name in enumerate(service_order):
        time_val = rest_results.get(name)
        if time_val is not None:
            print(f"{i+1}. {name:<{longest_name}}: {time_val:9.4f} ms", flush=True)
        else:
            print(f"{i+1}. {name:<{longest_name}}: FAILED", flush=True)
    
    print("\n" + "="*50, flush=True)
    print("Benchmark complete.", flush=True)


if __name__ == '__main__':
    run_benchmarks()