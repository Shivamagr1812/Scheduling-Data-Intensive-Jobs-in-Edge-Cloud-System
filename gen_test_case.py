import random

def generate_test_case():
    J = random.randint(1, 5)  # Number of jobs
    Nodes = 20 # Number of nodes
    B = random.randint(1, 5)  # Bandwidth constraint
    S = random.randint(1, 3)  # Number of virtual machines per node

    test_case = f"{J} {Nodes} {B} {S}\n"

    for _ in range(J):
        deadline = random.randint(1, 10)
        num_chunks = random.randint(1, 3)
        chunks_required = random.sample(range(1, 11), num_chunks)  # Assuming chunk IDs from 1 to 10
        test_case += f"{deadline} {num_chunks} {' '.join(map(str, chunks_required))}\n"

    return test_case

def generate_test_case_to_file(file_name, n):
    with open(file_name, 'w') as file:
        file.write(str(n) + "\n")
        for _ in range(n):
            test_case = generate_test_case()
            file.write(test_case)

# Example: Generate a random test case and save it to a text file
generate_test_case_to_file("test_case.txt", 10)