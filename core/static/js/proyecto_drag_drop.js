var drag_source_element = null;
var esquemas_dias = [];
var bloques_horas = [];
var turnos_bloques_horas = [];
var esquemas_bloques = [];
var pks_dias = [];
var data_encuentros = {};
var data_aulas = {};
var data_aulas_encuentros = {};
var data_encuentro_modal_actual = {};

var drag_start_list = [];
var drag_source_element_real;

function mostrar_modal_error(mensaje){
	swal(mensaje, {
	  buttons: {
		  confirm: {
		    text: "OK",
		    value: true,
		    visible: true,
		    className: "",
		    closeModal: true
		  }
	  },
	  icon: "error",
	});




}

function ocultar_modal_error(){
	$('#modalError').removeClass('show').addClass('fade');
}


function mostrar_modal_confirmacion2(){
	// swal(
	// 	'Error en url',
	// 	{
	//        icon: "success",
	//     }
	// );

	swal('Ya existe otro encuentro en ese bloque horario en la misma aula. ¿Realmente desea compartir el aula en el mismo momento?', {
	  // buttons: ["Cancelar", "Aceptar"],
	  buttons: {
		  cancel: {
		    text: "Cancelar",
		    value: null,
		    visible: true,
		    closeModal: true,
		  },
		  confirm: {
		    text: "OK",
		    value: true,
		    visible: true,
		    className: "aceptar-choque-encuentros",
		    closeModal: true
		  }


	  },
	  icon: "warning",
	});

}

function ocultar_modal_confirmacion(){
	$('#modalConfirmacionAlerta').removeClass('show').addClass('fade');
}

function handleDragStart(e) {
  // Target (this) element is the source node.
  // this.style.opacity = '0.4';
  if($(this).attr('class') && $(this).attr('class').indexOf('dnd-encuentro') != -1){
  	drag_source_element = this;
  	drag_source_element_real = this;
  	// console.log('drag source element real', drag_source_element_real);
	  e.dataTransfer.effectAllowed = 'move';
	  // e.dataTransfer.setData('text/html', this.innerHTML);
	  e.dataTransfer.setData('text/html', this.outerHTML);
  }
  // console.log('drag_source_element', drag_source_element);
  drag_start_list.push(this);
}	

function handleDragOver(e) {
  if (e.preventDefault) {
    e.preventDefault(); // Necessary. Allows us to drop.
  }

  e.dataTransfer.dropEffect = 'move';  // See the section on the DataTransfer object.

  return false;
}

function handleDragEnter(e) {
  // this / e.target is the current hover target.
  this.classList.add('over');
}

function handleDragLeave(e) {
  this.classList.remove('over');  // this / e.target is previous target element.
}

function acciones_drop_permitido(e){

	var this_element = (e && e.target) || contenedor_drop;

    // se borra del html del anterior padre al bloque
    // drag_source_element.innerHTML = this.innerHTML;
    // $(drag_source_element.parentElement).find('[data-encuentro-dia-pk=' + $(drag_source_element).data('encuentro-dia-pk') + ']').remove()
    // this.innerHTML = e.dataTransfer.getData('text/html');
    // this.innerHTML = e.dataTransfer.getData('text/html');
    var encuentro_data = data_encuentros[Number($(drag_source_element_real).data('encuentro-dia-pk'))];
  	// console.log('drop function drag_source_element', drag_source_element);
    $.post('/api/encuentros/update/', {
    	pk: encuentro_data.encuentro_dia_pk,
    	hora_inicio: esquemas_bloques[$(this_element).data('hora')],
    	dia: pks_dias[$(this_element).data('dia')],
    	aula: aula_pk,
    });
    encuentro_data.bloque.hora_inicio = esquemas_bloques[$(this_element).data('hora')];
    encuentro_data.dia = esquemas_dias[$(this_element).data('dia')];
    encuentro_data.dia_pk = pks_dias[$(this_element).data('dia')];
  	var jquery_dse = $(drag_source_element_real);
  	// if(jquery_dse.attr('class') && jquery_dse.attr('class').indexOf('resultado-busqueda') !=-1 && jquery_dse.data('aula') == aula){
	// console.log('se limpia la tabla');
	function limpiar_y_llenar_tabla_con_validacion(){
		if($('.tabla-encuentros .dnd-encuentro').length != data_aulas_encuentros[aula].length){
			// limpiar_encuentros_tabla(tmp_callback);
			console.log('se vuelve a llenar tabla desde validacion!');
			limpiar_encuentros_tabla(limpiar_y_llenar_tabla_con_validacion);
		}
		// if(Boolean(data_aulas_encuentros[aula])){
		// 	llenar_encuentros(aula, function(){
		// 	});
		// }
	}
	limpiar_encuentros_tabla(limpiar_y_llenar_tabla_con_validacion);	
}


