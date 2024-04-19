# Description: Python code to implement the Chunk Relocation and Elasticity-Division (CRED) algorithm for scheduling chunks on VMs within nodes

# Class definitions for Job, Chunk, Deadline, and Node
class Job:
    def __init__(self, deadline, chunks_required):
        self.deadline = deadline
        self.chunks_required = chunks_required

class Chunk:
    def __init__(self, id):
        self.id = id
        self.slots_required = 0
        self.finished = False

class Deadline:
    def __init__(self, deadline, chunks_required):
        self.deadline = deadline
        self.chunks_required = chunks_required

class Node:
    def __init__(self, id, S):
        self.id = id
        self.chunks_scheduled = [[] for _ in range(S)]  # Initialize list of lists for scheduling chunks on VMs


# Function to schedule chunks on available VMs within a node
def schedule_chunks(C, d, N, nodes, S):
    C.sort(key=lambda x: x.slots_required)  # Sort chunks based on their slots required

    for chunk_index in range(len(C)):
        chunk_id = C[chunk_index].id
        remaining_time_slots = C[chunk_index].slots_required
        finished = C[chunk_index].finished

        if not finished:
            NTS_rd = 0
            current_VM = 0
            # Find the VM with the maximum available time slots for scheduling the chunk
            for i in range(S):
                if len(nodes[N-1].chunks_scheduled[i]) != 0 and NTS_rd < (d - (nodes[N-1].chunks_scheduled[i][-1][1]+nodes[N-1].chunks_scheduled[i][-1][0].slots_required)):
                    NTS_rd = (d -(nodes[N-1].chunks_scheduled[i][-1][1]+nodes[N-1].chunks_scheduled[i][-1][0].slots_required))
                    current_VM = i
                elif len(nodes[N-1].chunks_scheduled[i]) == 0:
                    NTS_rd = d
                    current_VM = i
                    break
            if len(nodes[N-1].chunks_scheduled[current_VM]) == 0:    
                t_start = 0
            else:
                t_start = nodes[N-1].chunks_scheduled[current_VM][-1][2] 
            t_end = t_start + remaining_time_slots
            flag = False
            # Check if there is a scheduling conflict with existing chunks on the selected VM
            for i in range(S):
                for chunk in nodes[N-1].chunks_scheduled[i]:
                    if(chunk[0].id == chunk_id) and t_start <= chunk[1] < t_end:
                        flag = True
                    if flag:
                        break
                if flag:
                        break
            if flag:
                continue

            if remaining_time_slots - NTS_rd > 0:
                remaining_time_slots -= NTS_rd
                t_end = t_start + NTS_rd
                C[chunk_index].slots_required = remaining_time_slots
            else:
                t_end = t_start + remaining_time_slots
                C[chunk_index].slots_required = 0
                C[chunk_index].finished = True
            nodes[N-1].chunks_scheduled[current_VM].append((C[chunk_index], t_start, t_end))  # Schedule the chunk on the selected VM
            print("Chunk id: ", chunk_id, "scheduled at time: ", t_start, " on VM: ", current_VM, " on node: ", N-1)

    return [chunk for chunk in C if not chunk.finished]  # Return unscheduled chunks


# Function to schedule chunks with modifications for a specific node and deadline
def schedule_chunks_modified(node, ind, d, N, nodes, S):
    C = []
    deadlines_i = deadlines[ind]
    
    # Extract chunks scheduled on the node for the specific deadline
    for i in range(S):
        for chunk in node.chunks_scheduled[i]:
            for chunk_id in deadlines_i.chunks_required:
                if chunk[0].id == chunk_id.id:
                    C.append(chunk_id)
                    break
    C.sort(key=lambda x: x.slots_required)  # Sort chunks based on their slots required
    
    for chunk_index in range(len(C)):
        chunk_id = C[chunk_index].id
        remaining_time_slots = C[chunk_index].slots_required
        finished = C[chunk_index].finished

        if not finished:
            NTS_rd = 0
            current_VM = 0
            # Find the VM with the maximum available time slots for scheduling the chunk
            for i in range(S):
                if len(nodes[N-1].chunks_scheduled[i]) != 0 and NTS_rd < (d - (nodes[N-1].chunks_scheduled[i][-1][1]+nodes[N-1].chunks_scheduled[i][-1][0].slots_required)):
                    NTS_rd = (d -(nodes[N-1].chunks_scheduled[i][-1][1]+nodes[N-1].chunks_scheduled[i][-1][0].slots_required))
                    current_VM = i
                elif len(nodes[N-1].chunks_scheduled[i]) == 0:
                    NTS_rd = d
                    current_VM = i
                    break
            if len(nodes[N-1].chunks_scheduled[current_VM]) == 0:    
                t_start = 0
            else:
                t_start = nodes[N-1].chunks_scheduled[current_VM][-1][2] 
            t_end = t_start + remaining_time_slots
            flag = False
            # Check if there is a scheduling conflict with existing chunks on the selected VM
            for i in range(S):
                for chunk in nodes[N-1].chunks_scheduled[i]:
                    if(chunk[0].id == chunk_id) and t_start <= chunk[1] < t_end:
                        flag = True
                    if flag:
                        break
                if flag:
                        break
            if flag:
                continue
            
            if remaining_time_slots - NTS_rd > 0:
                remaining_time_slots -= NTS_rd
                t_end = t_start + NTS_rd
                C[chunk_index].slots_required = remaining_time_slots
            else:
                t_end = t_start + remaining_time_slots
                C[chunk_index].slots_required = 0
                C[chunk_index].finished = True
            nodes[N-1].chunks_scheduled[current_VM].append((C[chunk_index], t_start, t_end))  # Schedule the chunk on the selected VM
            print("Chunk id: ", chunk_id, "scheduled at time: ", t_start, " on VM: ", current_VM, " on node: ", N-1)

    for chunk in C:
        if chunk.finished:
            for j in deadlines_i.chunks_required:
                if j.id == chunk.id:
                    deadlines_i.chunks_required.remove(j)
        else:
            for j in deadlines_i.chunks_required:
                if j.id == chunk.id:
                    j.slots_required = chunk.slots_required
    deadlines[ind].chunks_required = deadlines_i.chunks_required
    return C


