# Agenda acessível

## Informações
* Autores: Abel Passos, Ângelo Abrantes  e Rui Fontes
* atualizado em: 31 de Outubro de 2022 
* Baixar a [versão estável][1]
* Compatibilidade: NVDA versão 2019.3 e posteriores

## Apresentação
Este addon permite anotar  compromissos e atividades, periódicos ou não, com ou sem alarmes.
É possível utilizar duas agendas diferentes.
Para alternar entre elas, vá ao menu do NVDA, Preferências, Configurações, seção Agenda e escolha, na caixa combinada, a agenda que quer usar.
Se a segunda linha estiver vazia, use o botão "Selecionar ou adicionar uma pasta" para criar uma segunda agenda.
Se utilizar este botão com um caminho selecionado, a agenda será movida para o novo caminho, se nele não existir nenhuma. Se existir, será apenas mudado o caminho, as duas agendas serão preservadas, passando a ser utilizada a do novo caminho.
Ao iniciar  o NVDA, serão exibidos os compromissos para o dia atual e o dia seguinte. Este lembrete pode ser uma janela com a lista de todos os compromissos ou um lembrete com um diálogo e um alarme sonoro para os compromissos com alarme definido.
Esta opção pode ser configurada nas definições do adon.

## Comando para abrir a agenda
O comando para chamar o addon  é NVDA+F4.
É possível alterá-lo no diálogo "Definir comandos", na seção Agenda.

## Como funciona:
* Ao iniciar  o nvda , serão mostrados os compromissos do dia atual e do dia seguinte, casoesteja configurado para tal.
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


### Funções dos botões da janela principal e suas respectivas teclas de atalho:

* Adicionar (Alt+A): abre uma janela para registrar compromissos na data selecionada;
* Editar (Alt+E): abre uma janela para editar o compromisso selecionado;
* Remover (Alt+R): apaga o compromisso selecionado;
* Pesquisar (Alt+P ou Ctrl+F): abre uma janela para pesquisa de informações na agenda;
* sair (Alt+S): Fecha a janela.

### As funções de adicionar e editar são bastante semelhantes e, por este motivo, a janela que será descrita serve para ambas as funcionalidades.
A principal diferença é que, para editar, necessita ter selecionado, previamente, um compromisso a ser alterado.
Além disto, na função Editar, os dados do compromisso selecionado são apresentados na janela para modificação. Na opção Adicionar, a janela abre com a data selecionada e com os demais campos em branco. 

### Campos da janela Adicionar e Editar: 

* dia/mês/ano: campos da data que podem ser alterados com as setas verticais ou digitando o valor pretendido; 
* hora/minutos: campos da hora  que podem ser alterados com as setas verticais ou digitando o valor pretendido; 
* Descrição: campo para preenchimento das informações sobre o compromisso ;
* Botão Repetir (Alt+R): configurar a periodicidade do evento
* Botão Alarmes (Alt+A): ajustar os alarmes para o evento.
* Botão OK (Alt+O): registra na agenda as informações do compromisso; 
* Botão Cancelar (Alt+C): descarta informações preenchidas nesta janela. 
* A janela Adicionar/Editar possui a tecla de atalho Ctrl+Enter para guardar as informações preenchidas. Equivalente à função do botão OK. 

### Campos da janela "Configurar periodicidade"

Ao se pressionar o botão "Repetir" dentro da janela de adicionar ou editar, aparecerá uma janela para configurar a periodicidade do evento. Campos desta janela:
* Escolha a periodicidade do evento: uma lista de opções para ajustar a frequência que o evento deve ser repetido. O usuário pode escolher entre as seguintes opções: Nenhuma, Todos os dias, Toda semana, A cada 15 dias, Todo mês, A cada 2 meses, A cada 3 meses, A cada 4 meses, A cada 6 meses ou Todos os anos. 
> Nenhuma: indica que o evento não se repetirá;
Se a opção escolhida for "Nenhuma", indica que o evento não se repetirá.
* Marque para definir o encerramento da periodicidade: marcando esta opção, serão abertas opções para determinar quando a frequência do evento deve ser encerrada.
* Quantidade de repetições: assinale quantas vezes o evento deve se repetir. Ao ajustar a quantidade, a data de término é automaticamente ajustada.
* Data final: campos para ajustar a data na qual o evento se encerrará. Ao ajustar a data final, o campo  "Quantidade de repetições" será automaticamente ajustado.
#### Observações: 
1. O ajuste da periodicidade terá como referência a data configurada na janela adicionar/editar.
2. Ao ajustar a periodicidade de um evento, sua repetição acontecerá sempre após sua data inicial.
3. Os eventos mensais serão ajustados automaticamente para o último dia válido do mês corrente, caso a data inicial selecionada para o evento possua um valor no dia que seja superior. 
Exemplo: supondo que no dia 31 de  janeiro eu tenha criado um evento mensal. O dia 31 não existe no mês de fevereiro. Neste caso, o evento se ajustará automaticamente para o dia 28 ou 29, caso seja ano bissexto. Nos meses cujo valor  máximo do dia seja 30, como o mês de abril, o dia será automaticamente ajustado para o dia 30.
4. Se estiver editando um evento periódico e ajustar sua periodicidade para "Nenhuma", a repetição do evento deixará de existir, mas o evento original continuará existindo.