var contenedor_drop = null;
function handleDrop(e) {
  // this/e.target is current target element.
  this.classList.remove('over');  // this / e.target is previous target element.

  if (e.stopPropagation) {
    e.stopPropagation(); // Stops some browsers from redirecting.
  }

  // Don't do anything if dropping the same column we're dragging.
  if (drag_source_element_real && drag_source_element_real != this && !this.classList.contains('dnd-encuentro')) {


  	// se valida que hayan suficientes bloques disponibles para en el turno para mover el encuentro
  	var turno_disponible = true;
  	var indice_bloque_hora_final_abarcado = $(this).data('hora') + data_encuentros[$(drag_source_element).data('encuentro-dia-pk')].numero_bloques;
  	if(indice_bloque_hora_final_abarcado > turnos_bloques_horas.length){
  		turno_disponible = false;
  	} else {
	  	var turnos_a_ocupar = turnos_bloques_horas.slice($(this).data('hora'), indice_bloque_hora_final_abarcado)
	  	var turno_anterior = turnos_a_ocupar[0];
	  	for (var i = 1; i < turnos_a_ocupar.length; i++) {
	  		if(turnos_a_ocupar[i] != turno_anterior){
	  			turno_disponible = false;
	  		}
	  	};
  	}

  	if(turno_disponible){
	  	// @TODO: hacer validacion parecida a la de abajo, pero que se muestre el modal de advertencia si
	  	// el encuentro ocupa mas de un bloque y alguno de los bloques que desea ocupar esta ocupado por
	  	// otro encuentro



	  	// @TODO: (mostrar advertencia o no permitir, dependiendo de configuracion)
	  	if($(this).find('.dnd-encuentro').length){
	  		contenedor_drop = this;
	  		mostrar_modal_confirmacion2();
	  	} else {
	  		acciones_drop_permitido(e);
	  	}
  	} else {
  		mostrar_modal_error('No hay suficientes bloques disponibles en el turno para este encuentro.')
  	}
  }
  return false;
}

function handleDragEnd(e) {
  // this/e.target is the source node.
  // var cols = [e.target];
  // e.target.classList.remove('over');

  // [].forEach.call(cols, function (col) {
  //   col.classList.remove('over');
  // 	// col.style.opacity = '1';
  // });
}

function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}	


