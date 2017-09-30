#import worker
import os
import socket
import json

import sh
#import time
#from multiprocessing import Process
#from threading import Thread
#from time import sleep
import multiprocessing
import threading
import time

import subprocess

class Worker:
    def __init__(self, worker_number, port_number, master_port, master_heartbeat_port):

#####################################Function###########################################
        def heartbeat(worker_number, port_number, master_port, master_heartbeat_port):
#        def heartbeat():
            while True:
                r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                #r.connect(("127.0.0.1", master_heartbeat_port))
                data = json.dumps({
                    "message_type": "heartbeat",
                    "worker_number": worker_number
                })
                #print ("sending...")
                r.sendto(data.encode('utf-8'), ('127.0.0.1', master_heartbeat_port))
                r.close()
                #print ("sending heartbeat...")
                time.sleep(2)
                #r.close()
#        clientsocket.sendto
            return

        def setup(worker_number, port_number, master_port, master_heartbeat_port):
            #1. create the worker heartbeat thread
            heart = threading.Thread(target=heartbeat, args=(worker_number, port_number, master_port, master_heartbeat_port))
            #heart = threading.Thread(target=heartbeat)
            heart.start()
            print ("worker heartbeat thread starts")
            #heartbeat.join()

            #2. tell the master this worker is ready
            r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            r.connect(("127.0.0.1", master_port))
            data = json.dumps({
                "message_type": "status",
                "worker_number": worker_number,
                "status": "ready"
            })
            r.sendall(data.encode('utf-8'))
            r.close()

            return

        def handle_msg(msg, master_port, worker_number):
            if msg['message_type'] == "new_worker_job":
                files = msg['input_files']
                exe = msg['executable']
                outdir = msg['output_directory']
                #Just execute all the files and put the outputs in the according outdir

                #print ("PRINT THE !!!EXE!!!", exe)
                print ("PRINT THE FILE", files[0])

                for f in files:
################Name exactly like the input file.... in / out same names
                    thisf = f.split("/")[len(f.split("/"))- 1]
                    full_output = os.path.join(outdir, thisf)

                    run = sh.Command(exe)
                    run(_in = open(f), _out = full_output)

                #while len(os.listdir(outdir)) < len(files):
                #    print ("Need to wait until all output files are finished...!!!!!!!!!!!!!! FOR COPY !!!!!!")
                #time.sleep(1)

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("127.0.0.1", master_port))
                data = json.dumps({
                    "message_type": "status",
                    "worker_number": worker_number,
                    "status": "finished"
                })
                s.sendall(data.encode('utf-8'))
                s.close()

            else:
                print ("no such work message type!!! ZZZ")

            return

        def getpid():
            return os.getpid()

########################################################################################

        #1st step: create new TCP of this work's port number
        #if __name__ == "__main__":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", port_number))

        s.listen(20)

        #2nd: do_setup_thread
        print ("Inside worker.... I am creating do setup thread")
        do_setup_thread = threading.Thread(target=setup, args=(worker_number, port_number, master_port, master_heartbeat_port))
        do_setup_thread.start()
        #because it needs to be ready fisrt then can here...
        #do_setup_thread.join()
        print ("one worker finish setup")

        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Worker's PID IS: ", os.getpid())
        #pid.append(os.getpid())

        while True:
            clientsocket, address = s.accept()
            max_data = 1024
            all_data = ""
            print ("Worker TCP Server: connection from", address)

            while True:
                message = clientsocket.recv(max_data)
                all_data += message.decode("utf-8")

                if len(message) != max_data:
                    #message = json.loads(all_data)
                    #handle_msg(message, master_port, worker_number)
                    break;

            message = json.loads(all_data)
            handle_msg(message, master_port, worker_number)
            clientsocket.close()
#            print(all_data)

        return
            
