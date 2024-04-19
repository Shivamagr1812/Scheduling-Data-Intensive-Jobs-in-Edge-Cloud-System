# Cloud Scheduling Algorithm

This Python script implements a cloud scheduling algorithm for distributing and processing jobs across a set of physical machines in a cloud environment. The algorithm aims to minimize the total number of active nodes while ensuring that all jobs are completed before their respective deadlines.

## Problem Description

Consider a set of J jobs that need to be processed by a cloud consisting of N physical machines (nodes). Each job has a deadline and requires access to a set of equal-sized data chunks stored in a distributed file system on the cloud. Each node is equipped with a certain number of virtual machines (VMs) and can host up to a maximum number of data chunks. The goal is to schedule the jobs on the nodes in such a way that the total number of active nodes is minimized while meeting all job deadlines.

## Implementation

The algorithm consists of the following components:

1. `schedule_chunks`: This function schedules data chunks on the available VMs of the nodes based on the remaining time slots and deadlines of the jobs.

2. `schedule_chunks_modified`: This function is a modified version of `schedule_chunks` used for scheduling chunks after the initial scheduling phase.

3. `CRED_S`: This function implements the CRED-S (Chunk REplication and Deadline-Sensitive) algorithm, which schedules chunks on the nodes to minimize the total number of active nodes.

4. `CRED_M`: This function orchestrates the scheduling process by iteratively applying the CRED-S algorithm and updating the scheduling information.

5. `Job`, `Chunk`, `Deadline`, and `Node` classes: These classes represent the entities involved in the scheduling process.

## Usage

1. Define the jobs, nodes, and other parameters such as the maximum number of data chunks per node and the number of VMs per node.

2. Instantiate the `Job`, `Chunk`, `Deadline`, and `Node` objects based on the defined parameters.

3. Call the `CRED_M` function with the appropriate arguments to perform the scheduling.

4. The function will return the total number of active nodes and the scheduling information for each active node.

## How to Run

You need to have Python installed on your system to run this script. You can run the script using the following command:

```
python CRED.py
```

## Input Format

`<J>` `<Nodes>` `<B>` `<S>`\
`<deadline_1>` `<num_chunks_required_1>` `<chunk_id_1>` `<chunk_id_2>` ... `<chunk_id_n>`\
`<deadline_2>` `<num_chunks_required_2>` `<chunk_id_1>` `<chunk_id_2>` ... `<chunk_id_m>`\
...\
`<deadline_J>` `<num_chunks_required_J>` `<chunk_id_1>` `<chunk_id_2>` ... `<chunk_id_p>`

## Output Format

Number of active nodes: `<num_active_nodes>`

Chunks scheduled on each active node:\
Node `<node_id>`:\
&emsp;    VM `<vm_id>`:\
&emsp;&emsp;        Chunk scheduled: `<chunk_id>` at time: <start_time>\
&emsp;&emsp;        Chunk scheduled: `<chunk_id>` at time: <start_time>\
&emsp;&emsp;        ...\
&emsp;    VM `<vm_id>`:\
&emsp;&emsp;        Chunk scheduled: `<chunk_id>` at time: <start_time>\
&emsp;&emsp;        Chunk scheduled: `<chunk_id>` at time: <start_time>\
&emsp;&emsp;        ...\
...

## Example

Input:

3 15 2 1\
4 6 1 1 1 1 1 1\
4 3 2 3 4\
4 3 5 5 5

Output:

Number of active nodes: 2

Chunks scheduled on each active node:\
Node 0:\
&emsp;    VM 0:\
&emsp;&emsp;        Chunk scheduled: 1 at time: 0\
&emsp;&emsp;        Chunk scheduled: 1 at time: 1\
&emsp;&emsp;        Chunk scheduled: 1 at time: 2\
Node 1:\
&emsp;    VM 0:\
&emsp;&emsp;        Chunk scheduled: 5 at time: 0\
&emsp;&emsp;        Chunk scheduled: 5 at time: 1\
&emsp;&emsp;        Chunk scheduled: 5 at time: 2
