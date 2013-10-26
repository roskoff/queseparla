<?php 
date_default_timezone_set('America/Asuncion');



function qseparla_loger($str){

	if(is_array($str) || is_object($str)){
		$str=print_r($str,true);
	}
	$archivolog='./leslogs/'.(date("Y/m/d"));
	if(!is_dir($archivolog)){
		mkdir($archivolog,0775,true);
	}
	$archivolog=$archivolog."/LOG-".(date("Y-m-d")).".log";
	$contenido="\n------------------------------------------------------------------------------------------------------------------------\n";
	$contenido.=date("Y-m-d H:i:s");
	$contenido.="\n".$str;
	$contenido.="\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n";
	file_put_contents($archivolog, $contenido, FILE_APPEND);
	return true;
}
