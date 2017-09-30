# MapReduce
In this project, you will implement a simplified MapReduce server in Python. 
This will be a single machine, multi-process, multi-threaded server that will execute user-submitted MapReduce jobs. 
It will run each job to completion, handling failures along the way, and write the output of the job to a given directory. 
Once you have completed this project, you will be able to run any MapReduce job on your machine, using a MapReduce implementation you wrote!

There are two primary classes in this project:
-	The Master, which will listen for MapReduce jobs, manage the jobs, distribute work amongst workers, and handle fault tolerance
-	The Worker, which will wait for commands from the Master, and then perform map or reduce tasks based on given input parameters

You will not be writing actual map or reduce functions, but instead focusing on the server itself. 
We have provided you with several sample map/reduce executables (in Python) that you can use to test your MapReduce server.
