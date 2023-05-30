#Agenda


## Información
* Autores: Abel Passos, Ângelo Abrantes y Rui Fontes
* Actualizado: mayo 30, 2023
* Descargar [versión estable][1]
* Compatibilidad: NVDA versión 2019.3 y posteriores

<br>
## Presentación
Este extra permite anotar anotaciones y actividades, con o sin alarmas y con o sin repeticiones periódicas.
Puedes usar dos agendas diferentes.
Para cambiar entre ellas, vaya al menú NVDA, Preferencias, Configuración, sección agenda y elija, en el cuadro combinado, el agenda que desea usar.
Si la segunda fila está vacía, use el botón "Seleccionar o agregar un directorio" para crear una segunda agenda.
Si utiliza este botón con una ruta seleccionada, la programación se moverá a la nueva ruta si no existe ninguna. Si existe, solo se cambiará el camino, se conservarán las dos agendas, comenzando a usarse la del nuevo camino.
En el lanzamiento de NVDA, seremos alertados de los compromisos para los próximos días. Este recordatorio puede ser una ventana con la lista de todas las anotaciones o un recordatorio con un diálogo y una alarma audible para anotaciones con una alarma configurada.
Esta opción se puede configurar en la configuración del complemento.

<br>
## Comando
El comando para llamar al extra es NVDA+F4.
Puede cambiarlo en el cuadro de diálogo "Establecer comandos" en la sección Programación.

<br>
## Cómo funciona:
* Cuando abra el programa, se le mostrarán las anotaciones del día actual.
* En la ventana principal, están los campos para cambiar la fecha, los compromisos de la fecha seleccionada y algunos botones de control del programa que se describirán a continuación.
Los campos de fecha se pueden cambiar mediante las flechas verticales o escribiendo el valor deseado. Cuando cambie la fecha, las anotaciones del día se mostrarán automáticamente.


### Teclas de atajo de la ventana principal:


* Alt + 1-9: Adelanta el número de días correspondientes al valor pulsado;
* Alt+0: Vuelve a la fecha actual;
* Alt + flecha izquierda: Rebobina la fecha un día;
* Alt + flecha derecha: Avanza un día en la fecha;
* Alt + Flecha hacia arriba: avance rápido una semana;
* Alt + Flecha a bajo: Retrocede una semana;
* Alt + PageUp: Adelanta un mes;
* Alt + PageDown: Se remonta a un mes;
* Entrar: Si se selecciona una anotación, se abre la ventana de edición. De lo contrario, abre la ventana para crear una nueva anotación;
* Eliminar: Elimina el registro seleccionado. La misma función que el botón Eliminar;
* Control+F: Abre la ventana de búsqueda. Equivalente a pulsar el botón "Buscar".


### Funciones de los botones de la ventana principal y sus respectivas teclas de aceleración:

* Agregar (Alt+A): abre una ventana para registrar anotaciones en la fecha seleccionada;
* Editar (Alt+E): abre una ventana para editar la anotación seleccionada;
* Eliminar (Alt+R): elimina la anotación seleccionada;
* Buscar (Alt+P): abre una ventana para buscar información en la agenda;
* exit (Alt+S): Cierra la ventana.

### Las funciones de añadir y editar son bastante similares y, por este motivo, la ventana que se describirá sirve para ambas funcionalidades.
La principal diferencia es que para editar, debe haber seleccionado previamente un compromiso para cambiar.
Además, en la función Editar, los datos de la anotación seleccionada se muestran en la ventana para su modificación. En la opción Agregar, se abre la ventana con la fecha seleccionada y los demás campos en blanco. 

### Agregar y editar campos de ventana: 

* día/mes/año: campos de fecha que se pueden cambiar con las flechas verticales o escribiendo el valor deseado; 
* hora/minutos: campos de tiempo que se pueden cambiar con las flechas verticales o escribiendo el valor deseado; 
* Descripción: campo para rellenar la información sobre el compromiso;
* Botón de repeticiones: Accedemos a la ventana donde podemos seleccionar la periodicidad de las repeticiones y su duración.
* Botón de alarmas: Accedemos a una ventana donde encontramos varias casillas de verificación para seleccionar las alarmas necesarias. De forma predeterminada, cuando se selecciona cualquier alarma antes de la fecha y hora de la anotación, la alarma de hora exacta se activa automáticamente.
* Botón OK (Alt + O): registra la información de la anotación en la agenda; 
* Botón Cancelar (Alt+C): no guarda la información rellenada en esta ventana. 
* La ventana Agregar / Editar tiene la tecla de método abreviado Ctrl + Enter para guardar la información completada. Equivalente a la función del botón OK. 

<br>
### Campos de la ventana de búsqueda. 
* Tipo de búsqueda: debe seleccionar entre las siguientes opciones:
<br>
	* Búsqueda de texto: se abrirá un campo de edición para escribir lo que desea buscar. No es necesario escribir la expresión completa, la búsqueda se puede hacer con partes de palabras;
\t* Próximos 7 días: muestra los compromisos para los próximos 7 días, sin incluir el día actual;
\t* Próximos 30 días: muestra los compromisos para los próximos 30 días, sin incluir el día actual;
\t* Rango de fechas: muestra los campos de fecha de inicio y finalización para buscar;
<br>
* Botón de búsqueda (Alt + P): ejecuta la búsqueda seleccionada y devuelve la información encontrada;
* Botón Agregar (Alt + A): La misma función agregar desde la ventana principal. La diferencia es que si seleccionó una anotación, la ventana para agregar será en la fecha de la anotación seleccionada. Si no se selecciona ningún registro, la ventana aparece en la fecha actual;
* Botón Editar (Alt+E): La misma función de edición que la ventana principal. Necesitas cierto compromiso para ser seleccionado;
* Eliminar (Alt+R): elimina la anotación seleccionada;
* Eliminar todo (Alt + T): elimina todas las anotaciones mostradas;
* Botón Cancelar (Alt+C): cierra la ventana de búsqueda y vuelve a la ventana principal.

[1]: https://github.com/ruifontes/agenda-for-NVDA/releases/download/2023.06.00/agenda-2023.06.00.nvda-addon
