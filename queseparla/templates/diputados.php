<?php include_once 'header.php'; ?>

	<div class="container">
		<div class="agenda-hoy">
			<div class="hoy">
				<h1>Hoy en Diputados</h1>
			</div>
			<div id="ahora">
				Sin contenido	
			</div>
			
			<!--  -->
			<div class="agenda-hoy">
			<h1>&Uacute;ltimos 30 d&iacute;as</h1>
			<div id="anteriores">
				Sin contenido
			</div>
			<!--  -->
			
			<!-- <div class="agenda-hoy">
				<h1>Temas tocados</h1>
				<ul>
					<li>
						<a href="">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Maiores, velit, obcaecati, illo nesciunt sint possimus distinctio architecto repellendus quibusdam id autem asperiores cupiditate quam</a>
					</li>
					<li><a href="">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Molestiae, ad ea sed maiores cumque molestias ipsum. Incidunt, magni, libero, hic atque quis officia magnam aut eligendi aperiam necessitatibus molestias similique.</a></li>
				</ul>
			</div> -->

	</div>

	<script>
		window.onload=function(){
			var source   = $("#template_agenda").html(); 
			var template = Handlebars.compile(source); 

			$.getJSON("//tedic.org/queseparla/agenda/diputados/proximos/json/",function(datos){
				var html=template(datos);
				$('#ahora').html(html);
				console.info('LISTO');
			});

			$.getJSON("//tedic.org/queseparla/agenda/diputados/ultimos/json/",function(datos){
				var html=template(datos);
				$('#anteriores').html(html);
				console.info('LISTO');
			});
			
			
		}
	</script>

<?php include_once 'footer.php'; ?>