# Function to execute the CRED algorithm for a single deadline
def CRED_S(F, B, d_i, N, nodes, S):
    C_r = F[:]  # Copy of chunks to schedule
    while len(C_r) > 0:
        C_r.sort(key=lambda x: x.slots_required)  # Sort chunks based on their slots required
        
        H_B = []
        for i in range(min(B, len(C_r))):
            H_B.append(C_r[i])  # Extract B number of chunks from the sorted list
        
        for chunk in H_B:
            C_r.remove(chunk)  # Remove chunks from the list after extraction

        C = schedule_chunks(H_B, d_i, N, nodes, S)  # Schedule extracted chunks
        
        if len(C) > 0:
            C_r.extend(C)  # Add unscheduled chunks back to the list
        N += 1  # Increment node index

    return N


# Function to execute the CRED algorithm for multiple deadlines
def CRED_M(nodes, chunks, deadlines, B, jobs, S): 
    D = len(deadlines)
    num_active_nodes = 1
    
    for i in range(D):
        chunks_i = deadlines[i].chunks_required
        num_active_nodes = CRED_S(chunks_i, B, jobs[i].deadline, num_active_nodes, nodes, S)  # Execute sequential CRED algorithm
        for n in range(num_active_nodes-1):
            for j in range(i+1, D):
                schedule_chunks_modified(nodes[n], j, deadlines[j].deadline, n+1, nodes, S)  # Schedule chunks with modifications
    
    return num_active_nodes-1


# Function to read input from a file
def read_input(file_name):
    test_cases = []
    with open(file_name, 'r') as file:
        lines = file.readlines()

    num_test_cases = int(lines[0])
    i = 1
    for _ in range(num_test_cases):
        J, Nodes, B, S = map(int, lines[i].split())  # Read parameters for each test case
        i += 1
        
        jobs = []
        for _ in range(J):
            parts = lines[i].split()
            deadline = int(parts[0])
            num_chunks_required = int(parts[1])
            chunks_required = [int(chunk_id) for chunk_id in parts[2:]]
            job = Job(deadline, chunks_required)
            jobs.append(job)
            i += 1
        
        test_cases.append((J, Nodes, B, S, jobs))

    return test_cases


# Function to print output to a file
def print_output(num_active_nodes, nodes, S, out_file):
    out_file.write(f"\nNumber of active nodes: {num_active_nodes}\n")

    for node in nodes:
        if node.id < num_active_nodes:
            out_file.write(f"\nChunks scheduled on node {node.id}:\n")
            for i in range(S):
                if len(node.chunks_scheduled[i]) > 0:
                    out_file.write(f"\tVM {i}:\n")
                    for chunk in node.chunks_scheduled[i]:
                        out_file.write(f"\t\tChunk scheduled: {chunk[0].id} at time: {chunk[1]}\n")


# Main function to execute the code
if __name__ == "__main__":
    input_file = "test_case.txt"
    output_file = "output.txt"

    test_cases = read_input(input_file)  # Read test cases from input file

    with open(output_file, 'w') as out_file:
        for idx, test_case in enumerate(test_cases, start=1):
            J, Nodes, B, S, jobs = test_case

            # Initialize chunks and deadlines
            chunks = []
            deadlines = []

            # Extract chunks and deadlines from jobs
            for job in jobs:
                deadline_exists = False
                for deadline in deadlines:
                    if deadline.deadline == job.deadline:
                        deadline_exists = True
                        break
                
                if not deadline_exists:
                    chunks_required = []
                    for chunk_id in job.chunks_required:
                        chunk_exists = False
                        for chunk in chunks_required:
                            if chunk.id == chunk_id:
                                chunk_exists = True
                                break
                        
                        if chunk_exists:
                            chunk.slots_required += 1
                        else:
                            chunk = Chunk(chunk_id)
                            chunk.slots_required = 1
                            chunks_required.append(chunk)

                    deadline = Deadline(job.deadline, chunks_required)
                    deadlines.append(deadline)
                    
                else:
                    for deadline in deadlines:
                        if deadline.deadline == job.deadline:
                            chunks_required = []
                            for chunk_id in job.chunks_required:
                                chunk_exists = False
                                for chunk in deadline.chunks_required:
                                    if chunk.id == chunk_id:
                                        chunk_exists = True
                                        break
                                
                                if chunk_exists:
                                    chunk.slots_required += 1
                                else:
                                    chunk = Chunk(chunk_id)
                                    chunk.slots_required = 1
                                    deadline.chunks_required.append(chunk)  

                            break

            deadlines.sort(key=lambda x: x.deadline)  # Sort deadlines

            nodes = [Node(n, S) for n in range(Nodes)]  # Initialize nodes

            num_active_nodes = CRED_M(nodes, chunks, deadlines, B, jobs, S)  # Execute CRED algorithm

            out_file.write(f"Test Case {idx}:\n")
            print_output(num_active_nodes, nodes, S, out_file)  # Print output for each test case
            out_file.write("\n")
