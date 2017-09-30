import collections
import heapq

import json
import shutil
import worker

from multiprocessing import Process, Queue
import multiprocessing
import os

#from threading import Thread
#from time import sleep
import threading

import time

import signal

import socket

#from enum import Enum
#class Status(Enum):
#    created = 1
#    ready = 2
#    busy = 3
#    finished = 4
#    dead = 5


class Master:
    def __init__(self, num_workers, port_number):
        #ALL THE GLOBAL VARIABLES ARE HERE ...
        self.worker_status = ["created", "ready", "busy", "finished", "dead"]
        self.allworker = [{"status": "created"}, {"status": "created"}, {"status": "created"}, {"status": "created"}, {"status": "created"},]
        self.readyworker = []
        #self.cur_mappingWorker = []
        #self.cur_reducingWorker = []
        self.cur_Worker = []
        self.counter = 0
        self.jobqueue = []
        self.masterBusy = False
        self.masterStatus = "lol"  #only be "map" "reduce" "lol"#  add another "group status" in the middle --> in case there are sth wrong
        self.port = port_number

        self.currentout = ""
        self.reducer_executable = ""

        self.storeTime = [time.time(), time.time(), time.time(), time.time()]

        q = Queue()

        self.pid = [{"index": 0, "pid": 10000}, {"index": 1, "pid": 10000}, {"index": 2, "pid": 10000}, {"index": 3, "pid": 10000}]
        self.info = [ {"tolerance": "alive", "job": False, "in": [], "exec": "", "out": ""},
                      {"tolerance": "alive", "job": False, "in": [], "exec": "", "out": ""},
                      {"tolerance": "alive", "job": False, "in": [], "exec": "", "out": ""},
                      {"tolerance": "alive", "job": False, "in": [], "exec": "", "out": ""}]

        self.wow = 4
        ######################################


################################################# ALL FUNCTIONS ############################################################
        #def heartbeat(heartbeat_port_number):
        def heartbeat():
            #print ("??????????????????????????????????????????????????????????????????????????")
            #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #s.bind(("127.0.0.1", heartbeat_port_number))
            #s.bind("127.0.0.1", port_number - 1)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #s.bind(("127.0.0.1", 5999))
            s.bind(("127.0.0.1", self.port - 1))

            #s.listen(10)
            print ("Inside heartbeat")
            while True:
                #clientsocket, address = s.accept()
                max_data = 1024

                message, addr = s.recvfrom(max_data)
                all_data = message.decode("utf-8")

                message = json.loads(all_data)
#                handle_msg(message)

                if message['message_type'] == "heartbeat":
                    index = message['worker_number']
                    print ("The worker", str(index), "is alive !!!!")

                    self.storeTime[index] = time.time()

                else:
                    print ("NOOOOOOOOO !! The type is not heartbeat")

                #clientsocket.close()
#                print(all_data)

            #print ("Master Heartbeat Server: connection from", addr)

            return

        def f_tolerance():
            dead = []
            while True:
                i = 0
                while i < num_workers:
                    if self.storeTime[i] < time.time() - 10:
                        dead.append(i)
                    i = i+1
                
                while len(dead) != 0:
                #if len(dead) != 0:
                    for dd in dead:
                        print ("OMG! This Worker is DEAD!!!!!!!!    ", str(dd), " with a pid of:  ", str(self.pid[dd]['pid']) )
                        #print (str (self.pid[dd]['pid']))
                        try:
                            os.kill(self.pid[dd]['pid'], signal.SIGKILL)
                            print("Can kill !!!!!!!!!!!!!     ", str(self.pid[dd]['pid']) )
                            #dead.remove(dd)
                        except:
                            print("cannot kill this process.....already killed...     ", str(self.pid[dd]['pid']) )

                        self.allworker[dd]['status'] = "dead"

                        self.info[dd]['tolerance'] = "dead"

                        if dd in self.readyworker:
                            (self.readyworker).remove(dd)
                        
                        p = Process(target=createWorker, args=(dd, self.port))
                        p.start()

                        while not q.empty():
                            k = q.get()
                            index = k['index']
                            pid = k['pid']
                            self.pid[index]['pid'] = pid
                            print("new pid:   ", str(index), "  for worker with index: ", str(pid))

                        dead.remove(dd)

                time.sleep(8)
            return

        def createWorker(i, p_number):
