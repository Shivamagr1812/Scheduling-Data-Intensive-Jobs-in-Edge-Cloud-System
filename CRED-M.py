def schedule_chunks(C, NTS_rd):
    # Sort C based on the remaining number of required time slots for d in ascending order
    # print(C)
    C.sort(key=lambda x: x.slots_required)  # Assuming each chunk in C is represented as (chunk_id, remaining_time_slots, finished)

    for chunk_index in range(len(C)):
        # print(C)
        chunk_id = C[chunk_index].id
        remaining_time_slots = C[chunk_index].slots_required
        finished = C[chunk_index].finished

        # Check if the chunk has not been finished yet
        if not finished:
            # Check if remaining time slots of the chunk is greater than 0
            if remaining_time_slots - NTS_rd > 0:
                # Update remaining time slots and NTS_rd
                remaining_time_slots -= NTS_rd
                NTS_rd = 0
                C[chunk_index].slots_required = remaining_time_slots  # Update the remaining time slots in the original list
                break
            else:
                # Update NTS_rd and set remaining time slots to 0
                NTS_rd -= remaining_time_slots
                C[chunk_index].slots_required = 0
                C[chunk_index].finished = True  # Set remaining time slots to 0 and mark chunk as finished
    
    # Remove finished chunks from the list
    for chunk in C:
        if chunk.finished:
            C.remove(chunk)

    return C, NTS_rd

def schedule_chunks_modified(node, deadlines_i, NTS_rd):
    C = []
    # use node and deadlines_i to create a list C that contains objects in C whose chunk id exists in the node list
    for chunk in node.chunks_scheduled:
        if chunk in deadlines_i:
            C.append(chunk)

    # Sort C based on the remaining number of required time slots for d in ascending order
    C.sort(key=lambda x: x.slots_required)  # Assuming each chunk in C is represented as (chunk_id, remaining_time_slots, finished)

    for chunk_index in range(len(C)):
        # print(C)
        chunk_id = C[chunk_index].id
        remaining_time_slots = C[chunk_index].slots_required
        finished = C[chunk_index].finished

        # Check if the chunk has not been finished yet
        if not finished:
            # Check if remaining time slots of the chunk is greater than 0
            if remaining_time_slots - NTS_rd > 0:
                # Update remaining time slots and NTS_rd
                remaining_time_slots -= NTS_rd
                NTS_rd = 0
                C[chunk_index].slots_required = remaining_time_slots  # Update the remaining time slots in the original list
                break
            else:
                # Update NTS_rd and set remaining time slots to 0
                NTS_rd -= remaining_time_slots
                C[chunk_index].slots_required = 0
                C[chunk_index].finished = True  # Set remaining time slots to 0 and mark chunk as finished
    
    # Remove finished chunks from the deadlines_i list
    for chunk in C:
        if chunk.finished:
            deadlines_i.remove(chunk)

    return C, NTS_rd

def CRED_S(F, B, d_i):
    # Implementation of CRED-S function
    N=0
    C_r=F
    while len(C_r)>0:
        # sort the chunks based on the number of slots required
        # print(type(C_r[0]))
        C_r.sort(key=lambda x: x.slots_required)
        
        total_F = sum(C_r[i].slots_required for i in range(1, min(B,len(C_r))))

        H_B=[]
        if total_F>S*d_i:
            for i in range(1, min(B,len(C_r))):
                H_B.append(C_r[i])
            # Remove the chunks from the list
            C_r = [chunk for chunk in C_r if chunk not in H_B]

            nodes[N].chunks_scheduled.extend(H_B)
            C, NTS_rd = schedule_chunks(H_B, S*d_i - len(nodes[n].chunks_scheduled))
            # print("Value of C: ", C)
            C_r.extend(C)
            if NTS_rd == 0:
                N+=1
        else:
            break
    while len(C_r)>0:
        H_B=[]
        for i in range(1, min(B,len(C_r))):
            H_B.append(C_r[i])
            # print(C_r[i])
        C_r = [chunk for chunk in C_r if chunk not in H_B]

        nodes[N].chunks_scheduled.extend(H_B)
        # print("Value of H_B: ", H_B)
        C, NTS_rd = schedule_chunks(H_B,S*d_i - len(nodes[n].chunks_scheduled))
        C_r.extend(C)
        # print("C_r: ", C_r)
        if NTS_rd == 0:
            N+=1
    return N

def CRED_M(nodes, chunks, deadlines, B, jobs, S): 
    D = len(deadlines)
    num_active_nodes = 0
    
    for i in range(D):
        chunks_i = deadlines[i].chunks_required
        num_active_i = CRED_S(chunks_i, B, jobs[i].deadline)
        for n in range(num_active_i):
            for j in range(i+1, D):
                schedule_chunks_modified(nodes[n], deadlines[i], S*d[j] - len(nodes[n].chunks_scheduled))
        num_active_nodes += num_active_i
    
    return num_active_nodes


# User Input
# J = int(input("Enter the number of jobs: "))
# N = int(input("Enter the number of nodes: "))
# B = int(input("Enter the maximum number of data chunks each node can host: "))
# S = int(input("Enter the number of VMs (virtual machines) on each node: "))

class Job:
    def __init__(self, deadline, chunks_required):
        self.deadline = deadline
        self.chunks_required = chunks_required

# jobs = []
# for j in range(J):
#     deadline = int(input(f"Enter the deadline for job {j+1}: "))
#     chunks_required = input(f"Enter the list of chunk ids required for job {j+1} (comma-separated): ").split(',')
#     chunks_required = [int(chunk_id) for chunk_id in chunks_required]
#     job = Job(deadline, chunks_required)
#     jobs.append(job)

J = 3  # Number of jobs
N = 2  # Number of nodes
B = 4  # Maximum number of data chunks each node can host
S = 2  # Number of VMs (virtual machines) on each node

jobs = [
    Job(5, [1, 2, 3]),
    Job(4, [2, 3, 4]),
    Job(3, [3, 4, 5])
]

class Chunk:
    def __init__(self, id):
        self.id = id
        self.slots_required = 0
        self.finished = False

class Deadline:
    def __init__(self, deadline, chunks_required):
        self.deadline = deadline
        self.chunks_required = chunks_required

chunks = []
deadlines = []
for job in jobs:
    # print(job.deadline, job.chunks_required)
    chunks_required = []
    for chunk_id in job.chunks_required:
        chunk_exists = False
        for chunk in chunks:
            if chunk.id == chunk_id:
                chunk_exists = True
                break
        
        if chunk_exists:
            chunk.slots_required += 1
        else:
            chunk = Chunk(chunk_id)
            chunk.slots_required = 1

        chunks_required.append(chunk)
        chunks.append(chunk)
    
    if job.deadline not in deadlines:
        deadline = Deadline(job.deadline, chunks_required)
        deadlines.append(deadline)
    else:
        for deadline in deadlines:
            if deadline.deadline == job.deadline:
                deadline.chunks_required.extend(chunks_required)    


class Node:
    def __init__(self, chunks_scheduled):
        self.chunks_scheduled = chunks_scheduled

nodes = []
for n in range(N):
    chunks_scheduled = []
    node = Node(chunks_scheduled)
    nodes.append(node)

num_active_nodes = CRED_M(nodes, chunks, deadlines, B, jobs, S)
print(f"Number of active nodes: {num_active_nodes}")