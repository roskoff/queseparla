		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
		<script src="//code.jquery.com/jquery.js"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="/queseparla/js/bootstrap.min.js"></script>
		<script src="//cdnjs.cloudflare.com/ajax/libs/handlebars.js/1.0.0/handlebars.min.js"></script>


		<script id="template_agenda" type="text/x-handlebars-template">

			<ul class="lista-temas">
				{{#each this}}
					<li>
						<small>{{this.fecha_evento}}</small>
						<br>
						<a href="/queseparla/{{this.camara}}/{{this.id}}">

							<strong class="badge">{{this.camara}}</strong>
							{{this.texto}}
						</a>
					</li>	
				{{/each}}
				
			</ul>

		</script>

	</body>
</html>