#            self.pid[i]['pid'] = os.getpid()
            #print("this create worker's pid is ahahahahahha: ", str(os.getpid()))
            print("this create worker's pid is : ", str( self.pid[i]['pid'] ) )

            self.allworker[i]['status'] = "created"

            dic = {"index": i, "pid": os.getpid()}
            q.put(dic)

            w = worker.Worker(i, p_number + i + 1, p_number, p_number - 1)
            return

        #def setup(num_worker, p_number):
        def setup():
            #5th create processes for workers
            for i in range(num_workers):
                p = Process(target=createWorker, args=(i, port_number))
                #p = Process(target=worker.Worker, args=(i, port_number + i + 1, port_number, port_number-1))
                print ("!!!!!!!!!!!!!!!!!!! Now the Pid is:", str(os.getpid()) )
                p.start()

            while not q.empty():
                k = q.get()
                index = k['index']
                pid = k['pid']
                self.pid[index]['pid'] = pid
                print("new pid:   ", str(index), "  for worker with index: ", str(pid))
            #6th create 2 new threads -- heartbeat & fault tolerance
            #heartbeat_thread = threading.Thread(target=heartbeat, args=(port_number-1))
            heartbeat_thread = threading.Thread(target=heartbeat)
            print ("I am here")
            heartbeat_thread.start()
            print ("heartbeat thread starts....")
#            heartbeat_thread.join()

            i = 0
            while i < num_workers:
                self.storeTime[i] = time.time()
                i += 1

            fault_tolerance_thread = threading.Thread(target=f_tolerance)
#            fault_tolerance_thread = threading.Thread(target=f_tolerance)
            print ("doing fault tolerance thread")
            fault_tolerance_thread.start()
            print ("anything wrong???")

            #7th all do_setup_thread do, and return....
            return


        def Map(indir, mapexec):
           #####
            #self.cur_Worker = self.readyworker

            self.masterBusy = True
            self.masterStatus = "map"  #only be "map" "reduce" "lol"#

            num = len(self.readyworker)
# for hahahaha in os.listdir()
            print ("there are " + str(num)+ " ready workers")

#            for root, dirs, files in os.walk(some_directory):
#                num_file = len(files)
            filelist = os.listdir(indir)
            num_file = len(filelist)
            print ("there are ", str(num_file), " files to execute")

            n = num_file // num
            remain_file = num_file - (n * num)

            print ("and there are ", "file for each ready worker while: ", str(remain_file), " files are left...")

            count_file = 0
            #for i in range(num):

            c = 0
            for i in self.readyworker:

                ################
                self.info[i]['job'] = True
                ################

                array = []
                j = 0
                while j < n:
                    s = os.path.join(indir, str(filelist[count_file]))
                    array.append(s)
                    #print ("Print the file NAME!!!!!!!!!!!", s)
                    #array.append(filelist[count_file])
                    count_file += 1
                    j += 1

                if (c == 0) and (remain_file > 0):
                    s = os.path.join(indir, str(filelist[count_file]))
                    array.append(s)
                    #array.append(filelist[count_file])
                    count_file +=1

                if (c == 1) and (remain_file > 1):
                    s = os.path.join(indir, str(filelist[count_file]))
                    array.append(s)
                    #array.append(filelist[count_file])
                    count_file +=1

                if (c == 2) and (remain_file > 2):
                    s = os.path.join(indir, str(filelist[count_file]))
                    array.append(s)
                    #array.append(filelist[count_file])
                    count_file +=1

                c = c+1

                (self.info)[i]['in'] = array
                (self.info)[i]['out'] = "./var/job-"+str(self.counter)+"/mapper-output"
                (self.info)[i]['exec'] = mapexec

                r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                r.connect(("127.0.0.1", self.port + i + 1))
                data = json.dumps({
                    "message_type": "new_worker_job",
                    "input_files": array,
                    "executable": mapexec,
                    "output_directory": "./var/job-"+str(self.counter)+"/mapper-output"
                })
                r.sendall(data.encode('utf-8'))
                r.close()

                (self.cur_Worker).append(i)

                #MIGHT BE MORE WORKERS THAN FILES !!!!!!!!! INTERESTRING!!!!!!!!!!!!!!!!!!!!
                if count_file == num_file:
                    break

            if count_file == num_file:
                print ("Oh YEAH! The files are distributed correctly")
            else:
                print ("NOOOOOOOOOO!!! Map Files Wrong!")


            self.wow = len(self.cur_Worker)

            for i in self.cur_Worker:
                (self.allworker[i])['status'] = "busy"
                (self.readyworker).remove(i)
            #self.readyworker = []

