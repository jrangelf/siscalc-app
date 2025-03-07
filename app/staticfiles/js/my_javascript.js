'use strict';

function recalcula()
{
  	


    let dt_corrente;   
    let novo_fator;
    let fator_corrente;
    let novo_indice;
    let str_novo_indice;

    let dt_atualiza = document.getElementById("dtatua").value;
    let str_tamanho = document.getElementById("qtde_linhas").innerHTML;
    let tamanho = parseInt(str_tamanho)-1;
    //console.log("tamanho: " + tamanho);

    // buscar o novo fator    
    for (let i = 0; i <= tamanho; i++) {

        dt_corrente = document.getElementById("a"+i).innerHTML;
                
        if (dt_atualiza == dt_corrente) {
            novo_fator = document.getElementById("e"+i).innerHTML;
            novo_fator = parseFloat(novo_fator.replace(",","."));
        }        
    }
    
    //alert("RECALCULAR OS ÍNDICES \n" + "Nova data atualização: " + dt_atualiza + "\n" +
    //      "Novo fator: " + novo_fator + "\n" );

    for (let i = 0; i <= tamanho ; i++){
        
        fator_corrente = document.getElementById("e"+i).innerHTML;
        fator_corrente = parseFloat(fator_corrente.replace(",","."));
        //console.log(fator_corrente);        
        
        novo_indice = novo_fator / fator_corrente;
        novo_indice = novo_indice.toFixed(10); 
        //console.log(novo_indice);
        
        str_novo_indice = novo_indice.toString();
        str_novo_indice = str_novo_indice.replace(".",",");        
        document.getElementById("f"+i).innerHTML= str_novo_indice; //novo_indice.toFixed(10);
    }
      	
}

function inabcampo2()
{
	//alert("selecionou campo1!");
	//alert(document.getElementById("campo2").value)		
	document.getElementById("campo2").value = "";
}

function valida1()
{
	dt1=document.getElementById("dtenvio").value;
	dt2=document.getElementById("dtadvoga").value;
	if (dt1 > dt2)
	{
	    document.getElementById("dtadvoga").value = "";
	}
}

function valida2()
{
	dt1=document.getElementById("dtenvio").value;
	dt2=document.getElementById("dtsaida").value;
	if (dt1 > dt2)
	{
	    document.getElementById("dtsaida").value = "";
	}
}	

function noback()
{
	javascript:window.history.forward(1);	
}					


function atualizaRelogio() {
    console.log("Rotina do relógio");
    var momentoAtual = new Date();
    var vhora = momentoAtual.getHours();
    var vminuto = momentoAtual.getMinutes();
    var vsegundo = momentoAtual.getSeconds();

	now = new Date;
    dayName = new Array("Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado")
    monName = new Array("janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro")
    let data = dayName[now.getDay()] + ", " + now.getDate() + " de " + monName[now.getMonth()] + " de " + now.getFullYear();
    document.getElementById("localdata").innerHTML = data;


    if (vhora < 10) {
        vhora = "0" + vhora;
    }
    if (vminuto < 10) {
        vminuto = "0" + vminuto;
    }
    if (vsegundo < 10) {
        vsegundo = "0" + vsegundo;
    }
    horaFormat = "  [" + vhora + ":" + vminuto + ":" + vsegundo + "]";
    document.getElementById("hora").innerHTML = horaFormat;
    setTimeout("atualizaRelogio()", 1000);
}

function enviarTabela() {
    // Obtendo os valores dos campos
      const dataInicial = document.getElementById('campo1').value;
      const dataFinal = document.getElementById('campo2').value;
      const radios = document.getElementsByName('radio');
      let formatoSelecionado = null;
      // Verifica qual rádio foi selecionado
      for (const radio of radios) {
          if (radio.checked) {
              formatoSelecionado = radio.value;
              break;
          }
      }
      // Validações
      if (!dataInicial || !dataFinal) {
          alert("Por favor, preencha todas as datas.");
          return;
      }
      if (dataInicial > dataFinal) {
          alert("A data inicial não pode ser maior que a data final.");
          return;
      }
      if (!formatoSelecionado) {
          alert("Por favor, selecione um formato (PDF ou Excel).");
          return;
      }
      // Captura o conteúdo HTML da tabela
      const tabelaHTML = document.querySelector('table.table').outerHTML;      
      // Coloca o HTML no campo oculto do formulário
      document.getElementById('html_content').value = tabelaHTML;      
      // Submete o formulário
      document.getElementById('form-relatorio').submit();  
    }