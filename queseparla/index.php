<?php
//error_reporting(E_ERROR | E_WARNING | E_PARSE);
require 'Slim/Slim.php';
require_once('redbean/rb.php');
require_once ('functions.inc.php');
// set up database connection
R::setup('mysql:host=localhost;dbname=queseparla','root','toor');
R::freeze(true); // CONGELA LA DB Y NO LA MODIFICA
R::$writer->setUseCache(true);

\Slim\Slim::registerAutoloader();
require "Slim/Extras/Log/DateTimeFileWriter.php";

require_once 'mobiledetect/Mobile_Detect.php';


$dir_logs="./leslogs/".(date("Y/m/d"));
if(!is_dir($dir_logs)){
	mkdir($dir_logs,0755,true);
}

$app = new \Slim\Slim(array(
    "log.writer" => new \Slim\Extras\Log\DateTimeFileWriter(array(
        "path" => "./leslogs/",
        "name_format" => "Y/m/d/Y-m-d",
        "date_format" => "Y-m-d H:i:s",
        "message_format" => "%label% [%date%] %message%"
    ))
));

$app->config(
	array(
		'template.path' => './templates',
		'log.enabled'   => true,
		'log.level'     => \Slim\Log::DEBUG,
		'paginacion'	=> 100
	)
);


$app->hook('slim.before.router', function () use ($app){    
	$res = $app->response();
    $res['Como-se-hizo'] = "Bots + Pilsen + python";
});


$app->notFound(function () use ($app) {
	if(strstr($_SERVER["SCRIPT_URI"], 'json')){
		$app->contentType('application/json');
		echo json_encode(array('404'=>'Contenido no encontrado :('));
	} else {
		$app->render('404.html');
	}
});

class ResourceNotFoundException extends Exception {}

$app->get('/', function() use($app){
	$detect = new Mobile_Detect;
	if ($detect->isMobile() ) {
 		$app->render('inicio.php');
	} else {
		$app->redirect("/queseparla/acerca/");
	}
	
});

$app->get('/home/', function() use($app){
	$app->render('inicio.php');
});


$app->get('/acerca/', function() use($app){
	$app->render('acerca.php');
});

