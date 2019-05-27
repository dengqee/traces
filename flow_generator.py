#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re
import os
import sys
import random

class FileGenerator:
    '''
    According to the information user enters in GUI,
    generate the flow description file.
    '''
    def __init__(self, 
                 out_file,
                 simu_time,
                 src, dst,
                 proto,
                 flow_num,
                 flow_trace):
        '''
        Reading user inputs params
        '''
        # output file description path
        self.out_file = os.path.join(os.getcwd(), out_file)               

        # simulation time
        # self.simu_time = int(simu_time)                                   
        self.simu_time = simu_time
        # simuation src and dst
        # self.src = int(src)
        # self.dst = int(dst)
        self.src = src
        self.dst = dst

        # protocol for traces to choose
        self.proto = proto

        # flow num
        self.flow_num = flow_num

        # input traces directory
        if flow_trace == 0:
            self.input_dir = os.path.join(os.getcwd(), 'origin_traces')       
        else:
            self.input_dir = os.path.join(os.getcwd(), 'origin_traces')

        # mapping proto to TCP/UDP
        # assume TCP is 1, UDP is 0
        self.proto_map = {
            'HTTP': 1,
            'SMTP': 1,
            'FTP': 0,
            'DNS': 0,
            'TELENET': 0
        }

        # read topology info from topo_file
        topo_file='inputFile.txt'
        # self.read_topo(topo_file)

        # generate flow description file
        self.generate()

        print('[SUCC] generate flow description file to ', self.out_file)
    
    '''
    def read_topo(self, topo_file):
        try:
            fin = open(topo_file, 'r')
        except IOError as e:
            print "[ERROR] open %s failed!" % topofile
            return

        for line in fin:
            arr = line.split(' ')
            if arr[0] == 'numHost':
                self.host_num = int(arr[1])
            elif arr[0] == 'Controller':
                self.ctrl_pos = int(arr[1])
                break
    '''

    def get_stop_time(self, start_time, idx, flow_file):
        '''
        To check whether the flow is an elephant flow or a mice flow
        If it's an elephant flow, return *True*, otherwise return *False*
        '''
        try:
            fin = open(flow_file, 'r')
        except IOError as e:
            print("[ERROR] open file %s failed!" % flow_file)
            return

        flow_duration = 0.0
        flow_size = 0
        stop_time = start_time
        for line in fin:
            arr = line.split(' ')
            time = float(arr[2])
            if time + start_time <= self.simu_time[idx]:
                stop_time = time + start_time
                flow_duration = time
                flow_size += int(arr[3])
            else:
                break

        return stop_time

    def get_flow_files(self):
        '''
        Get Trace File according to given protos
        '''
        try:
            self.fout = open(self.out_file, 'w')
        except IOError as e:
            print("[ERROR] open %s failed" % out_file)
            return

        # according to protos to get the directory store the traces
        proto_paths = ''
        for path in os.listdir(self.input_dir):
            if path == self.proto:
                proto_path = os.path.join(self.input_dir, path)
                proto_paths = proto_path
                break

        # get all the traces can choose, store them to self.trace_files
        self.trace_files = []
        for f in os.listdir(proto_path):
            file = os.path.join(proto_path, f)
            self.trace_files.append(file)

    def generate(self):
        '''
        Generate flow description files
        '''
        # get all the trace files can choose
        self.get_flow_files()
        self.fout.write(str(self.flow_num) + '\n')

        server = set()
        max_tos = 2

        for idx in range(self.flow_num):

            # get flow's src and dst
            src_node = (int)(self.src[idx])
            dst_node = (int)(self.dst[idx])

            # range [9, 100], you can modify this
            dst_port = random.randint(9, 100)
            
            # random choose a trace
            trace = random.choice(self.trace_files)

            # range [0, maxTos]
            tos = random.randint(0, max_tos)

            # the protocol in IP header
            protocol = self.proto_map[self.proto]

            # random the start time of the stream
            start_time = random.randint(2 * 1000000, ((int)(self.simu_time[idx])) * 1000000)
            stop_time = (int)(self.get_stop_time(start_time, idx, trace))

            self.fout.write(' '.join([str(src_node), str(dst_node), 
                                      str(dst_port), trace, str(tos), 
                                      str(start_time), str(stop_time), 
                                      str(protocol), '\n']))
            serv = ' '.join([str(dst_node), str(dst_port), str(protocol)])

            
            server.add(serv)

        # output the all server
        self.fout.write(str(len(server)) + '\n')
        for s in server:
            self.fout.write(s + '\n')
            

        self.fout.close()

def fileGen(out_file,time_start,time_end,src_start,src_end,des_start,des_end,flow_num):
    '''

    :param out_file: out file name
    :param timd_start: simulator start time
    :param time_end: simulator end time
    :param src_start: client start node number
    :param src_end: client end node number
    :param des_start: server start node number
    :param des_end: server end node number
    :param flow_num: the number of flow
    :return:
    '''
    srcs=[]

    dess=[]

    startTimes=[]
    for i in range(flow_num):
        srcs.append(random.randint(src_start,src_end))
        dess.append(random.randint(des_start,des_end))
        startTimes.append(random.randint(time_start,time_end))
    FileGenerator(out_file,startTimes,srcs,dess, 'HTTP', flow_num, 0)

if __name__ == '__main__':

    startTime=2
    endTime=2
    srcStart=0
    srcEnd=63
    desStart=64
    desEnd=127
    flowNum=10000
    fileGen("flow_n_n_1000.txt",startTime,endTime,srcStart,srcEnd,desStart,desEnd,flowNum)

    # print sys.argv[1]


    #FileGenerator("default-flow.txt", [5,6,8,9,10], [0,0,0,0,0], [79,79,79,79,79], 'HTTP', 5, 0) #file name,start time,source number,sink number,proto,flow_num,flow_trace
 #    FileGenerator("default-flow.txt", 5, 1, 2, 'HTTP', 1, 0)
	# FileGenerator("default-flow.txt", 4, 2, 3, 'HTTP', 1, 0)
	# FileGenerator("default-flow.txt", 5, 5, 1, 'HTTP', 1, 0)
 #    # FileGenerator(sys.argv[1],
    #               int(sys.argv[2]),
    #               int(sys.argv[3]),
    #               int(sys.argv[4]),
    #               sys.argv[5],
    #               int(sys.argv[6]),
    #               int(sys.argv[7]))
    '''
    def __init__(self, 
                 out_file="flow-dafault.txt",
                 simu_time = 10,
                 src, dst,
                 proto,
                 flow_num,
                 flow_trace):
    '''
