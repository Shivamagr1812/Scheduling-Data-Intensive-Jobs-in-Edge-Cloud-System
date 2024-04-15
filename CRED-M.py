def CRED_M(nodes, chunks, deadlines, B, jobs, S): 
    D = len(deadlines)
    num_active_nodes = 0
    
    for i in range(D):
        num_active_i = CRED_S(deadlines[i], chunks, B, jobs[i].deadline)
        for n in range(num_active_i):
            for j in range(i+1, D):
                schedule_chunks(nodes[n].chunks_scheduled, S*d[j] - count_scheduled_slots(n))
        num_active_nodes += num_active_i
    
    return num_active_nodes

def CRED_S(Ci, F, B, d_i):
    # Implementation of CRED-S function
    N=0
    C_r=F
    while C_r >0:
        C_r.sort(key=lambda x:x[1])
        
        total_F = sum(F[i].slots_required for i in range(1, B))

        H_B=[]
        if total_F>S*d_i:
            for i in range(1,B):
                H_B.append(F[i])
            schedule_chunks(H_B,S*d_i)
            N+=1
        else:
            break
    while C_r>0:
        H_B=F
        schedule_chunks(H_B,S*d_i)
        N+=1
    return N

def schedule_chunks(C, NTS):
    # Implementation of chunk scheduling
    pass

def count_scheduled_slots(node):
    # Implementation of counting scheduled slots
    pass


# User Input
J = int(input("Enter the number of jobs: "))
N = int(input("Enter the number of nodes: "))
B = int(input("Enter the maximum number of data chunks each node can host: "))
S = int(input("Enter the number of VMs (virtual machines) on each node: "))

class Job:
    def __init__(self, deadline, chunks_required):
        self.deadline = deadline
        self.chunks_required = chunks_required

jobs = []
for j in range(J):
    deadline = int(input(f"Enter the deadline for job {j+1}: "))
    chunks_required = input(f"Enter the list of chunk ids required for job {j+1} (comma-separated): ").split(',')
    chunks_required = [int(chunk_id) for chunk_id in chunks_required]
    job = Job(deadline, chunks_required)
    jobs.append(job)

class Chunk:
    def __init__(self, id, slots_required):
        self.id = id
        self.slots_required = slots_required

chunks = []
for i in range(len(jobs)):
    for chunk_id in jobs[i].chunks_required:
        chunk_exists = False
        for chunk in chunks:
            if chunk.id == chunk_id:
                chunk_exists = True
                break
        
        if chunk_exists:
            chunk.slots_required[jobs[i].deadline] += 1

        slots_required = []
        slots_required[jobs[i].deadline] = 1
        chunk = Chunk(chunk_id, slots_required)
        chunks.append(chunk)

class Deadline:
    def __init__(self, deadline, chunks_required):
        self.deadline = deadline
        self.chunks_required = chunks_required

deadlines = []
for job in jobs:
    chunks_required = [chunk_id for chunk_id in job.chunks_required]
    
    if job.deadline not in deadlines:
        deadline = Deadline(job.deadline, chunks_required)
        deadlines.append(deadline)
    else:
        for deadline in deadlines:
            if deadline.deadline == job.deadline:
                deadline.chunks_required.append(chunks_required)    

class Node:
    def __init__(self, chunks_scheduled):
        self.chunks_scheduled = chunks_scheduled

nodes = []
for n in range(N):
    chunks_scheduled = []
    node = Node(chunks_scheduled)
    nodes.append(node)