#            return len(cur_doingWorker)
            return

        def __staff_run_group_stage(self, input_dir, output_dir, num_workers):
            # Loop through input directory and get all the files generated in Map stage
            filenames = []

            for in_filename in os.listdir(input_dir):
                filename = input_dir + in_filename

                # Open file, sort it now to ease the merging load later
                with open(filename, 'r') as f_in:
                    content = sorted(f_in)

                # Write it back into the same file
                with open(filename, 'w+') as f_out:
                    f_out.writelines(content)

                # Remember it in our list
                filenames.append(filename)

            # Create a new file to store ALL the sorted tuples in one single
            sorted_output_filename = os.path.join(output_dir, 'sorted.out')
            sorted_output_file = open(sorted_output_filename, 'w+')

            # Open all files in a single map command! Python is cool like that!
            files = map(open, filenames)

            # Loop through all merged files and write to our single file above
            for line in heapq.merge(*files):
                sorted_output_file.write(line)

            sorted_output_file.close()

            # Create a circular buffer to distribute file among number of workers
            grouper_filenames = []
            grouper_fhs = collections.deque(maxlen=num_workers)

            for i in range(num_workers):
                # Create temp file names
                basename = "file{0:0>4}.out".format(i)
                filename = os.path.join(output_dir, basename)
  
                # Open files for each worker so we can write to them in the next loop
                grouper_filenames.append(filename)
                fh = open(filename, 'w')
                grouper_fhs.append(fh)

            # Write lines to grouper output files, allocated by key
            prev_key = None
            sorted_output_file = open(os.path.join(output_dir, 'sorted.out'), 'r')

            for line in sorted_output_file:
                # Parse the line (must be two strings separated by a tab)
                tokens = line.rstrip().split("\t", 2)
                assert len(tokens) == 2, "Error: improperly formatted line"
                key, value = tokens

                # If it's a new key, then rotate circular queue of grouper files
                if prev_key != None and key != prev_key:
                    grouper_fhs.rotate(1)

                # Write to grouper file
                fh = grouper_fhs[0]
                fh.write(line)

                # Update most recently seen key
                prev_key = key

            # Close grouper output file handles
            for fh in grouper_fhs:
                fh.close()

            # Delete the sorted output file
            sorted_output_file.close()
            os.remove(sorted_output_filename)

            # Return array of file names generated by grouper stage
            return grouper_filenames

        def Reduce(files, outdir, reduce_exec):
            #self.cur_Worker = self.readyworker

            self.masterBusy = True
            self.masterStatus = "reduce"  #only be "map" "reduce" "lol"#

            num = len(self.readyworker)
            print ("there are ", str(num), " ready workers")

            num_file = len(files)
            print ("there are ", str(num_file), " files to execute")

            n = num_file // num
            remain_file = num_file - (n * num)

            print ("and there are ", str(n), "file for each ready worker while: ", str(remain_file), " files are left...")

            count_file = 0
            #for i in range(num):
            c = 0

            for i in self.readyworker:
                array = []
                j = 0
                while j < n:
                    #s = "./var/job-"+ str(self.counter) + "/grouper-output/" + str (files[count_file])
                    s = str (files[count_file])
                    array.append(s)
                    #array.append(f[count_file])
                    count_file += 1
                    j += 1

                if c == 0 and remain_file > 0:
                    #s = "./var/job-"+ str(self.counter) + "/grouper-output/" + str (files[count_file])
                    s = str (files[count_file])
                    array.append(s)
                    #array.append(f[count_file])
                    count_file +=1

                if c == 1 and remain_file > 1:
                    #s = "./var/job-"+ str(self.counter) + "/grouper-output/" + str (files[count_file])
                    s = str (files[count_file])
                    array.append(s)
                    #array.append(f[count_file])
                    count_file +=1

                if c == 2 and remain_file > 2:
                    #s = "./var/job-"+ str(self.counter) + "/grouper-output/" + str (files[count_file])
                    s = str (files[count_file])
                    array.append(s)
                    #array.append(f[count_file])
                    count_file +=1

                c = c+1

                (self.info)[i]['in'] = array
                (self.info)[i]['out'] = "./var/job-"+str(self.counter)+"/reducer-output/"
                (self.info)[i]['exec'] = reduce_exec

                r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                r.connect(("127.0.0.1", self.port + i + 1))
                data = json.dumps({
                    "message_type": "new_worker_job",
                    "input_files": array,
                    "executable": reduce_exec,
                    "output_directory": "./var/job-"+str(self.counter)+"/reducer-output/"
                })
                r.sendall(data.encode('utf-8'))
                r.close()

                (self.cur_Worker).append(i)
                #MIGHT BE MORE WORKERS THAN FILES !!!!!!!!! INTERESTRING!!!!!!!!!!!!!!!!!!!!
                if count_file == num_file:
                    break

            if count_file == num_file:
                print ("Oh YEAH! The !!!REDUCE!!! files are distributed correctly")
            else:
                print ("NOOOOOOOO Reduce files wrong")

            for i in self.cur_Worker:
                (self.allworker[i])['status'] = "busy"
                (self.readyworker).remove(i)

            #self.readyworker = []

            #for i in self.cur_Worker:
            #    print (str(i))

            return

        def shutdown():
            #kill all workers' processes
            for i in self.pid:
                try:
                    os.kill(i['pid'], signal.SIGKILL)
                except:
                    print ("shit..cant kill one process")

            return

        def handle_msg(msg):
            #change worker status
            if msg['message_type'] == "status":
                index = msg['worker_number']
                status = msg['status']

                if status in (self.worker_status):
                    (self.allworker)[index]['status'] = status
                else:
                    print ("something wroing, no such status")

                if status == "ready":
                    if index not in self.readyworker:
                        (self.readyworker).append(index)
                    else:
                        print ("?????????????? It is already ready, why send again? something wrong" )
                    ##############################Fault Tolerance##################################
                    if (self.info)[index]['tolerance'] == "dead":
                        (self.info)[index]['tolerance'] = "alive"
                        if (self.info)[index]['job'] == True:
                            r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            r.connect(("127.0.0.1", self.port + index + 1))
                            data = json.dumps({
                                "message_type": "new_worker_job",
                                "input_files": (self.info)[index]['in'],
                                "executable": (self.info)[index]['exec'],
                                "output_directory": (self.info)[index]['out']
                            })
                            r.sendall(data.encode('utf-8'))
                            r.close()
                    ###############################################################################

                if status == "finished":
                    if index in self.cur_Worker:
                        (self.cur_Worker).remove(index)
                    else:
                        print ("Something wrong!!! The index should be in the cur_worker --> since it is running the job!!!!")

                    print ("Finished !!! INDEX: ", str(index))

                    (self.allworker)[index]['status'] = "ready"
                    if index not in self.readyworker:
                        (self.readyworker).append(index)
                    else:
                        print ("!!!!!!!!!!!!!!!!!!! FINISH THEN READY!!!!!!!!!!!! Why it is already ready!!! something wrong")

                    ##The worker finishes the job....when dead, do not need to redo anything..... mark it JOB FALSE!!!
                    if self.masterStatus == "reduce":
                        (self.info)[index]['job'] = False

                    if len(self.cur_Worker) == 0:
                        if self.masterStatus == "map":  #only be "map" "reduce" "lol"#
                            #Worker finish mapping
                            worker_duoshao = len(self.readyworker)
                            #worker_duoshao = self.wow
                            #GROUP
                            self.masterStatus == "group"
                            f = __staff_run_group_stage(self, "./var/job-"+str(self.counter)+"/mapper-output/", "./var/job-"+str(self.counter)+"/grouper-output/", worker_duoshao)
                            #Worker finish grouping

                            #REDUCE
                            #Reduce(f, msg['output_directory'], msg['reducer_executable'])
                            Reduce(f, self.currentout, self.reducer_executable)

                        elif self.masterStatus == "reduce":
                            self.masterStatus = "lol"
                            self.masterBusy = False
                            #Worker finish reducing

                            #copy all the outputs to the output directory!!!!
                            red_out = "./var/job-"+str(self.counter)+"/reducer-output/"
                            out = self.currentout
                            #out = msg['output_directory']
                            
                            time.sleep(1)
                            g_out = "./var/job-"+str(self.counter)+"/reducer-output/"
                            while len(os.listdir(red_out)) < len(os.listdir(g_out)):
                                print ("Need time for reducer to get all the output files")

                            if not os.path.exists(out):
                                os.makedirs(out)
                            #print ("I am gonna copy files")
                            for i in os.listdir(red_out):
                                print (str(i))
                                name = os.path.join(red_out, str(i))
                                if (os.path.isfile(name)):
                                    print ("print print print print")
                                    shutil.copy(name , out)

                            for i in range(4):
                                (self.info)[index]['job'] = False

                            self.counter += 1
                    
                    else:
                        for i in self.cur_Worker:
                            print (str(i))
                return

            #new job reqeust
            if msg['message_type'] == "new_master_job":
                if self.masterBusy:
                    (self.jobqueue).append( {"indir": msg['input_directory'], "outdir": msg['output_directory'], "mapper": msg['mapper_executable'], "reducer": msg['reducer_executable']}  )
                    return
                else:
                    self.masterBusy = True
                    newpath = "./var/job-" + str(self.counter)
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                        newpath = "./var/job-" + str(self.counter) + "/mapper-output"
                        os.makedirs(newpath)
                        newpath = "./var/job-" + str(self.counter) + "/grouper-output"
                        os.makedirs(newpath)
                        newpath = "./var/job-" + str(self.counter) + "/reducer-output"
                        os.makedirs(newpath)
                    else:
                        print ("something wrong, this directory is already exist")
                        #os.remove(newpath)
                        #os.makedirs(newpath)

