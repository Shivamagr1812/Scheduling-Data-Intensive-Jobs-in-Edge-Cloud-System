def schedule_chunks(C, d, N):
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
            NTS_rd = 0
            current_VM = 0
            for i in range(S):
                if len(nodes[N-1].chunks_scheduled[i])!=0 and NTS_rd < (d - (nodes[N-1].chunks_scheduled[i][-1][1]+nodes[N-1].chunks_scheduled[i][-1][0].slots_required)):
                    NTS_rd = (d -(nodes[N-1].chunks_scheduled[i][-1][1]+nodes[N-1].chunks_scheduled[i][-1][0].slots_required))
                    current_VM = i
                elif len(nodes[N-1].chunks_scheduled[i])==0:
                    NTS_rd = d
                    current_VM = i
                    break
            if len(nodes[N-1].chunks_scheduled[current_VM])==0:    
                t_start = 0
            else:
                t_start = nodes[N-1].chunks_scheduled[current_VM][-1][2] 
            t_end = t_start + remaining_time_slots
            flag = False
            for i in range(S):
                # Check if the ith VM has a chunk of chunk_id scheduled between t_start and t_end
                for chunk in nodes[N-1].chunks_scheduled[i]:
                    if(chunk[0].id == chunk_id) and t_start <= chunk[1] < t_end:
                        flag = True
                    if flag:
                        break
                if flag:
                        break
            if flag:
                continue
            
            # print("Chunk id: ", chunk_id, "NTS_rd: ", NTS_rd, "remaining_time_slots: ", remaining_time_slots, "t_start: ", t_start, "t_end: ", t_end, "current_VM: ", current_VM)
            # Check if remaining time slots of the chunk is greater than 0
            if remaining_time_slots - NTS_rd > 0:
                # Update remaining time slots and NTS_rd
                remaining_time_slots -= NTS_rd
                t_end = t_start + NTS_rd
                C[chunk_index].slots_required = remaining_time_slots  # Update the remaining time slots in the original list
            else:
                t_end = t_start + remaining_time_slots
                C[chunk_index].slots_required = 0
                C[chunk_index].finished = True  # Set remaining time slots to 0 and mark chunk as finished
            nodes[N-1].chunks_scheduled[current_VM].append((C[chunk_index], t_start, t_end))    
            print("Chunk id: ", chunk_id, "scheduled at time: ", t_start, " on VM: ", current_VM, " on node: ", N-1)
            

    # Return a new list C that contains only the chunks that have not been finished yet
    return [chunk for chunk in C if not chunk.finished]

def schedule_chunks_modified(node, ind, d, N):
    C = []
    # print("deadlines_i", deadlines[ind].chunks_required)
    deadlines_i = deadlines[ind]
    # use node and deadlines_i to create a list C that contains objects in C whose chunk id exists in the node list
    
    for i in range(S):
        for chunk in node.chunks_scheduled[i]:
            for chunk_id in deadlines_i.chunks_required:
                if chunk[0].id == chunk_id.id:
                    C.append(chunk_id)
                    break
    # Sort C based on the remaining number of required time slots for d in ascending order
    C.sort(key=lambda x: x.slots_required)  # Assuming each chunk in C is represented as (chunk_id, remaining_time_slots, finished)
    # print("node: ", node.id)
    # print("deadline: ", d)
    for chunk_index in range(len(C)):
        # print(C)
        chunk_id = C[chunk_index].id
        remaining_time_slots = C[chunk_index].slots_required
        finished = C[chunk_index].finished

        # Check if the chunk has not been finished yet
        # print("Chunk id: ", chunk_id, "remaining_time_slots: ", remaining_time_slots)
        if not finished:
            NTS_rd = 0
            current_VM = 0
            for i in range(S):
                if len(nodes[N-1].chunks_scheduled[i])!=0 and NTS_rd < (d - (nodes[N-1].chunks_scheduled[i][-1][1]+nodes[N-1].chunks_scheduled[i][-1][0].slots_required)):
                    NTS_rd = (d -(nodes[N-1].chunks_scheduled[i][-1][1]+nodes[N-1].chunks_scheduled[i][-1][0].slots_required))
                    current_VM = i
                elif len(nodes[N-1].chunks_scheduled[i])==0:
                    NTS_rd = d
                    current_VM = i
                    break
            if len(nodes[N-1].chunks_scheduled[current_VM])==0:    
                t_start = 0
            else:
                t_start = nodes[N-1].chunks_scheduled[current_VM][-1][2] 
            t_end = t_start + remaining_time_slots
            flag = False
            for i in range(S):
                # Check if the ith VM has a chunk of chunk_id scheduled between t_start and t_end
                for chunk in nodes[N-1].chunks_scheduled[i]:
                    if(chunk[0].id == chunk_id) and t_start <= chunk[1] < t_end:
                        flag = True
                    if flag:
                        break
                if flag:
                        break
            if flag:
                continue
            
            # Check if remaining time slots of the chunk is greater than 0
            if remaining_time_slots - NTS_rd > 0:
                # Update remaining time slots and NTS_rd
                remaining_time_slots -= NTS_rd
                t_end = t_start + NTS_rd
                C[chunk_index].slots_required = remaining_time_slots  # Update the remaining time slots in the original list
            else:
                t_end = t_start + remaining_time_slots
                C[chunk_index].slots_required = 0
                C[chunk_index].finished = True  # Set remaining time slots to 0 and mark chunk as finished
            nodes[N-1].chunks_scheduled[current_VM].append((C[chunk_index], t_start, t_end))    
            print("Chunk id: ", chunk_id, "scheduled at time: ", t_start, " on VM: ", current_VM, " on node: ", N-1)

    
    # Remove finished chunks from the deadlines_i list
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
    # print("deadlines_i", deadlines[ind].chunks_required)
    return C

