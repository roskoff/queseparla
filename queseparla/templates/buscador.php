<?php include_once 'header.php'; ?>

	<div class="container">
		<div class="agenda-hoy">
			<div class="hoy">
				<h1>Resultados encontrador para "<?php echo htmlentities($palabra);?>"</h1>
			</div>
			<div id="resultados">
				<?php if(count($info)<1){
					echo "Contenido no encontrado.";
				} else { ?>
					<ul class="lista-temas">
						<?php foreach ($info as $key => $value) { ?>
							<li>
								<small><?php echo $value['fecha_evento']; ?></small>
								<br>
								<a href="/queseparla/<?php echo $value['camara']; ?>/<?php echo $value['id']; ?>">

									<strong class="badge"><?php echo $value['camara']; ?></strong>
									<?php echo $value['texto']; ?>
								</a>
							</li>	
						<?php } ?>
					</ul>
				<?php } ?>
			</div>
	</div>


<?php include_once 'footer.php'; ?>