function asignar_handlers_drag_and_drop(){
	var cols = document.querySelectorAll('.dnd-encuentro');
	var cols2 = document.querySelectorAll('.tabla-encuentros td');
	cols2 = $(cols2).not('td:nth-child(1), td:nth-child(2)');
	var cols3 = document.querySelectorAll('#resultados_busqueda');

	var elements = Array.prototype.slice.call(cols);
	var elements2 = Array.prototype.slice.call(cols2);
	var elements3 = Array.prototype.slice.call(cols3);

	elements = elements.concat(elements2);
	elements = elements.concat(elements3);

	[].forEach.call(elements, function(col) {
	  col.addEventListener('dragstart', handleDragStart, false);
	  col.addEventListener('dragenter', handleDragEnter, false)
	  col.addEventListener('dragover', handleDragOver, false);
	  col.addEventListener('dragleave', handleDragLeave, false);
	  col.addEventListener('drop', handleDrop, false);
	  col.addEventListener('dragend', handleDragEnd, false);
	});

	$('.dnd-encuentro .icono-editar').click(function(){
		$('#creacionEdicionencuentroModal')[0].classList.remove('fade');
		$('#creacionEdicionencuentroModal')[0].classList.add('show');
		data_encuentro_modal_actual = data_encuentros[this.parentElement.parentElement.parentElement.getAttribute('data-encuentro-dia-pk')]
		$('#creacionEdicionencuentroModal [name=docente] option[value=' + data_encuentro_modal_actual.seccion.docente_pk + ']').attr('selected', true);
		$('#creacionEdicionencuentroModal [name=aula] option[value=' + data_encuentro_modal_actual.aula.pk + ']').attr('selected', true);
		$('#creacionEdicionencuentroModal [name=tipo] option[value=' + data_encuentro_modal_actual.tipo + ']').attr('selected', true);
		$('#creacionEdicionencuentroModal [name=cupo]').attr('value', data_encuentro_modal_actual.seccion.cupo);

	});	

}

function callWhenReady(selector, callback) {
    var self = this;
    if ($(selector).closest('body').length) {
        callback();
    } else {
        setTimeout(function () {
            self.callWhenReady(selector, callback);
        }, 1);
    }
}	

function obtener_datos_encuentros(callback){
	$.getJSON('/api/encuentros/?proyecto=' + proyecto, function(data){
		for (var i = 0; i < data.length; i++) {
			data_encuentros[data[i].encuentro_dia_pk] = data[i];
			data_aulas_encuentros[data[i].aula.nombre] = (data_aulas_encuentros[data[i].aula.nombre] || []).concat(data[i]);
			data_aulas_encuentros['aulas_en_orden'] = (data_aulas_encuentros['aulas_en_orden'] || []).concat(data[i]);

			if(data_aulas_encuentros['aulas_en_orden'].length > 1){
				data_aulas_encuentros['aulas_en_orden'].sort(
					function(a, b) {
					  var ele1 = a.aula.numero;
					  var ele2 = b.aula.numero;
					  var comparison = 0;
					  if (ele1 > ele2) {
					    comparison = 1;
					  } else if (ele1 < ele2) {
					    comparison = -1;
					  }
					  return comparison;
					}
				);
				
			}
		};
		callback();
	});
	$.getJSON('/api/aulas/?carrera=' + carrera, function(data_aulas_resp){
		data_aulas = data_aulas_resp;
	});	
}

function limpiar_encuentros_tabla(callback){
	// $('.tabla-encuentros .dnd-encuentro').remove().ready(callback);
	renderizar_tabla(callback);
}