$app->get('/proximos/json/', function() use($app){
	$fecha=date('Y-m-d');
	$app->response()->header('Content-Type', 'application/json');
	$q="SELECT * FROM (( SELECT 'S' AS camara,(id_preagenda) AS padre, id, texto, fecha_evento FROM agenda_senado ORDER BY fecha_evento DESC )UNION( SELECT 'D' AS camara, (id_preagenda) AS padre, id, texto, fecha_evento FROM agenda_diputados ORDER BY fecha_evento DESC )) AS t WHERE fecha_evento>='$fecha' ORDER BY fecha_evento DESC";
	try { 
		$data=R::getAll($q);
		if($data){
			echo json_encode(($data));	
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
	
});

$app->get('/ultimomes/json/', function() use($app){
	$fecha=date('Y-m-d');
	$ultimos30=date('Y-m-d', strtotime('today - 30 days'));
	$app->response()->header('Content-Type', 'application/json');
	$q="SELECT * FROM (( SELECT 'S' AS camara,(id_preagenda) AS padre, id, texto, fecha_evento FROM agenda_senado ORDER BY fecha_evento DESC )UNION( SELECT 'D' AS camara, (id_preagenda) AS padre, id, texto, fecha_evento FROM agenda_diputados ORDER BY fecha_evento DESC )) AS t WHERE fecha_evento<='$fecha' AND fecha_evento>='$ultimos30' ORDER BY fecha_evento DESC";
	try { 
		$data=R::getAll($q);
		if($data){
			echo json_encode(($data));	
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
	
});

$app->post('/buscar/', function() use($app){
	
	$json=json_encode($_POST);
	$md5=md5($json);
	file_put_contents('./cache/'.$md5, $json);
	$app->redirect("/queseparla/buscar/$md5/");
});


$app->get('/buscar/(:hash)/', function($hash='') use($app){
	$json=file_get_contents("./cache/$hash");
	$json=json_decode($json,true);
	$palabra=$json['palabra'];

	$q="SELECT * FROM (( SELECT 'S' AS camara,(id_preagenda) AS padre, id, texto, fecha_evento FROM agenda_senado ORDER BY fecha_evento DESC )UNION( SELECT 'D' AS camara, (id_preagenda) AS padre, id, texto, fecha_evento FROM agenda_diputados ORDER BY fecha_evento DESC )) AS t WHERE texto LIKE '%$palabra%' ORDER BY fecha_evento DESC";
	try { 
		$data=R::getAll($q);
		if($data){
			//echo json_encode(($data));
			$data['info']=$data;
			$data['palabra']=$palabra;
			$app->render('buscador.php',$data);
		} else {
			$data['info']=$data;
			$data['palabra']=$palabra;
			$app->render('buscador.php',$data);
			//throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
	
});


$app->get('/preagenda/senado/json/', function() use($app){
	$app->response()->header('Content-Type', 'application/json');
	try {
		//$campos.=" LIMIT $page, ".$app->config('paginacion');
		$articles = R::find('preagenda_senado','ORDER BY id DESC');
		if($articles){
			echo json_encode(R::exportAll($articles));	
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
});

$app->get('/preagenda/senado/(:id)/json/', function($id=1) use($app){
	$app->response()->header('Content-Type', 'application/json');
	try {		
		$article = R::findOne('preagenda_senado', 'id=?', array($id)); 
		if($article){
			echo json_encode(R::exportAll($article));	
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
});

$app->get('/preagenda/diputados/json/', function() use($app){
	$app->response()->header('Content-Type', 'application/json');
	try {
		//$campos.=" LIMIT $page, ".$app->config('paginacion');
		$articles = R::find('preagenda_diputados','ORDER BY id DESC');
		if($articles){
			echo json_encode(R::exportAll($articles));	
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
});

$app->get('/preagenda/diputados/(:id)/json/', function($id=1) use($app){
	$app->response()->header('Content-Type', 'application/json');
	try {		
		$article = R::findOne('preagenda_diputados', 'id=?', array($id)); 
		if($article){
			echo json_encode(R::exportAll($article));	
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
});



$app->get('/diputados/', function() use($app){
		$app->render('diputados.php');
});


$app->get('/senado/', function() use($app){
		$app->render('senado.php');
});


$app->get('/agenda/diputados/proximos/json/', function() use($app){
	$app->response()->header('Content-Type', 'application/json');
	try {
		$fecha=date('Y-m-d');
		$q="SELECT 'D' AS camara,(id_preagenda) AS padre, id, texto, fecha_evento FROM agenda_diputados WHERE fecha_evento>='$fecha' ORDER BY fecha_evento DESC ";
		$articles = R::getAll($q);
		if($articles){
			echo json_encode(($articles));	
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
});


$app->get('/agenda/senado/proximos/json/', function() use($app){
	$app->response()->header('Content-Type', 'application/json');
	try {
		$fecha=date('Y-m-d');
		$q="SELECT 'S' AS camara,(id_preagenda) AS padre, id, texto, fecha_evento FROM agenda_senado WHERE fecha_evento>='$fecha' ORDER BY fecha_evento DESC ";
		$articles = R::getAll($q);
		if($articles){
			echo json_encode(($articles));	
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
});


$app->get('/agenda/diputados/ultimos/json/', function() use($app){
	$app->response()->header('Content-Type', 'application/json');
	try {
		$fecha=date('Y-m-d');
		$ultimos30=date('Y-m-d', strtotime('today - 30 days'));
		$q="SELECT 'D' AS camara,(id_preagenda) AS padre, id, texto, fecha_evento FROM agenda_diputados WHERE fecha_evento<='$fecha' AND fecha_evento>='$ultimos30' ORDER BY fecha_evento DESC ";
		$articles = R::getAll($q);
		if($articles){
			echo json_encode(($articles));	
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
});


$app->get('/agenda/senado/ultimos/json/', function() use($app){
	$app->response()->header('Content-Type', 'application/json');
	try {
		$fecha=date('Y-m-d');
		$ultimos30=date('Y-m-d', strtotime('today - 30 days'));
		$q="SELECT 'S' AS camara,(id_preagenda) AS padre, id, texto, fecha_evento FROM agenda_senado WHERE fecha_evento<='$fecha' AND fecha_evento>='$ultimos30' ORDER BY fecha_evento DESC ";
		$articles = R::getAll($q);
		if($articles){
			echo json_encode(($articles));	
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
});


$app->get('/agenda/diputados/json/', function() use($app){
	$app->response()->header('Content-Type', 'application/json');
	try {
		$articles = R::find('agenda_diputados','ORDER BY fecha_evento DESC');
		if($articles){
			echo json_encode(R::exportAll($articles));	
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
});


$app->get('/agenda/diputados/(:id)/json/', function($id=1) use($app){
	$app->response()->header('Content-Type', 'application/json');
	try {		
		$article = R::findOne('agenda_diputados', 'id=?', array($id)); 
		if($article){
			echo json_encode(R::exportAll($article));	
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
});

$app->get('/D/(:id)/', function($id=1) use($app){
	try {		
		$article = R::findOne('agenda_diputados', 'id=?', array($id)); 
		if($article){
			$data['info']=R::exportAll($article);
			$orig = R::findOne('preagenda_diputados', 'id=?', array($data['info'][0]['id_preagenda'])); 
			$data['info']['orig']=R::exportAll($orig);
			$app->render('single.php',$data);
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
});

$app->get('/S/(:id)/', function($id=1) use($app){
	try {		
		$article = R::findOne('agenda_senado', 'id=?', array($id)); 
		if($article){
			$data['info']=R::exportAll($article);
			$orig = R::findOne('preagenda_senado', 'id=?', array($data['info'][0]['id_preagenda'])); 
			$data['info']['orig']=R::exportAll($orig);
			$app->render('single.php',$data);
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
});


$app->get('/agenda/senado/json/', function() use($app){
	$app->response()->header('Content-Type', 'application/json');
	try {
		$articles = R::find('agenda_senado','ORDER BY id DESC');
		if($articles){
			echo json_encode(R::exportAll($articles));	
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
});


$app->get('/agenda/senado/(:id)/json/', function($id=1) use($app){
	$app->response()->header('Content-Type', 'application/json');
	try {		
		$article = R::findOne('agenda_senado', 'id=?', array($id)); 
		if($article){
			echo json_encode(R::exportAll($article));	
		} else {
			throw new ResourceNotFoundException();
		}
	} catch (ResourceNotFoundException $e) {
		 $app->response()->status(404);
	} catch (Exception $e) {
		$app->response()->status(400);
		$app->response()->header('X-Status-Reason', $e->getMessage());
	} 
});


$app->run();
