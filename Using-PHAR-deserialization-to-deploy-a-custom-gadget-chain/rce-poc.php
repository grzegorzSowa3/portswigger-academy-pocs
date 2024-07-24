<?php

// sudo apt-get install composer
// composer require twig/twig:1.1.9
// run php gadget-chain.php "<command>" before to generate out.jpg

require_once('vendor/autoload.php');


class CustomTemplate {
    private $template_file_path;

    public function __construct($template_file_path) {
        echo "CustomTemplate construct\n";
        $this->template_file_path = $template_file_path;
    }

    private function isTemplateLocked() {
        return file_exists($this->lockFilePath());
    }

    public function getTemplate() {
        return file_get_contents($this->template_file_path);
    }

    public function saveTemplate($template) {
        if (!isTemplateLocked()) {
            if (file_put_contents($this->lockFilePath(), "") === false) {
                throw new Exception("Could not write to " . $this->lockFilePath());
            }
            if (file_put_contents($this->template_file_path, $template) === false) {
                throw new Exception("Could not write to " . $this->template_file_path);
            }
        }
    }

    public function __wakeup() {
        echo "CustomTemplate wakeup\n";
    }

    function __destruct() {
        echo "CustomTemplate destruct\n";
        // Carlos thought this would be a good idea
        @unlink($this->lockFilePath());
    }

    private function lockFilePath()
    {
        echo "CustomTemplate lockFilePath\n";
        return 'templates/' . $this->template_file_path . '.lock';
    }
}

class Blog {
    public $user;
    public $desc;
    private $twig;

    public function __construct($user, $desc) {
        $this->user = $user;
        $this->desc = $desc;
        echo "Blog constructor\n";
    }

    public function __toString() {
        echo "Blog toString\n";
        return $this->twig->render('index', ['user' => $this->user]);
    }

    public function __wakeup() {
        echo "Blog wakeup\n";
        $loader = new Twig_Loader_Array([
            'index' => $this->desc,
        ]);
        $this->twig = new Twig_Environment($loader);
    }

    public function __sleep() {
        echo "Blog sleep\n";
        return ["user", "desc"];
    }
}


$filename = "out.jpg";
echo file_exists("phar://{$filename}") . "\n"

?>