function llenar_encuentros(aul, callback){
	var indice_bloques_dias = 0;
	var indice_bloques_horas = 0;
	if(Boolean(data_aulas_encuentros[aul])){
		for (var i = 0; i < data_aulas_encuentros[aul].length; i++) {
			var bloque_objetivo = null;
			// indice_bloques_dias = esquemas_dias.indexOf(data_aulas_encuentros[aul][i].dia) + 2;
			indice_bloques_dias = esquemas_dias.indexOf(data_aulas_encuentros[aul][i].dia);
			indice_bloques_horas = esquemas_bloques.indexOf(data_aulas_encuentros[aul][i].bloque.hora_inicio) + 1;
			// var selector_bloque_objetivo = '.tabla-encuentros tr:nth-child(' + indice_bloques_horas + ') td:nth-child(' + indice_bloques_dias + ')';
			var selector_bloque_objetivo = '.tabla-encuentros tr:nth-child(' + indice_bloques_horas + ') td[data-dia=' + indice_bloques_dias + ']';
			bloque_objetivo = $(selector_bloque_objetivo);
			if(!bloque_objetivo.length){
				selector_bloque_objetivo = '.tabla-encuentros tr td[data-dia=' + indice_bloques_dias + ']';
				bloque_objetivo = $(".tabla-encuentros tr td[data-dia=2]").slice(0, indice_bloques_horas - 1).last();
			}
			// console.log('bloque_objetivo', bloque_objetivo[0]);
				
				var nuevo_encuentro = $('<div>');
				nuevo_encuentro.attr('class', 'dnd-encuentro');
				nuevo_encuentro.attr('draggable', 'true');
				var titulo_encuentro  = $('<div>');
				titulo_encuentro.attr('class', 'titulo');
				var icono_editar_encuentro = $('<a>').attr('href', '#').attr('class', 'icono-editar').append($('<i>').attr('class', 'fa fa-pencil-square-o pull-right').attr('aria-hidden', 'true'));
				titulo_encuentro.append(icono_editar_encuentro);
				titulo_encuentro.append('<br>');
				var nombre_materia = $('<small>');
				nombre_materia.append($('<p>').text(data_aulas_encuentros[aul][i].seccion.materia.nombre));
				titulo_encuentro.append(nombre_materia);
				nuevo_encuentro.append(titulo_encuentro);
				var texto = $('<p>');
				texto.text('Sección: ' + data_aulas_encuentros[aul][i].seccion.numero);
				texto.append($('<br>'))
				texto.append($('<strong>').append(data_aulas_encuentros[aul][i].seccion.docente_nombre_apellido));
				texto.append($('<br>'));
				texto.append('Cupo: ' + data_aulas_encuentros[aul][i].seccion.cupo);
				nuevo_encuentro.append(texto);
				nuevo_encuentro.attr('data-encuentro-dia-pk', data_aulas_encuentros[aul][i].encuentro_dia_pk);
				// console.log('nuevo_encuentro', nuevo_encuentro[0]);
				bloque_objetivo.append(nuevo_encuentro);

				// @TODO: Hacer validaciones de numero de bloques de encuentro aqui
				var numero_bloques = data_aulas_encuentros[aul][i].numero_bloques;
				bloque_objetivo.attr('rowspan', numero_bloques);
				for (var ind_blo = indice_bloques_horas + 1; ind_blo <= esquemas_bloques.length && ind_blo < indice_bloques_horas + numero_bloques; ind_blo++) {
					// var selector_bloque_eliminar = '.tabla-encuentros tr:nth-child(' + ind_blo + ') td:nth-child(' + indice_bloques_dias + ')'
					var bloque_eliminar = $('.tabla-encuentros tr:nth-child(' + ind_blo + ') td[data-dia=' + indice_bloques_dias + ']');
					// console.log('se va a eliminar:', bloque_eliminar[0], 'en llenado de encuentros');
					bloque_eliminar.remove();
				};
			// })
		}
		if(callback){
			callback();
		}
		
	}
		
}

function renderizar_tabla(callback){
	// var tabla = $('.tabla-encuentros');
	tabla = $('<table>').attr('class', 'table table-bordered tabla-encuentros');
	// tabla.append($('<div>').attr('class', 'box-footer'));
	tabla_recien_creada = true
	var thead = $('<thead>');
	var tbody = $('<tbody>');
	thead.append($('<th>').attr('class', 'text-center').attr('colspan', '2').text('Horas'));
	for (var i = 0; i < esquemas_dias.length; i++) {
		thead.append($('<th>').text(esquemas_dias[i]).attr('class', 'text-center'));
	};
	var tmp_turno = turnos_bloques_horas[0];
	for (var i = 0; i < bloques_horas.length; i++) {
		var fila = $('<tr>');
		// fila.append($('<td>').append($('<strong>').text(bloques_horas[i])));
		fila.append($('<td>').attr('valign', 'center').attr('align', 'center').attr('class', 'bold').text(i + 1));
		fila.append($('<td>').attr('class', 'bold').html(bloques_horas[i].replace(' - ', '<br>')));	
		for (var j = 0; j < esquemas_dias.length; j++) {
			fila.append($('<td>').attr('data-hora', i).attr('data-dia', j));
		};
		if(tmp_turno != turnos_bloques_horas[i]){
			fila.attr('class', 'separador-turno');
		}
		tmp_turno = turnos_bloques_horas[i];
		tbody.append(fila);
	};
	// console.log(tabla);
	tabla.append(thead);
	tabla.append(tbody);
	$('div.tabla-encuentros-wrapper').html(tabla).ready(
		llenar_encuentros(aula, callback)
	).ready(
		asignar_handlers_drag_and_drop()
	)
}

