from sys import argv
from socket import socket, gethostbyname
from _thread import start_new_thread, allocate_lock

def sockread(lock):
    try:
      while True:
        msg=s.recv(1024)
        if len(msg)==0:
            lock.release()
        print(msg.decode('utf-8'),end='')
    except:
      lock.release() 

def sockwrite(lock):
    try:
      while True:
        msg=input("")
        s.send((msg+'\n').encode('utf-8'))
    except:
      lock.release()

if len(argv)!=3:
    print("usage: nc -l port | nc addr port")
    exit(1)
s=socket()
if argv[1]=='-l':
    port=int(argv[2])
    s.bind(('0.0.0.0',port))
    s.listen(1)
    c,addr=s.accept()
    s=c
else:
    addr=gethostbyname(argv[1])
    port=int(argv[2])
    s.connect((addr,port))

lock=allocate_lock()
lock.acquire()
start_new_thread(sockread,(lock,))
start_new_thread(sockwrite,(lock,))
try:
  lock.acquire()
except:
  pass
