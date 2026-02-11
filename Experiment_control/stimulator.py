################################
# Electrotactile Stimulation frontend#
#script created by Sina Parsnejad and Yousef Gtat
################################

import serial.tools.list_ports
import threading
import sys
import time
import random
import math
import funcs
import json
import csv


################################
mac_port = '/dev/cu.usbmodem1451'
port = 'COM3'
################################
title= 'test_set_2.csv'  #target csv file name

amp= 10  #current amplitude 
PBD= 1000 #Post-bundle delay
PuF= 2000 #Base pulse frequency
rand= 'not random' #choices are:   'not random' & 'random'
################################

test_order = [
    ['reset', 'prefix_off'],
    ]

test_order = funcs.runfile (title, PBD, PuF, amp, rand)

    
with open('generic_test_order.csv', mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['stack', 'CH', 'SPW', 'PePD' , 'NS', 'IPD', 'NP', 'NB', 'IBD', 'PBD', 'word_amp'])
    for row in (test_order):
         stim_writer.writerow([row])


################################
options = test_order
################################

# serial interface
cntr= 1;

packet = b''
streaming_flag = False
def reading(serial_port, stop_event, size):
  print('Serial Reader is ready...')
  sys.stdout.flush()
  global packet
  global streaming_flag
  while(not stop_event.is_set()):
    raw = serial_port.read(size=size) #not thread safe if timeout=None (infinit)
    if raw != b'':
      if raw == b'\r':
        if len(packet) != 0:
          if packet == b'Streaming':
            streaming_flag = True
            print(packet)
        packet = b''
      else:
        packet += raw

if __name__ == '__main__':
  devs = serial.tools.list_ports.comports()
  for dev in devs:
    print(dev)
  try:
    ser = serial.Serial(port, 9600, timeout=0.1) #read will block if timeout=None
  except serial.SerialException:
    print('SerialException: cannot create HAT serial object')
    sys.exit()
  else:
    if ser.isOpen():
      print('HAT serial port is opened successfully!')
  #
  thread_stop = threading.Event()
  thread = threading.Thread(target=reading, args=(ser, thread_stop, 1))
  thread.start()
  #
  while(1):
    query = str(input('*****Type exit or go> '))
    if (query == "exit") or (query == "q"):
      ser.write('stop\r\n'.encode())
      thread_stop.set()
      break
    elif (query == "go"):
      for p in options:
        if (type(p) == list):
          if (len(p) % 2) != 0:
            print('WARNING: unable to send packets ', p)
            continue
          i = 0;
          while (i<len(p)):
            msg = "{}\r\n".format(p[i])
            ser.write(msg.encode())
            #print('sent: ', msg)
            i+=1
          print('sent: ', p)
        else:
          if p=='prompt':
            inter_flag = 1
            while(inter_flag):
              inter_query = str(input('*****Type r (repeat) or c (continue) or q (quit) then enter> ')).lower()
              print("stim #", cntr)
              cntr+=1
              if inter_query=='r':
                msg = "{}\r\n".format('stream')
                ser.write(msg.encode())
                while(not streaming_flag): pass
                streaming_flag = False
              elif inter_query=='c':
                inter_flag = 0
              elif inter_query=='q':
                ser.write('stop\r\n'.encode())
                thread_stop.set()
                print('waiting on read thread...')
                sys.stdout.flush()
                thread.join()
                print("serial is closing...")
                sys.stdout.flush()
                ser.close()
                print("bye")
                sys.stdout.flush()
                inter_flag = 0
                time.sleep(5)
                sys.exit()
          else:    
            msg = "{}\r\n".format(p)
            ser.write(msg.encode())
            while(not streaming_flag): pass
            streaming_flag = False
    elif (query == "print"):
      print('received: ', packet)
    elif (query == "clear"):
      packet = b''
    elif (query == "report"):
        stim_nu=0
        for stim_nu in range(len(my_list)) :
            print([stim_nu+1, my_list[stim_nu] ])       
    else:
      ser.write('{}\r\n'.format(query).encode())



  #
  print('waiting on read thread...')
  sys.stdout.flush()
  thread.join()
  #
  print("serial is closing...")
  sys.stdout.flush()
  ser.close()
  #
  print("bye bitch")
  sys.stdout.flush()
  time.sleep(5)