$(document).ready(function(){
	tabla_recien_creada = false;
	obtener_datos_encuentros(function(){
		var tabla = $('.tabla-encuentros');
		if(!tabla.length){
			tabla = $('<table>').attr('class', 'table table-bordered tabla-encuentros');

			tabla_recien_creada = true
		}
		var thead = $('<thead>');
		var tbody = $('<tbody>');
		$.getJSON('/api/dias/?carrera=' + carrera, function(data){
			for (var i = 0; i < data.length; i++) {
				esquemas_dias.push(data[i].dia);
				pks_dias.push(data[i].numero);
			};
			$.getJSON('/api/bloques/?carrera=' + carrera, function(data_bloques){
				for (var i = 0; i < data_bloques.length; i++) {
					bloques_horas.push(data_bloques[i].representacion);
					turnos_bloques_horas.push(data_bloques[i].turno);
					esquemas_bloques.push(data_bloques[i].hora_inicio);
				};
				thead.append($('<th>').attr('class', 'text-center').attr('colspan', '2').text('Horas'));
				for (var i = 0; i < esquemas_dias.length; i++) {
					thead.append($('<th>').text(esquemas_dias[i]).attr('class', 'text-center'));
				};
				var tmp_turno = turnos_bloques_horas[0];
				for (var i = 0; i < bloques_horas.length; i++) {
					var fila = $('<tr>');
					// fila.append($('<td>').append($('<strong>').text(bloques_horas[i])));
					// fila.append($('<td>').attr('valign', 'center').attr('align', 'center').append($('<strong>').text(i + 1)));
					fila.append($('<td>').attr('valign', 'center').attr('align', 'center').attr('class', 'bold').text(i + 1));
					fila.append($('<td>').attr('class', 'bold').html(bloques_horas[i].replace(' - ', '<br>')));
					for (var j = 0; j < esquemas_dias.length; j++) {
						fila.append($('<td>').attr('data-hora', i).attr('data-dia', j));
					};
					if(tmp_turno != turnos_bloques_horas[i]){
						fila.attr('class', 'separador-turno');
					}
					tmp_turno = turnos_bloques_horas[i];
					tbody.append(fila);
				};
				// console.log(tabla);
				tabla.append(thead);
				tabla.append(tbody);
				// tabla.append($('<div>').attr('class', 'box-footer'));

				if(tabla_recien_creada){
					tabla_recien_creada = false;
					// var contenedor_tabla = $('<div>').attr('class', 'box-body').append(tabla)
					$('div.tabla-encuentros-wrapper').html(tabla).ready(
						llenar_encuentros(aula)
					).ready(
						asignar_handlers_drag_and_drop()
					);
				}
			});
		});
		if(data_aulas_encuentros['aulas_en_orden'] !== undefined && data_aulas_encuentros['aulas_en_orden'].length){
			$('.aula-actual').text(aula);
			llenar_encuentros(aula);
		}
	});

});

// ######## Eventos ##############


$('.aula-button').click(function(){
	aula = $(this).text();
	aula_pk = $(this).data('pk');
	$('.aula-actual').text(aula);
	limpiar_encuentros_tabla();
	// limpiar_encuentros_tabla(function(){
	// 	if(Boolean(data_aulas_encuentros[aula])){
	// 		llenar_encuentros(aula);
	// 	}
	// })
});