def CRED_S(F, B, d_i, N):
    # Implementation of CRED-S function
    C_r=F
    while len(C_r)>0:
        # print("length of C_r: ", len(C_r))
        # sort the chunks based on the number of slots required
        # print(type(C_r[0]))
        C_r.sort(key=lambda x: x.slots_required)
        
        # total_F = sum(C_r[i].slots_required for i in range(1, min(B,len(C_r))))

        H_B=[]
        for i in range(min(B,len(C_r))):
            H_B.append(C_r[i])
        # Remove the chunks from the list
        for chunk in H_B:
            C_r.remove(chunk)

        C= schedule_chunks(H_B, d_i, N)
        # print("Value of C: ")
        # for i in C:
        #     print(i.id)
        if len(C)>0:
            C_r.extend(C)
        N+=1
    # while len(C_r)>0:
    #     print("length of C_r: ", len(C_r))
    #     H_B=[]
    #     for i in range(min(B,len(C_r))):
    #         H_B.append(C_r[i])
    #         # print(C_r[i])
        
    #     # Remove the chunks from the list
    #     for chunk in H_B:
    #         C_r.remove(chunk)
    #         # print("Chunk removed ", chunk.id)

    #     C= schedule_chunks(H_B,d_i,N)
    #     if len(C)>0:
    #         C_r.extend(C)
    #     N+=1
    return N

def CRED_M(nodes, chunks, deadlines, B, jobs, S): 
    D = len(deadlines)
    num_active_nodes = 1
    
    for i in range(D):
        chunks_i = deadlines[i].chunks_required
        # print("Deadline: ", deadlines[i].deadline)
        # for chunk in chunks_i:
        #     print(chunk.id, chunk.slots_required)
        num_active_nodes = CRED_S(chunks_i, B, jobs[i].deadline, num_active_nodes)
        for n in range(num_active_nodes-1):
            for j in range(i+1, D):
                # print("Deadline: ", deadlines[j].deadline, "Node: ", n)
                schedule_chunks_modified(nodes[n],j,deadlines[j].deadline, n+1)
    
    return num_active_nodes-1


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
Nodes = 10  # Number of nodes
B = 4  # Maximum number of data chunks each node can host
S = 2  # Number of VMs (virtual machines) on each node

jobs = [
    Job(2, [1, 2, 3]),
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
    if job.deadline not in deadlines:
        # print(job.deadline, job.chunks_required)
        chunks_required = []
        for chunk_id in job.chunks_required:
            
            chunk = Chunk(chunk_id)
            chunk.slots_required = 1

            chunks_required.append(chunk)
            chunks.append(chunk)
        deadline = Deadline(job.deadline, chunks_required)
        deadlines.append(deadline)
        
    else:
        for deadline in deadlines:
            if deadline.deadline == job.deadline:
                # print(job.deadline, job.chunks_required)
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

                    chunks_required.append(chunk)
                    chunks.append(chunk)
                deadline.chunks_required.extend(chunks_required)    

# for deadline in deadlines:
#     print("Deadline: ", deadline.deadline)
#     for chunk in deadline.chunks_required:
#         print(chunk.id, chunk.slots_required)

# sort the deadlines based on the deadline value
deadlines.sort(key=lambda x: x.deadline)

class Node:
    def __init__(self, id, S):
        self.id = id
        self.chunks_scheduled = [[] for _ in range(S)]

nodes = []
for n in range(Nodes):
    node = Node(n, S)
    nodes.append(node)

num_active_nodes = CRED_M(nodes, chunks, deadlines, B, jobs, S)
print("-----------------------------------------------------------------------------")
print(f"\nNumber of active nodes: {num_active_nodes}")

# print the chunks scheduled on each node
for node in nodes:
    if node.id < num_active_nodes:
        print(f"\nChunks scheduled on node {node.id}: \n")
        for i in range(S):
            print("VM", i )
            for chunk in node.chunks_scheduled[i]:
                print("Chunk scheduled: ", chunk[0].id, " at time: ", chunk[1])