### Campos da janela "Configurar alarme"

Nesta janela o usuário poderá assinalar com que antecedência um alarme para o evento deve ser tocado. As opções de alarme possíveis são: Ajustar o alarme para o dia anterior, Ajustar o alarme para uma hora antes, Ajustar o alarme para meia hora antes, Ajustar o alarme para 15 minutos antes ou Ajustar o alarme para a hora exata.

### Campos da janela de pesquisa. 

* Tipo de pesquisa: deve selecionar entre as seguintes opções:
	* pesquisa por texto: será aberto um campo de edição para digitar o que deseja procurar. Não é necessário digitar a expressão completa, a pesquisa pode ser feita com partes de palavras;
	* Próximos 7 dias: mostra os compromissos para os próximos 7 dias, não incluindo o dia atual;
	* Próximos 30 dias: mostra os compromissos para os próximos 30 dias, não incluindo o dia atual;
	* Intervalo de datas: mostra os campos de data inicial e final para pesquisar;
* Botão Pesquisar (Alt+P): executa a pesquisa selecionada e retorna as informações encontradas;
* Botão Adicionar (Alt+A): A mesma função adicionar da janela principal. A diferença é que, se selecionou um compromisso, a janela para adicionar estará na data do compromisso selecionado. Se nenhum registro for selecionado, mostra a janela na data atual;
* Botão Editar (Alt+E): A mesma função editar da janela principal. Necessita que algum compromisso esteja selecionado;
* Remover (Alt+R): apaga o compromisso selecionado;
* Remover tudo (Alt+T): apaga todos os compromissos apresentados;
* Botão Cancelar  (Alt+C): fecha a janela de pesquisa e retorna à janela principal.

#### Observações:
1. Caso exista uma data de um evento periódico no período selecionado, sua periodicidade será mostrada. 
Exemplo: se um evento ocorrer diariamente, aparecerá antes da descrição do evento os dizeres "Todos os dias", indicando a frequência na qual o evento deve ocorrer.
2. Na pesquisa por texto, caso algum evento periódico seja mostrado, será a data  de origem do evento e não as suas datas posteriores.
Exemplo: se eu iniciei um evento com periodicidade diária na data de 3 de janeiro de 2022, se for feita uma pesquisa por texto e este evento for encontrado, as datas posteriores, como os dias 4, 5, 6 de janeiro, etc, não serão mostradas.
Este comportamento se deve ao fato de este tipo de pesquisa não ter uma data limite, tornando o cálculo de datas posteriores tendendo ao infinito.
3. Se for selecionado um evento dentre os encontrados por uma pesquisa que não seja por texto,  desejando editar ou remover este registro, o usuário será avisado se se tratar de um evento periódico. Caso o evento seja deste tipo, o usuário poderá editar ou remover apenas os registros que deram origem ao evento mostrado.
Exemplo: supondo que eu tenha criado um evento diário na data de 8 de fevereiro de 2022 e tenha feito uma pesquisa para os próximos 7 dias, este evento aparecerá todos os dias, resultando em 7 eventos, a partir da data atual. Se um destes eventos for selecionado para edição ou exclusão, aparecerá um aviso para o usuário indicando que esta ação deverá ser executada na data que originou o evento e toda alteração feita repercutirá em todas suas datas posteriores.

[1]: https://github.com/ruifontes/agenda-for-NVDA/releases/download/2022.10/agenda-2022.10.nvda-addon