$('#busqueda_encuentro').click(function(){
	var materia = $('#busqueda_materia').val().toLowerCase();
	var seccion = $('#busqueda_seccion').val();
	if(materia && seccion){
		$('#resultados_busqueda').html('');
		if(data_aulas_encuentros['aulas_en_orden']){
			for (var i = data_aulas_encuentros['aulas_en_orden'].length - 1; i >= 0; i--) {
				if(data_aulas_encuentros['aulas_en_orden'][i].seccion.materia.nombre.toLowerCase().indexOf(materia) != -1){
					if(data_aulas_encuentros['aulas_en_orden'][i].seccion.numero == Number(seccion)){
						
						// var nuevo_encuentro  = $('<div>');
						// nuevo_encuentro.attr('class', 'dnd-encuentro resultado-busqueda');
						// nuevo_encuentro.attr('draggable', 'true');
						// var titulo_encuentro  = $('<div>');
						// titulo_encuentro.attr('class', 'titulo');
						// // titulo_encuentro.append($('<i class="fa fa-pencil-square-o" aria-hidden="true"></i>'))
						// // titulo_encuentro.append($('<strong>').text(data_aulas_encuentros['aulas_en_orden'][i].seccion.materia.nombre));
						// titulo_encuentro.append($('<i>').attr('class', 'fa fa-pencil-square-o icono-editar pull-right').attr('aria-hidden', 'true'));
						// nuevo_encuentro.append(titulo_encuentro);
						// var texto = $('<p>');
						// texto.text('Sección: ' + data_aulas_encuentros['aulas_en_orden'][i].seccion.numero)
						// texto.append($('<br>'))
						// texto.append($('<strong>').append(data_aulas_encuentros['aulas_en_orden'][i].seccion.docente_nombre_apellido))
						// texto.append($('<br>'))
						// texto.append('Cupo: ' + data_aulas_encuentros['aulas_en_orden'][i].seccion.cupo)
						// nuevo_encuentro.append(texto);
						// nuevo_encuentro.attr('data-aula', data_aulas_encuentros['aulas_en_orden'][i].aula.nombre);
						// // nuevo_encuentro.attr('data-encuentro-dia-pk', data[i].encuentro_dia_pk)
						// nuevo_encuentro.attr('data-encuentro-dia-pk', data_aulas_encuentros['aulas_en_orden'][i].encuentro_dia_pk);
						// nuevo_encuentro.attr('rowspan', data_aulas_encuentros['aulas_en_orden'][i].numero_bloques);
						// // console.log('se agrega res busqueda');


						var nuevo_encuentro = $('<div>');
						nuevo_encuentro.attr('class', 'dnd-encuentro');
						nuevo_encuentro.attr('draggable', 'true');
						var titulo_encuentro  = $('<div>');
						titulo_encuentro.attr('class', 'titulo');
						var icono_editar_encuentro = $('<a>').attr('href', '#').attr('class', 'icono-editar').append($('<i>').attr('class', 'fa fa-pencil-square-o pull-right').attr('aria-hidden', 'true'));
						titulo_encuentro.append(icono_editar_encuentro);
						titulo_encuentro.append('<br>');
						var nombre_materia = $('<small>');
						nombre_materia.append($('<p>').text(data_aulas_encuentros['aulas_en_orden'][i].seccion.materia.nombre));
						titulo_encuentro.append(nombre_materia);
						nuevo_encuentro.append(titulo_encuentro);
						var texto = $('<p>');
						texto.text('Sección: ' + data_aulas_encuentros['aulas_en_orden'][i].seccion.numero);
						texto.append($('<br>'))
						texto.append($('<strong>').append(data_aulas_encuentros['aulas_en_orden'][i].seccion.docente_nombre_apellido));
						texto.append($('<br>'));
						texto.append('Cupo: ' + data_aulas_encuentros['aulas_en_orden'][i].seccion.cupo);
						nuevo_encuentro.attr('data-aula', data_aulas_encuentros['aulas_en_orden'][i].aula.nombre);
						nuevo_encuentro.append(texto);
						nuevo_encuentro.attr('data-encuentro-dia-pk', data_aulas_encuentros['aulas_en_orden'][i].encuentro_dia_pk);
						nuevo_encuentro.attr('rowspan', data_aulas_encuentros['aulas_en_orden'][i].numero_bloques);

						$('#resultados_busqueda').append(nuevo_encuentro);
						asignar_handlers_drag_and_drop();
					}
				}
			};
		}
	}
});

