<!DOCTYPE html>
<html>
  <head>
    <title>Qu&eacute; se parla?</title>
    <meta charset=utf-8>
    <meta name=description content="">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.0.0-rc2/css/bootstrap.min.css">

    <link rel="stylesheet" href="/queseparla/css/main.css">
    

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="../../assets/js/html5shiv.js"></script>
      <script src="../../assets/js/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <nav class="navbar navbar-default navbar-static-top" role="navigation">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="/queseparla/">
        <img src="/queseparla/img/queseparla.png" alt="">
      </a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse navbar-ex1-collapse">
      <!-- <ul class="nav navbar-nav">
        <li>
          <a href="#" class="dropdown-toggle" data-toggle="dropdown">Temas <b class="caret"></b></a>
          <ul class="dropdown-menu">
            <li><a href="#">Tema 1</a></li>
            <li><a href="#">Tema 2</a></li>
            <li><a href="#">Tema 3</a></li>
          </ul>
        </li>
      </ul> -->
      <form action="/queseparla/buscar/" class="navbar-form navbar-left" role="search" method="post">
        <div class="form-group">
          <input type="text" name="palabra" class="form-control" placeholder="Buscar">
        </div>
        <button type="submit" class="btn btn-default">Buscar</button>
      </form>
     

    </div><!-- /.navbar-collapse -->
    <ul class="nav navbar-nav nav-congresistas">
      <li><a href="http://tedic.org/queseparla/senado">Senadores</a></li><!-- 
      --><li><a href="http://tedic.org/queseparla/diputados">Diputados</a></li>
    </ul>
  </nav>