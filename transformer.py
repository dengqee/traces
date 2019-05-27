#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os

def escape(ip_addr):
    '''
    convet '/ |  | :' to '.' in ip_addr such as CDP/VTP/DTP/PAgP/UDLD
    '''
    addr = '.'.join(ip_addr.split('/'))
    addr = '.'.join(addr.split(':'))
    return '.'.join(addr.split(' '))

def print_traces_to_files(counter):
    '''
    store packet info in counter(a dict),
    and output to files according to proto and src_dst_pair
    '''

    print '[INFO] Writing file to disk ... '

    out_dir = os.path.join(os.getcwd(), "origin_traces")

    if (not os.path.exists(out_dir)):
        try:
            os.mkdir(out_dir)
        except IOError as e:
            print "[ERROR] make directory %s failed!" % out_dir

    for proto in counter.keys():

        # create the directory to store files
        dirname = os.path.join(out_dir, proto)
        if (not os.path.exists(dirname)):
            try:
                os.mkdir(dirname)
            except IOError as e:
                print "[ERROR] make directory %s failed!" % dirname
                return

        for filename in counter[proto].keys():
            
            out_file_name = os.path.join(dirname, filename + ".txt")
            try:
                fout = open(out_file_name, 'w')
            except IOError as e:
                print "[ERROR] open %s failed!" % out_file_name
                return
            
            for packet in counter[proto][filename]:
                fout.write(packet)
            
            fout.close()

def process_trace_file(file_path):
    '''
    reading input_trace_file contents, and store it to output_traces directory.
    input_trace_file is a csv file
    '''
    print '[INFO] Processing %s .... ' % file_path

    try:
        fin = open(file_path, 'r')
    except IOError as e:
        print "[ERROR] open file %s failed!" % file_path
        return
    
    # remove the first description line
    fin.readline()
    
    counter = {}
    timer = {}
    total_packets = 0
    
    # read rest lines from input_trace_file
    while True:
        arr = fin.readline().split(',')
        if len(arr) < 2: break  # end of input_trace_file
        total_packets += 1

        # attention! use [1:-1] to remove the outside "" wrapper

        time = int(float(arr[1][1:-1])*1000000)  # convert time to microsecond format
        src = escape(arr[2][1:-1])          # src_ip
        dst = escape(arr[3][1:-1])          # dst_ip
        proto = escape(arr[4][1:-1])        # proto
        size = int(arr[5][1:-1])            # get the size
        
        # counter
        src_dst = '-'.join([src, dst])  # src_dst pair, for output_filename
        counter.setdefault(proto, {})
        timer.setdefault(proto, {})
        counter[proto].setdefault(src_dst, [])
        timer[proto].setdefault(src_dst, time)
        counter[proto][src_dst].append(' '.join([str(len(counter[proto][src_dst])), 'I', str(time-timer[proto][src_dst]), str(size), '\n']))
    
    ## print traces to files
    print_traces_to_files(counter)

    print "\nTotally have %s packets." % (total_packets)

def main():
    '''
    reading input_trace files
    '''
    dir = os.path.join(os.getcwd(), "input_traces")
    for file_name in os.listdir(dir):
        file_path = os.path.join(dir, file_name)
        process_trace_file(file_path)

if __name__ == "__main__":
    main()