$('#creacionEdicionencuentroModal .submit-modal').click(function(e){
	e.preventDefault();
	var anterior_aula = data_encuentro_modal_actual.aula;
	var aula_edicion_encuentro = $('#creacionEdicionencuentroModal [name=aula]').val();
	var nombre_aula_edicion = data_aulas[aula_edicion_encuentro].nombre;
	var docente = $('#creacionEdicionencuentroModal [name=docente]').val();
	var docente_nombre = $('#creacionEdicionencuentroModal [name=docente]').text();
	var tipo = $('#creacionEdicionencuentroModal [name=tipo]').val();
	var cupo = $('#creacionEdicionencuentroModal [name=cupo]').val();
	$.post('/api/encuentros/update/', {
		pk: data_encuentro_modal_actual.encuentro_dia_pk,
		aula: aula_edicion_encuentro,
		docente: docente,
		tipo: tipo,
		cupo: cupo,
	}).done(function(algo){
		$('#creacionEdicionencuentroModal')[0].classList.remove('show');	
		$('#creacionEdicionencuentroModal')[0].classList.add('fade');
		data_encuentro_modal_actual.aula = data_aulas[aula_edicion_encuentro];
		data_encuentro_modal_actual.seccion.docente.nombres = docente_nombre;
		data_encuentro_modal_actual.seccion.docente.pk = docente;
		data_encuentro_modal_actual.tipo = tipo;
		data_encuentro_modal_actual.seccion.cupo = cupo;
		for (var i = 0; i < data_aulas_encuentros[anterior_aula.nombre].length; i++) {
			if(data_aulas_encuentros[anterior_aula.nombre][i].encuentro_dia_pk == data_encuentro_modal_actual.encuentro_dia_pk){
				data_aulas_encuentros[nombre_aula_edicion] = (data_aulas_encuentros[nombre_aula_edicion] || []).concat(data_aulas_encuentros[anterior_aula.nombre][i]);
				data_aulas_encuentros[anterior_aula.nombre].splice(i, 1);
				break;
			}
		};
		renderizar_tabla();
		$('#busqueda_encuentro').click();
		
	});
});

$('body').on('click', '.aceptar-choque-encuentros', function(){
	console.log('acepto modal de confirmacion de alerta');
	acciones_drop_permitido();
});


$('#modalConfirmacionAlerta .cancelar').click(function(e){
	ocultar_modal_confirmacion();
});

$('#modalError .cancelar').click(function(e){
	ocultar_modal_error();
});

$('#reporte_aula').click(function(e){
	var url_vista = '/reporte/aula/' + proyecto + '/' + aula + '/';
	$.post(url_vista, {html_tabla: $('.tabla-encuentros')[0].outerHTML}).done(function(){
		document.location = url_vista;
	});
});

$('.eliminar-encuentro').click(function(){
	$.get('/encuentro/' + data_encuentro_modal_actual.encuentro_dia_pk + '/delete/').done(function(){
		delete data_encuentros[data_encuentro_modal_actual.pk];
		for (var i = data_aulas_encuentros[data_encuentro_modal_actual.aula.nombre].length - 1; i >= 0; i--) {
			if(data_aulas_encuentros[data_encuentro_modal_actual.aula.nombre][i].pk == data_encuentro_modal_actual.pk){
				data_aulas_encuentros[data_encuentro_modal_actual.aula.nombre].splice(i, 1);
			}
		};
		renderizar_tabla();
	})

});

$('#limpiar_resultados_busqueda').click(function(){
	$('#resultados_busqueda .dnd-encuentro').remove();
});


// $('.generar_reporte').on('change', function(e){
// 	if($(this).val() === "1"){
// 		var win = window.open('/reporte/semestres/' + proyecto + '/', '_blank');
// 		win.focus();		
// 	}
// });


// ###############################


