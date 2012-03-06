import socket, pty, tty, select
import sys, os

if len( sys.argv ) < 3:
    print "[x] Usage: %s [host] [port]" % ( sys.argv[0] )
else:
    host = str( sys.argv[1] )
    port = int( sys.argv[2] )
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.settimeout( 10 )

    try:
        sock.bind( (host, port) )
        sock.listen( 5 )
    except:
        print "[!] Can't bind !\n"

    tty.setraw( pty.STDIN_FILENO )

    while True:
        #accept connections from outside
        print "[x] Waiting for incoming on %s:%s...\r" % (host, port)
        try:
            (csock, addr) = sock.accept()
            fsock = csock.fileno()
        except socket.timeout:
            continue

        print "[x] Ok....%s\r" % str( addr )
        while True:
            r, w, e = select.select( [ fsock, pty.STDIN_FILENO ], [], [] )
            #print r, str( [ fsock, pty.STDIN_FILENO ] )

            if fsock in r:
                dat = os.read( fsock, 1000 )
                if dat:
                    dat = dat.replace( '\x01', '' )    ## strip out magic byte
                    os.write( pty.STDOUT_FILENO, dat )
                else:
                    print "[!] client close connection....\r"
                    break

            if pty.STDIN_FILENO in r:
                dat = os.read( pty.STDIN_FILENO, 1000 )
                os.write( fsock, dat )

