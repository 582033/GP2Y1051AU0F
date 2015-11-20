<?php
class pm{
    public $content;
    public function __construct(){
        exec('python ./run.py', $result);
        $this->content = count($result) >0 ? $result[0] : "get data error";
    }

    public function show(){
        echo $this->content;
    }
}
?>

<?php
if($_SERVER['REQUEST_METHOD'] == 'POST'){
    $pm = new pm();
    $pm->show();
}else{
?>
<html>
    <head>
        <script src="http://libs.baidu.com/jquery/1.9.0/jquery.js"></script>
    </head>
    <body>
        <div id="content"></div>
    </body>
<script>
    setInterval(function(){
        $.post('./', function(result){
            $('#content').text(result);
        });
    }, 1000);
</script>
</html>
<?php }?>
