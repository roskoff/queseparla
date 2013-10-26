<?php include_once 'header.php'; ?>

	<div class="container">
		<div class="agenda-hoy">
			<!-- <pre>
				<?php //print_r($info); ?>
			</pre> -->

			<h4><?php echo $info[0]['fecha_evento']; ?></h4>
			<h3><?php echo $info[0]['texto']; ?></h3>

			<hr>
			<h2>Agenda del dia</h2>
			<p>
				<?php echo $info['orig'][0]['html']; ?>
			</p>
		</div>

	</div>

<?php include_once 'footer.php'; ?>