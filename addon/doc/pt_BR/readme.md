#Agenda

<br>
## Informações
* Autores: Abel Passos, Ângelo Abrantes  e Rui Fontes
* atualizado em: 20 de Abril de 2022 
* Baixar a [versão estável][1]
* Compatibilidade: NVDA versão 2019.3 e posteriores

<br>
## Apresentação
Este addon permite anotar  compromissos e atividades, com ou sem alarmes.
É possível utilizar duas agendas diferentes.
Para alternar entre elas, vá ao menu do NVDA, Preferências, Configurações, seção Agenda e escolha, na caixa combinada, a agenda que quer usar.
Se a segunda linha estiver vazia, use o botão "Selecionar ou adicionar um diretório" para criar uma segunda agenda.
Se utilizar este botão com um caminho selecionado, a agenda será movida para o novo caminho, se nele não existir nenhuma. Se existir, será apenas mudado o caminho, as duas agendas serão preservadas, passando a ser utilizada a do novo caminho.
Ao iniciar  o NVDA, serão exibidos os compromissos para o dia atual e o dia seguinte. Este lembrete pode ser uma janela com a lista de todos os compromissos ou um lembrete com um diálogo e um alarme sonoro para os compromissos com alarme definido.
Esta opção pode ser configurada nas definições do adon.

<br>
## Comando para abrir a agenda
O comando para chamar o addon  é NVDA+F4.
É possível alterá-lo no diálogo "Definir comandos", na seção Agenda.

<br>
## Como funciona:
* Ao iniciar  o nvda , serão mostrados os compromissos do dia atual e do dia seguinte.
* Na jannela principal, existem os campos para se alterar a data, os compromissos da data selecionada e alguns botões de controle do programa que serão descritos adiante.
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
* Enter: Se estiver selecionado um compromisso, abre a janela de edição. Caso contrário, abre a janela para criar um novo compromisso;
* Delete: apaga o registro selecionado. Mesma função do botão Remover;
* Ctrl+F: abre a janela de pesquisa. Mesma função do botão Pesquisar.


### Funções dos botões da janela principal e suas respectivas teclas aceleradoras:

* Adicionar (Alt+A): abre uma janela para registrar compromissos na data selecionada;
* Editar (Alt+E): abre uma janela para editar o compromisso selecionado;
* Remover (Alt+R): apaga o compromisso selecionado;
* Pesquisar (Alt+P): abre uma janela para pesquisa de informações na agenda;
* sair (Alt+S): Fecha a janela.

### As funções de adicionar e editar são bastante semelhantes e, por este motivo, a janela que será descrita serve para ambas as funcionalidades.
A principal diferença é que, para editar, necessita ter selecionado, previamente, um compromisso a ser alterado.
Além disto, na função Editar, os dados do compromisso selecionado são apresentados na janela para modificação. Na opção Adicionar, a janela abre com a data selecionada e com os demais campos em branco. 

### Campos da janela Adicionar e Editar: 

* dia/mês/ano: campos da data que podem ser alterados com as setas verticais ou digitando o valor pretendido; 
* hora/minutos: campos da hora  que podem ser alterados com as setas verticais ou digitando o valor pretendido; 
* Descrição: campo para preenchimento das informações sobre o compromisso ;
* Alarmes: caixas de verificação que devem ser marcadas conforme a necessidade. Por padrão, quando algum alarme for selecionado com antecedência à data e hora do compromisso, automaticamente o alarme de hora exata é ativado. 
* Botão OK (Alt+O): registra na agenda as informações do compromisso; 
* Botão Cancelar (Alt+C): descarta informações preenchidas nesta janela. 
* A janela Adicionar/Editar possui a tecla de atalho Ctrl+Enter para guardar as informações preenchidas. Equivalente à função do botão OK. 

<br>
### Campos da janela de pesquisa. 
* Tipo de pesquisa: deve selecionar entre as seguintes opções:
<br>
	* pesquisa por texto: será aberto um campo de edição para digitar o que deseja procurar. Não é necessário digitar a expressão completa, a pesquisa pode ser feita com partes de palavras;
	* Próximos 7 dias: mostra os compromissos para os próximos 7 dias, não incluindo o dia atual;
	* Próximos 30 dias: mostra os compromissos para os próximos 30 dias, não incluindo o dia atual;
	* Intervalo de datas: mostra os campos de data inicial e final para pesquisar;
<br>
* Botão Pesquisar (Alt+P): executa a pesquisa selecionada e retorna as informações encontradas;
* Botão Adicionar (Alt+A): A mesma função adicionar da janela principal. A diferença é que, se selecionou um compromisso, a janela para adicionar estará na data do compromisso selecionado. Se nenhum registro for selecionado, mostra a janela na data atual;
* Botão Editar (Alt+E): A mesma função editar da janela principal. Necessita que algum compromisso esteja selecionado;
* Remover (Alt+R): apaga o compromisso selecionado;
* Remover tudo (Alt+T): apaga todos os compromissos apresentados;
* Botão Cancelar  (Alt+C): fecha a janela de pesquisa e retorna à janela principal.

