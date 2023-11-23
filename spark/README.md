# What
Spark is a unified library for large-scale distributed data processing.

## Why is it special?
It is a unified library that supports batch processing, stream processing, machine learning, graph algorithms, 
SQL, etc...

Transformations occur in-memory, making it faster than MapReduce.


## High-Level Architecture

### Cluster
![spark physical architecture.svg](spark%20physical%20architecture.svg)

**Driver:** This is the leader node. It is the entrypoint to the rest of the spark system, and also assigns tasks to Executors

**Cluster manager:** It allocates resources to the worker nodes. The types of managers are standalone, Mesos, Yarn, K8s

**Worker Node:** Physical or Virtual machine in the cluster. 
It's primary role is to provide the environment and resource(CPU, memory, storage) for executors to run.

**Executor:** JVM process launched for spark application. It's primary role is to execute tasks from the Driver.

**Slots:** Fancy name for cores on the executor. Typically 1 slot<--->1 task<--->1 partition. 
So If I have 4 executors with 4 slots, I can run 16 tasks in parallel

#### Executor memory Breakdown
![Executor-memory-breakdown.svg](Executor-memory-breakdown.svg)

Executor memory stores temporary data used for shuffles, joins, sorts, aggregations. If data exceeds memory, it will spill onto disk.

Storage memory is used for cached data, broadcasts.

Reserved memory is used to prevent OOM issues.

### Logical

![img.png](dag_to_job_stage_task.png)

![img_1.png](Job_Stage_Task.png)

**Transformation:** Operations like filter, select, join, groupBy.
* Narrow Transformations: Transformations that each input partition contributes to only one output partition. Generally more efficient and faster.
* Wide Transformations: Transformations where input data from multiple partitions may be combined to produce each output partition. This means they require
a shuffle, which involves disk I/O, network I/O, and serialization/deserialization of the data.

**Action:** Operations like save, show, and count. Once an action is invoked, Spark will take transformations to create an optimized 
Directed Acyclic Graph (DAG). This DAG is then divided into multiple Jobs, Stages, and Tasks. 
The code is executed accordingly, with the result either being returned to the Driver or written to disk.

**Logical Plan:** Each transformation builds upon a logical plan, a tree of logical operations and high level abstraction
of what the user wants to do. After the plan is constructed the catalyst optimizer creates logical optimized plan

**Physical Plan:** How the optimized logical plan will be executed in the cluster. It is represented as a DAG. 
The driver will break it down into one or more jobs. 

**Job:** Represents the entire computation required to produce results for an action. A job consists of 1 or more stages.

**Stage:** Each stage contains a sequence of transformations that can be completed without shuffling, shuffles mark the boundary of 
an individual stage. A stage has multiple tasks that can be executed in parallel

**Task:** A unit of work that will be performed by the executor and corresponds to 1 slot and 1 partition.


## Performance bottlnecks

I/O caused by:

Shuffle, Skew, Spill

TODO: Write more about this
