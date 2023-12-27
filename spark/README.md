# What
Spark is a unified library for large-scale distributed data processing.

## Why is it special?
Spark supports batch processing, stream processing, machine learning, graph algorithms, 
SQL, etc...

Transformations occur in-memory, making it faster than MapReduce.


## High-Level Architecture

### Cluster
![spark_physical_architecture.svg](README_images/spark_physical_architecture.svg)

**Driver:** The entrypoint to the cluster that does the following: converts spark code to tasks, assigns tasks to Executors, handles task failures, and returns result to client. 

**Cluster manager:** It allocates resources(CPU, memory, storage) to the worker nodes and driver node. The types of managers are standalone, Mesos, Yarn, K8s

**Worker Node:** Physical or virtual machine in the cluster that provides the environment and resource(CPU, memory, storage) 
for executors to run.

**Executor:** JVM process that executes tasks assigned by the Driver.

**Slots:** A fancy name for executor cores. Typically, there is one slot for one task for one partition. 
So if I have four executors, and each has four slots, I can run sixteen tasks(`4 * 4 = 16`) in parallel

#### Executor memory Breakdown
![executor_memory_breakdown.svg](README_images/executor_memory_breakdown.svg)

Execution memory stores temporary data used for shuffles, joins, sorts, aggregations. When data exceeds available execution
memory, it will spill onto disk to prevent memory overload.

Storage memory stores cached data and broadcasts. This is used to improve the performance of Spark jobs that access the same
data frequently. We avoid recomputing the same DataFrames.

Reserved memory prevents OOM issues by acting as a buffer by ensuring a minimum memory allocation for Spark's
internal operations, especially when execution or storage memory runs out.

### Execution Engine

![dag_to_job_stage_task.png](README_images/dag_to_job_stage_task.png)

![job_stage_task.png](README_images/job_stage_task.png)

**Transformation:** Operations like filter, select, join, groupBy. They are "lazy" and will not execute until a spark action is invoked.
* Narrow Transformations: Transformations where one input partition contributes to only one output partition. Generally more efficient and faster.
* Wide Transformations: Transformations where multiple input partitions combine to produce multiple output partition. This means they require
a shuffle, which involves disk I/O, network I/O, and serialization/deserialization of the data.

**Action:** Operations like save, show, and count. Once the client invokes an action, Spark will evaluate the lineage of lazily stored transformations.

**Logical Plan:** Each transformation builds upon a logical plan, a tree of logical operations and high level abstraction
of the user's intended actions. After the logical plan forms, the catalyst optimizer creates a logical optimized plan (filter pushdowns, etc...)

**Physical Plan:** How the optimized logical plan will be executed in the cluster. It is represented as a DAG of RDD
transformations, representing the sequence of operations required to complete a Spark Job.

**Job:** Represents the entire computation required to produce results for an action. A job consists of 1 or more stages.

**Stage:** Each stage contains a sequence of transformations that can be completed without shuffling, shuffles mark the boundary of 
an individual stage. A stage has multiple tasks that can be executed in parallel.

**Task:** A unit of work that will be performed by the executor and corresponds to 1 slot and 1 partition. 
 Once all tasks are complete for the job, the final result will be returned to the Driver or written to disk.


## Performance bottlenecks

I/O caused by:

Shuffle, Skew, Spill

TODO: Write more about this
