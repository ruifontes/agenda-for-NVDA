#Agenda


## Información
* Autores: Abel Passos, Ângelo Abrantes y Rui Fontes
* Actualizado: 01.09.2023
* Descargar [versión estable][1]
* Compatibilidad: NVDA versión 2019.3 en adelante


## Presentación
Este complemento permite anotar citas y actividades, que pueden tener alarmas y ser periódicas.
Puedes usar dos agendas diferentes.
Para alternar entre ellas, ve al menú NVDA, Preferencias, Opciones, sección Agenda, y elige en el cuadro combinado la agenda que quieres usar.
Si la segunda línea está vacía, usa el botón \"Seleccionar o añadir un directorio\" para crear una segunda agenda.
Si usas este botón con una agenda seleccionada, la agenda se moverá a la nueva ruta, si no hay agenda en ella. Si la hay, sólo cambiará la ruta, y se conservarán ambas agendas usando la nueva ruta.
Al arrancar NVDA se te recordarán las citas de los próximos días. Este recordatorio puede ser una ventana con una lista con todas las citas, o un recordatorio con una alarma sonora y un diálogo para las citas con alarma.
Este ajuste se puede configurar en las opciones del complemento.


## Orden
La orden para invocar el complemento es NVDA+f4.
Puedes cambiarla desde el diálogo Gestos de entrada, en la sección Agenda.


## Cómo funciona:
* Al abrir el programa, se mostrarán las citas de hoy.
* En la ventana principal hay campos para cambiar la fecha, las citas de la fecha seleccionada, y algunos botones de control que se describirán más adelante.
Se pueden modificar los campos de fecha usando las flechas arriba y abajo o tecleando el valor deseado. Al cambiar la fecha, se mostrarán automáticamente las citas de ese día.


### Atajos de teclado en la ventana principal:


* Alt + 1-9: adelanta varios días según el número pulsado;
* Alt+0: vuelve a la fecha actual;
* Alt+flecha izquierda: retrocede un día en la fecha;
* Alt+flecha derecha: avanza un día en la fecha;
* Alt+flecha arriba: avanza una semana;
* Alt+flecha abajo: retrocede una semana;
* Alt+retroceso de página: avanza un mes;
* Alt+avance página: retrocede un mes;
* Intro: si hay una cita seleccionada, abre la ventana de edición. Si no, abre una ventana para crear una nueva cita;
* Suprimir: elimina el registro seleccionado, al igual que el botón Eliminar;
* Control+f: abre la ventana «Buscar». Lo mismo que pasa al activar el botón "Buscar".


### Funciones de los botones de la ventana principal y teclas aceleradoras de los mismos:
* Añadir (Alt+A): Abre una ventana para registrar citas en la fecha seleccionada;
* Editar (Alt+E): Abre una ventana para editar la cita seleccionada;
* Eliminar (Alt+R): Elimina la cita seleccionada;
* Buscar (Alt+B): Abre una ventana para buscar información en la agenda;
* Salir (Alt+A): Cierra la ventana.


### Las funciones de añadir y editar son muy similares, y por ello la ventana que se describe sirve para ambos propósitos.
La principal diferencia es que para editar, debe haber una cita previamente seleccionada.
Además, se muestra la información de la cita para modificarla. Al añadir una cita, la fecha y otros campos aparecen en blanco.


### Añadir y editar campos de ventana:
* día/mes/año: campos de fecha que se pueden cambiar con flechas arriba y abajo o tecleando el valor deseado;
* hora/minutos: campos de hora que se pueden cambiar con las flechas arriba y abajo o tecleando el valor deseado;
* Description: campo para rellenar con información de la cita;
* Botón Repetir: permite acceder a la ventana de configurar periodicidad, donde se puede definir el periodo de repetición y cuándo finalizará.
* Alarmas: permite acceder a la ventana de "Configuración de alarmas", donde hay varias casillas de verificación para elegir cuándo disparar la alarma. Por defecto, cuando se seleccione una alarma antes de la fecha y hora de la cita, se activa automáticamente la alarma en la hora exacta.
* Botón Aceptar (Alt+A): introduce la información de la cita en el calendario.
* Botón Cancelar (Alt+C): no guarda la información introducida en esta ventana.
* La ventana de añadir o editar dispone del atajo control+intro para guardar la información introducida. Esto es equivalente a la función del botón Aceptar


### Campos de la ventana de búsqueda
* Tipo de búsqueda: debes elegir entre las siguientes opciones:

	* Búsqueda de texto: se abrirá un cuadro de edición para escribir lo que quieres buscar. No es necesario escribir frases completas, se puede hacer la búsqueda con partes de palabras;
	* Próximos 7 días: muestra las citas de los próximos 7 días, sin incluir el día actual;
	* Próximos 30 días: muestra las citas de los próximos 30 días, sin incluir el día actual;
	* Rango de fechas: muestra los campos de fecha de inicio y fecha de finalización para buscar;

* Botón Buscar (Alt+B): ejecuta la búsqueda seleccionada y devuelve la información encontrada;
* Botón Añadir (Alt+A): la misma función de añadir de la ventana principal. La diferencia es que si hay una cita seleccionada, se rellenará la fecha con la de esa cita. Si no se selecciona ninguna cita, se mostrará el día de hoy;
* Botón Editar (Alt+E): misma función que en la ventana principal. Debe haber una cita seleccionada;
* Botón Eliminar (Alt+R): elimina la cita seleccionada;
* Botón Eliminar todo (Alt+T): elimina todas las citas mostradas;
* Botón Cancelar (Alt+C): cierra la ventana de búsqueda y regresa a la ventana principal.

[1]: https://github.com/ruifontes/agenda-for-NVDA/releases/download/2023.09.25/agenda-2023.09.25.nvda-addon
