import socket, time, tty, pty, sys, os

if len( sys.argv ) < 3:
    print "[x] Usage: %s [host] [port]" % ( sys.argv[0] )
else:
    host = str( sys.argv[1] )
    port = int( sys.argv[2] )
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

    try:
        sock.bind( (host, port) )
        sock.listen( 5 )
    except:
        print "[!] Can't bind !\n"

    tty.setraw( pty.STDIN_FILENO )

    while True:
        #accept connections from outside
        print "[x] Waiting for incoming on %s:%s...\r" % (host, port)
        (csock, addr) = sock.accept()
        print "[x] Ok....%s\r" % str( addr )
        os.dup2( csock.fileno(), pty.STDIN_FILENO  )
        os.dup2( csock.fileno(), pty.STDOUT_FILENO )
        os.dup2( csock.fileno(), pty.STDERR_FILENO )
        while True:
            time.sleep( 0.01 )
            #r, w, e = select.select( [ csock.fileno(), pty.STDIN_FILENO ], [], [] )
            ##print r, str( [ csock.fileno(), pty.STDIN_FILENO ] )

            #if csock.fileno() in r:
            #    dat = os.read( csock.fileno(), 1000 )
            #    os.write( pty.STDOUT_FILENO, dat )
            #    if not dat:
            #        print "[!] client close connection....\r"
            #        break

            #if pty.STDIN_FILENO in r:
            #    dat = os.read( pty.STDIN_FILENO, 1000 )
            #    #print '--->', dat, '<---'
            #    os.write( csock.fileno(), dat )

