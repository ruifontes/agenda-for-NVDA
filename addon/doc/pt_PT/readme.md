#Agenda


## Informações
* Autores: Abel Passos, Ângelo Abrantes  e Rui Fontes
* Actualizado em: 01.09.2023
* Descarregar [versão estável][1]
* Compatibilidade: NVDA versão 2019.3 e posteriores


## Apresentação
Este extra permite anotar  compromissos e actividades, com ou sem alarmes e com ou sem repetições periódicas.
É possível utilizar duas agendas diferentes.
Para alternar entre elas, vá ao menu do NVDA, Preferências, Configurações, secção Agenda e escolha, na caixa combinada, a agenda que quer usar.
Se a segunda linha estiver vazia, use o botão "Seleccionar ou adicionar um directório" para criar uma segunda agenda.
Se utilizar este botão com um caminho seleccionado, a agenda será movida para o novo caminho, se nele não existir nenhuma. Se existir, será apenas mudado o caminho, as duas agendas serão preservadas, passando a ser utilizada a do novo caminho.
No arranque do NVDA, seremos alertados para os compromissos para os próximos dias. Este lembrete pode ser uma janela com a lista de todos os compromissos ou um lembrete com um diálogo e um alarme sonoro para os compromissos com alarme definido.
Esta opção pode ser configurada nas definições do extra.
Também nas configurações do NVDA, secção Agenda, pode seleccionar os sons a serem usados, e também escolher entre o calendário gregoriano e o iraniano.


## Comando
O comando para chamar o extra é NVDA+F4.
É possível alterá-lo no diálogo "Definir comandos", na secção Agenda.


## Como funciona:
* Ao abrir o programa, serão mostrados os compromissos do dia actual.
* Na jannela principal, existem os campos para se alterar a data, os compromissos da data selecionada e alguns botões de controlo do programa que serão descritos adiante.
Os campos da data podem ser alterados usando as setas verticais ou digitando o valor pretendido. Ao alterar-se a data, os compromissos do dia serão automaticamente mostrados.


### Teclas de atalho da janela principal:


* Alt + 1-9: Avança a quantidade de dias correspondentes ao valor pressionado;
* Alt+0: Retorna à data atual;
* Alt+seta esquerda: Retrocede um dia na data;
* Alt+seta direita: Avança um dia na data;
* Alt+Seta acima: Avança uma semana;
* Alt+Seta abaixo: Retrocede uma semana;
* Alt+PageUp: Avança um mês;
* Alt+PageDown: Retrocede um mês;
* Enter: Se estiver seleccionado um compromisso, abre a janela de edição. Caso contrário, abre a janela para criar um novo compromisso;
* Delete: Apaga o registo selecionado. Mesma função do botão Remover;
* Control+F: Abre a janela de pesquisa. Equivalente a pressionar o botão "Pesquisar".


### Funções dos botões da janela principal e suas respectivas teclas aceleradoras:

* Adicionar (Alt+A): abre uma janela para registar compromissos na data seleccionada;
* Editar (Alt+E): abre uma janela para editar o compromisso seleccionado;
* Remover (Alt+R): apaga o compromisso seleccionado;
* Pesquisar (Alt+P): abre uma janela para pesquisa de informações na agenda;
* sair (Alt+S): Fecha a janela.


### As funções de adicionar e editar são bastante semelhantes e, por este motivo, a janela que será descrita serve para ambas as funcionalidades.
A principal diferença é que, para editar, necessita ter seleccionado, previamente, um compromisso a ser alterado.
Além disto, na função Editar, os dados do compromisso seleccionado são apresentados na janela para modificação. Na opção Adicionar, a janela abre com a data seleccionada e com os demais campos em branco. 


### Campos da janela Adicionar e Editar: 

* dia/mês/ano: campos da data que podem ser alterados com as setas verticais ou digitando o valor pretendido; 
* hora/minutos: campos da hora  que podem ser alterados com as setas verticais ou digitando o valor pretendido; 
* Descrição: campo para preenchimento das informações sobre o compromisso ;
* Botão Repetições: Acede à janela onde podemos seleccionar o a periodicidade das repetições e sua duração.
* Botão Alarmes: Acede a uma  janela onde encontramos  várias caixas de verificação para seleccionarmos os alarmes necessários. Por padrão, quando algum alarme for seleccionado com antecedência à data e hora do compromisso, automaticamente o alarme de hora exacta é activado.
* Botão OK (Alt+O): regista na agenda as informações do compromisso; 
* Botão Cancelar (Alt+C): não guarda as informações preenchidas nesta janela. 
* A janela Adicionar/Editar possui a tecla de atalho Ctrl+Enter para guardar as informações preenchidas. Equivalente à função do botão OK. 


### Campos da janela de pesquisa. 
* Tipo de pesquisa: deve seleccionar entre as seguintes opções:
<br>
	* pesquisa por texto: será aberto um campo de edição para digitar o que deseja procurar. Não é necessário digitar a expressão completa, a pesquisa pode ser feita com partes de palavras;
	* Próximos 7 dias: mostra os compromissos para os próximos 7 dias, não incluindo o dia actual;
	* Próximos 30 dias: mostra os compromissos para os próximos 30 dias, não incluindo o dia actual;
	* Intervalo de datas: mostra os campos de data inicial e final para pesquisar;
<br>
* Botão Pesquisar (Alt+P): executa a pesquisa seleccionada e retorna as informações encontradas;
* Botão Adicionar (Alt+A): A mesma função adicionar da janela principal. A diferença é que, se seleccionou um compromisso, a janela para adicionar estará na data do compromisso seleccionado. Se nenhum registo for seleccionado, mostra a janela na data actual;
* Botão Editar (Alt+E): A mesma função editar da janela principal. Necessita que algum compromisso esteja seleccionado;
* Remover (Alt+R): apaga o compromisso seleccionado;
* Remover tudo (Alt+T): apaga todos os compromissos apresentados;
* Botão Cancelar  (Alt+C): fecha a janela de pesquisa e retorna à janela principal.

[1]: https://github.com/ruifontes/agenda-for-NVDA/releases/download/2023.09.25/agenda-2023.09.25.nvda-addon