#                if self.masterBusy:
#                    (self.jobqueue).append = {"indir": msg['input_directory'], "outdir": msg['output_directory'], "mapper": msg['mapper_executable'], "reducer": msg['reducer_executable']}
#                else:
                    
                    self.currentout = msg['output_directory']
                    self.reducer_executable = msg['reducer_executable']

                    #MAP
                    Map(msg['input_directory'], msg['mapper_executable'])

                    ###############For Debug####################
                    #time.sleep(60)
                    ############################################

                    #while len(self.cur_Worker) != 0:
                    #    print "Worker is doing Mapping"
                    #Worker finish mapping

                    #worker_duoshao = len(self.readyworker)
                    #GROUP
                    #f = __staff_run_group_stage(self, "./var/job-"+str(self.counter)+"/mapper-output", "./var/job-"+str(self.counter)+"/grouper-output", worker_duoshao)
                        #Worker finish grouping

                    #REDUCE
                    #Reduce(f, msg['output_directory'], msg['reducer_executable'])
                    #while len(self.cur_Worker) != 0:
                    #    print "Worker is doing Reducing"
                    #Worker finish reducing

                    #copy all the outputs to the output directory!!!!
                    #red_out = "./var/job-"+str(self.counter)+"/reducer-output/"
                    #out = msg['output_directory']
                    #if not os.path.exists(out):
                    #    os.makedirs(out)
                    #for i in os.listdir(red_out):
                    #    name = os.path.join(red_out, i)
                    #    if (os.path.isfile(name)):
                    #        shutil.copy(name , out)

                #self.counter += 1
                return
        
            #Map Stage && Reduce Stage
