---
title: "Redes Neurais do Zero: Classificador Linear"
date: 2026-07-27 10:00:00 -0300
math: true
---

# Programação Tradicional vs Aprendizado de Máquina

Antes de mais nada é importante traçar uma divisória bem clara para separar duas coisas: Uma rede neural (inteligência artificial) não é um algoritmo "inteligente" cheio de condicionais. São duas formas diferentes (desde a sua concepção) de interpretar e solucionar problemas. 

- *Programação tradicional*: Você escreve regras $\to$ entra com dados $=$ sai a resposta
- *Machine Learning*: Você entra com dados $\to$ entra com as respostas $=$ o algoritmo *"aprende"* (calcula) as regras de forma autônoma. 	

# Situação problema: diabetes
Para começar a pensar sobre redes neurais, tomemos a seguinte situação:
Por meio de uma [pesquisa](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database), um grupo de 752 pessoas tiveram, dentre outras coisas, duas informações aferidas:
- Nível de glicose no sangue (mg/dL) - eixo $x$
- Índice de Massa Corporal (IMC) - eixo $y$ 

Desta forma, cada pessoa é inserida em um plano cartesiano por meio de um par de coordenadas $(x, y)$. Além disso, cada ponto possui uma cor associada a uma informação verdadeira:
- Azul: Paciente não diabético
- Vermelho: Paciente diabético

Veja abaixo o gráfico interativo com os dados reais da pesquisa. 

<div style="position: relative; width: 100%; aspect-ratio: 4 / 3; margin: 1.5em auto;">
  <iframe src="/assets/plots/diabetes_scatter.html" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"></iframe>
</div>

Não é preciso fazer uma análise matemática profunda para perceber que existe um certo padrão que divide esse dois dados. Talvez, não de forma exata, seria possível traçar uma reta que tentasse separar, mesmo que grosseiramente, a maioria dos pontos azuis, da maioria dos pontos vermelhos. Desta forma, seria possível criar uma espécie de regra algébrica de validação. Algo como, os pontos à esquerda da reta tem uma grande chance de não serem diabéticos, enquanto à direita, uma grande chance de serem. 
Com esta instrução simples, toda vez que a gente fosse inserir um novo ponto no plano, mesmo sem saber verdadeiramente se a pessoa é diabética, ou não, seria possível, por meio das coordenadas $(x, y)$ criar uma validação simples que prevê com uma certa precisão se a pessoa tem ou não diabetes. 

Esta regra, nada mais é do que um modelo bem simples de rede neural. Por meio de um conjunto de dados, com informações verdadeiras, "treinamos o modelo" para que ele aprenda como classificar os dados por meio de um conjunto de características. Em outras palavras, dentro um conjunto de dados dispersos em um plano, encontramos uma reta, que passa a ser uma divisória para um modelo tentar prever as chances de um paciente ter diabetes. 

> Isto por si só é informação suficiente para **realmente** prever se alguém tem diabetes? Obviamente não. Diabetes possui inúmeros outros fatores que aqui não foram considerados: genética, histórico familiar, hábitos, composição de gordura corporal, etc... Mas aqui estamos simplificando o modelo para uma análise apenas com fins didáticos. 

# Camadas da Rede
## Input Layer 
Para uma rede neural não importa com que tipo de dado estamos trabalhando. Para ela tudo são vetores. Se existe um objeto ou conceito abstrato no mundo real que pode ser transformado num vetor, então existe uma grande chance de que ela consiga entender e aprender as características dessa coisa.  
Seja um conjunto de palavras, uma imagem, um dataset sobre diabetes, para uma rede neural tudo são vetores. 

Por isso no contexto do nosso problema, a camada de entrada, também conhecida por input layer, nada mais é do que a simples representação vetorial de cada um dos nossos pacientes. Tomando como base as convenções usadas no livro [DeepLearning](https://www.deeplearningbook.org/) para representar escalares, vetores, matrizes e tensores... temos que um vetor de entrada, é um vetor coluna $\mathbf{x}$ no formato $n \times 1$:

$$\mathbf{x} = 
\begin{bmatrix} x_1 \\ 
x_2 \\ \vdots \\ 
x_n 
\end{bmatrix}$$

### Neurônios
Os famosos neurônios que compõe as redes neurais, nada mais são do que cada uma das coordenas do vetor. Então, no nosso exemplo, como o vetor possui duas dimensões, podemos dizer que a primeira camada da rede neural é composta por exatamente dois neurônios.

## Output layer
A camada de saída também se trata de um vetor, geralmente de dimensão inferior que o vetor de entrada. Como uma rede neural é um sistema probabilístico, então por convenção dizemos que o vetor de saída é um vetor de previsão, também no formato vetor coluna, representado por $\hat{\mathbf{y}}$:

$$\hat{\mathbf{y}} = \begin{bmatrix}
\hat{y}_1 \\
\hat{y}_2 \\
\vdots \\
\hat{y}_{n} \\
\end{bmatrix}$$



No nosso caso é um vetor de dimensão única, ou uma camada de um único neurônio, pois queremos separar o conjunto de dados em apenas dois grandes grupos. 