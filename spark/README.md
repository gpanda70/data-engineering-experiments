# What
Spark is a unified library for large-scale distributed data processing.

## Why is it special?
It is a unified library that supports batch processing, stream processing, machine learning, graph algorithms, 
SQL, etc...

Transformations occur in-memory, making it faster than MapReduce.


## High-Level Architecture

### Physical
![spark physical architecture.svg](spark%20physical%20architecture.svg)

**Driver:** This is the leader node. You can think of it as the entrypoint to the rest of the spark system.

**Cluster manager:** Allocates resources to the executors.

**Executor:** These are the worker nodes that will perform the unit of work known as **tasks**, that are sent from the Driver.

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

**Transformation:** Operations like filter, select, join, groupBy. Can be split into narrow or wide(shuffle)

**Action:** Operations like save, show, count. This will actually start the execution. It will take the transformations
and create a Optimized DAG (Physical plan)

**Logical Plan:** Each transformation builds upon a logical plan, a tree of logical operations and high level abstraction
of what the user wants to do. After the plan is constructed the catalyst optimizer creates logical optimization

**Physical Plan:** How the logical plan will be executed in the cluster. Represented as a DAG. Driver will break it down into 
one or more jobs. 

**Job:** Triggered by an action, this represents the entire computation required to produce results for an action. A job
consists of 1 or more stages.

**Stage:** 
Each stage contains a sequence of transformations that can be completed without shuffling, shuffles mark the boundary of 
an individual stage. A stage has multiple tasks that can be executed in parallel

**Task:** A unit of work that will be performed by the executor and corresponds to 1 slot and 1 partition.


## Performance bottlnecks

I/O caused by:

Shuffle, Skew, Spill

TODO: Write more about this
