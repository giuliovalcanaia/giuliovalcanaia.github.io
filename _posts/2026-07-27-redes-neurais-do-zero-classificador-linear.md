---
title: "Redes Neurais do Zero: Classificador Linear"
date: 2026-07-27 10:00:00 -0300
math: true
---

# Programação Tradicional vs Aprendizado de Máquina

1. Antes de mais nada é importante traçar uma divisória bem clara para separar as duas coisas: Uma rede neural (inteligência artificial) não é um algoritmo "inteligente" cheio de condicionais. São duas formas diferentes (desde a sua concepção) de interpretar e solucionar problemas. 
	- *Programação tradicional*: Você escreve regras -> entra com dados = sai a resposta
	- *Machine Learning*: Você entra com dados -> entra com as respostas = o algoritmo *"aprende"* (calcula) as regras de forma autônoma. 
	
2. Tudo são vetores: para uma rede neural, não importa se ela apenas classifica fotos de gatos, ou processa textos extremamente densos, tudo o que entra nela é, em última análise, um vetor. 

# Situação problema: diabetes
Para começar a pensar sobre redes neurais, tomemos a seguinte situação:
Por meio de uma [pesquisa](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database), um grupo de 752 pessoas tiveram, dentre outras coisas, duas informações aferidas:
- Nível de glicose no sangue (mg/dL) - eixo $x$
- Índice de Massa Corporal (IMC) - eixo $y$ 

Desta forma, cada pessoa é inserida em um plano cartesiano por meio de um par de coordenadas $x, y$. Além disso, cada ponto possui uma cor associada a uma informação verdadeira:
- Azul: Paciente não diabético
- Vermelho: Paciente diabético

Veja abaixo o gráfico interativo com os dados reais da pesquisa. É possível aplicar zoom, mover o gráfico e passar o mouse sobre os pontos para ver os detalhes de cada paciente.

<iframe src="/assets/plots/diabetes_scatter.html" width="100%" height="620px" style="border:none; display:block; margin: 1.5em auto;"></iframe>

Não é preciso fazer uma análise matemática profunda para perceber que existe um certo padrão entre esse dois dados. Talvez, não de forma exata, seria possível traçar uma reta que tentasse separar, mesmo que grosseiramente, a maioria dos pontos azuis, da maioria dos pontos vermelhos, para assim criar uma regra algébrica de validação. Algo como, os pontos à esquerda da reta tem uma grande chance de não serem diabéticos, enquanto à direita, uma grande chance de serem. 
Com esta instrução simples, toda vez que a gente fosse inserir um novo ponto no plano, mesmo sem saber verdadeiramente se a pessoa é diabética, ou não, seria possível, por meio das coordenadas $(x, y)$ criar uma validação simples que prevê com uma certa precisão se a pessoa tem ou não diabetes. 

Esta regra de validação nada mais é do que um modelo bem simples de rede neural. Por meio de um conjunto de dados, com informações verdadeiras, encontramos uma reta, que passa a ser uma divisória para um modelo que tenta probabilisticamente prever as chances de um paciente ter diabetes. Isto por si só é informação suficiente para **realmente** prever se alguém tem diabetes? Obviamente não. Diabetes possui inúmeros outros fatores que aqui não foram considerados: genética, histórico familiar, hábitos, composição de gordura corporal, etc... Mas aqui estamos recortando o modelo para uma análise simples com fins didáticos. 