#            if msg['message_type'] == "new_master_job":

#                return
          
            #Shutdown
            if msg['message_type'] == "shutdown":
                shutdown() 
                return

            print ("something wrong !!! no task matches to this msg type")
            return



################################################################################
        #1st step: create the new folder
        newpath = "./var"
        if not os.path.exists(newpath):
            #print ("no such dir")
            os.makedirs(newpath)
        else:
            #print ("this folder already exist..delete it first")
 #           if os.path.isdir(newpath):
            shutil.rmtree(newpath)
            os.makedirs(newpath)
        print ("1st step: Make VAR")

        #2nd step: create a new TCP socket
        #if __name__ == "__main__":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", port_number))

        s.listen(20)
        print ("2nd step: Create a new TCP")

        #3rd step: create a new thread do_setup_thread
        #do_setup_thread = threading.Thread(target=setup, args=(num_workers, port_number))
        do_setup_thread = threading.Thread(target=setup)
        print ("do setup thread setting")
        do_setup_thread.start()
#        print ("setup thread start")
#        do_setup_thread.join()

#        print ("Start accepting new msgs")
        #4th: starting accepting new msgs...
        while True:
            #print ("hahahahahahhaha")

            print ("??????????????????????????????????????????????????????")
            #for i in range(num_workers):
            #    print ( str(self.pid[i]['pid']) )
            while not q.empty():
                k = q.get()
                index = k['index']
                pid = k['pid']
                self.pid[index]['pid'] = pid
                print("worker index:   ", str(index), "  with new pid: ", str(pid))
                print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                #for i in range(num_workers):
                #    print ( str(self.pid[i]['pid']) )

################################# When the master is idle ##################### See whether there are other tasks need to be executed...haha
            if self.masterBusy == False and self.masterStatus == "lol" and len(self.jobqueue) > 0:
                print ("job queue has sth to do!!!!!!")
                self.masterBusy = True
                newpath = "./var/job-" + str(self.counter)
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                    newpath = "./var/job-" + str(self.counter) + "/mapper-output"
                    os.makedirs(newpath)
                    newpath = "./var/job-" + str(self.counter) + "/grouper-output"
                    os.makedirs(newpath)
                    newpath = "./var/job-" + str(self.counter) + "/reducer-output"
                    os.makedirs(newpath)
                else:
                    print ("something wrong, this directory is already exist")

                self.currentout = self.jobqueue[0]['outdir']
                self.reducer_executable = self.jobqueue[0]['reducer']

                Map(self.jobqueue[0]['indir'], self.jobqueue[0]['mapper'])

                (self.jobqueue).pop(0)
##############################################################################
            clientsocket, address = s.accept()
            max_data = 1024
            all_data = ""
            print ("Master TCP Server: connection from", address)
            while True:
                message = clientsocket.recv(max_data)
                all_data += message.decode("utf-8")

                if len(message) != max_data:
                    #message = json.loads(all_data)
                    #handle_msg(message)
                    break;
            message = json.loads(all_data)
            handle_msg(message)
            clientsocket.close()
#            print(all_data)

        return

