---
title: "Redes Neurais do Zero: Classificador Linear"
date: 2026-07-27 10:00:00 -0300
math: true
categories:
  - Inteligência Artificial
---

<style>
  .diagram-75 { width: 75%; }
  .responsive-diagram { width: 50%; }
  @media (max-width: 768px) {
    .diagram-75 { width: 100%; }
    .responsive-diagram { width: 100%; }
  }
</style>

## Programação Tradicional vs Aprendizado de Máquina

Antes de mais nada é importante traçar uma divisória bem clara para separar duas coisas: Uma rede neural (inteligência artificial) não é um algoritmo "inteligente" cheio de condicionais. São duas formas diferentes (desde a sua concepção) de interpretar e solucionar problemas. 

- *Programação tradicional*: Você escreve regras $\to$ entra com dados $=$ sai a resposta
- *Machine Learning*: Você entra com dados $\to$ entra com as respostas $=$ o algoritmo *"aprende"* (calcula) as regras de forma autônoma. 	

## Situação problema: diabetes
Para começar a pensar sobre redes neurais, tomemos a seguinte situação:
Por meio de uma [pesquisa](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database), um grupo de 752 pessoas tiveram, dentre outras coisas, duas informações aferidas:
- Nível de glicose no sangue (mg/dL) - eixo $x$
- Índice de Massa Corporal (IMC) - eixo $y$ 

>  Os níveis de glicose foram obtidos por meio do Teste Oral de Tolerância à Glicose (TOTG) de 2 horas. Nesse procedimento, a pessoa faz um jejum prévio e depois ingere uma solução padrão contendo 75g de glicose. A coleta de sangue é realizada exatamente duas horas após a ingestão.

Desta forma, cada pessoa é inserida em um plano cartesiano por meio de um par de coordenadas $(x, y)$. Além disso, cada ponto possui uma cor que está associada à uma informação verdadeira:
- Azul: Paciente não diabético
- Vermelho: Paciente diabético
> Esta classificação não representa apenas o estado de saúde do paciente no momento exato do exame, mas também o diagnóstico de desenvolvimento de diabetes em um período de acompanhamento de até 5 anos após a coleta dos dados.

Veja abaixo o gráfico interativo com os dados reais da pesquisa. 

<div class="plot-wrapper diagram-75" style="position: relative; aspect-ratio: 4 / 3; margin: 1.5em auto;">
  <iframe src="/assets/plots/diabetes_scatter.html" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"></iframe>
</div>

Não é preciso fazer uma análise matemática profunda para perceber que existe um certo padrão que divide esse dois dados. Talvez, não de forma exata, seria possível traçar uma reta que tentasse separar, mesmo que grosseiramente, a maioria dos pontos azuis, da maioria dos pontos vermelhos. Desta forma, seria possível criar uma espécie de regra algébrica de validação. Algo como: os pontos à esquerda da reta tem uma grande chance de não serem diabéticos, enquanto à direita, uma grande chance de serem. 

Com esta instrução simples, toda vez que a gente fosse inserir um novo ponto no plano, mesmo sem saber verdadeiramente se a pessoa é diabética, ou não, seria possível, por meio das coordenadas $(x, y)$ criar uma regra simples que prevê com uma certa precisão se a pessoa tem ou não diabetes, e esta regra, nada mais é do que um modelo (bem simples) de rede neural. 

Por meio de um conjunto de dados, com informações verdadeiras, "treinamos o modelo" para que ele aprenda como classificar os dados por meio de um conjunto de características. Em outras palavras, dentro um conjunto de dados dispersos em um plano, encontramos uma reta, que passa a ser uma divisória para o modelo tentar prever as chances de um paciente ter diabetes. 

> Isto por si só é informação suficiente para **realmente** prever se alguém tem diabetes? Obviamente não. Diabetes possui inúmeros outros fatores que aqui não foram considerados: genética, histórico familiar, hábitos, composição de gordura corporal, etc... Mas aqui estamos simplificando o modelo para uma análise apenas com fins didáticos. 

## Camadas da Rede
### Input Layer 
Para uma rede neural não importa com que tipo de dado estamos trabalhando. Para ela tudo são vetores. Se existe um objeto ou conceito abstrato no mundo real que pode ser transformado num vetor, então existe uma grande chance de que ela consiga entender e aprender as características dessa coisa. Seja um conjunto de palavras, uma imagem, um dataset sobre diabetes, para uma rede neural tudo são vetores. 

Por isso no contexto do nosso problema, a camada de entrada, também conhecida por input layer, nada mais é do que a representação vetorial de cada um dos nossos pacientes. Tomando como base as convenções usadas no livro [DeepLearning](https://www.deeplearningbook.org/) para representar escalares, vetores, matrizes e tensores... temos que um vetor de entrada, é um vetor coluna $\mathbf{x}$ no formato $n \times 1$:

$$\mathbf{x} = 
\begin{bmatrix} x_1 \\ 
x_2 \\ \vdots \\ 
x_n 
\end{bmatrix}$$

#### Neurônios
Os famosos neurônios que compõe as redes neurais, nada mais são do que cada uma das coordenas do vetor. Então, no nosso exemplo, como o vetor possui duas dimensões, podemos dizer que a primeira camada da rede neural é composta por exatamente dois neurônios.

### Output layer
A camada de saída também se trata de um vetor, geralmente de dimensão inferior que o vetor de entrada, ou as vezes igual. Como uma rede neural é um sistema probabilístico, então por convenção dizemos que o vetor de saída é um vetor de previsão, também no formato vetor coluna, representado por $\hat{\mathbf{y}}$:

$$\hat{\mathbf{y}} = \begin{bmatrix}
\hat{y}_1 \\
\hat{y}_2 \\
\vdots \\
\hat{y}_{n} \\
\end{bmatrix}$$


 Como o nosso problema é uma classificação binária (o paciente é diabético ou não), a camada de saída precisa de apenas 1 neurônio.

Esse único neurônio nos retornará um valor entre 0 e 1 (uma probabilidade). Por exemplo: um resultado $0.85$ significa $85\%$ de chance de o paciente ser diabético (grupo vermelho) e, consequentemente, apenas $15\%$ de chance de ser não diabético (grupo azul).

## Matriz de Pesos ($\mathbf{W}$)
Os pesos representam a importância relativa de cada informação da camada de entrada (ou anterior) para a próxima camada. Na prática, cada neurônio da camada seguinte recebe a soma das multiplicações entre o valor de cada neurônio anterior e o seu respectivo peso. Por isso, cada neurônio na camada de entrada possui um peso associado:

- $w_1$: Peso atribuído à Glicose
- $w_2$: Peso atribuído ao IMC

Se a rede perceber durante o treino que o nível de glicose é um indicador muito mais forte para diabetes do que o IMC, o valor de $w_1$ será ajustado para ser significativamente maior que $w_2$.

Assim sendo, podemos organizar estes pesos em um vetor coluna:

$$\mathbf{w} = \begin{bmatrix}
w_1 \\
w_2 \\
\end{bmatrix}$$

> Aqui é importante destacar que quando estamos lidando com pesos, geralmente ao agrupá-los, produzimos uma matriz de pesos e não um vetor. Isto se deve ao fato que cada neurônio da camada anterior cria uma linha na matriz de pesos, e cada neurônio da próxima camada recebe uma coluna da matriz de pesos.

## Viés ($b$)
Outro conceito importante para as redes neurais é o viés (ou *bias*). Trata-se de um escalar único que é somado à combinação das entradas. Matematicamente, ele possui a mesma função que que o coeficiente linear de uma reta ($y = ax + b$)
Na prática, o viés dá à rede a flexibilidade de deslocar a fronteira de decisão para cima, para baixo, para esquerda ou para direita, independentemente dos valores de entrada. Sem o viés, a nossa reta de separação seria forçada a passar sempre pela origem $(0,0)$ do plano cartesiano — o que raramente faz sentido para dados reais.

## Forward Propagation
É o processo de passar a entrada de dados pelas camadas da rede neural, a fim de gerar uma predição.
### Parte Linear do Neurônio
Agora que sabemos as principais partes que compõem o cálculo da rede neural, podemos ver como ficaria a primeira operação que o neurônio realiza: uma combinação linear (ou produto escalar) entre o vetor de entrada $\mathbf{x}$ e o vetor de pesos $\mathbf{w}$, somado ao viés $b$. Geralmente chamamos o resultado desta operação de $z$:

$$z = \mathbf{w}^T \mathbf{x} + b$$

> Perceba que a matriz de pesos precisou ser transposta para poder permitir a multiplicação. 

Expandindo a notação matricial para o nosso caso, temos:

$$z = w_1 x_1 + w_2 x_2 + b$$

Note algo fundamental aqui: $z$ é uma equação geral da reta. É exatamente essa reta que define em qual lado da fronteira de separação um determinado paciente se encontra:
- Se $z > 0$, o ponto tende a ficar do lado "vermelho"
- Se $z < 0$, o ponto tende a ficar do lado "azul"

### Função de Ativação (Sigmoide)
A outra parte do cálculo que o neurônio realiza, diz respeito à uma função matemática não-linear, chamada de Função Sigmoide (letra grega "$\sigma$" *sigma*). Esta função, tem por objetivo (agora vou pedir autorização para usar termos não técnicos) "achatar" a reta numérica, tanto a parte de infinitos positivos, quanto a parte de infinitos negativos, em um intervalo entre $0$ e $1$. Esta função é perfeita pois coloca os dados em um intervalo que podemos facilmente interpretar em termos de "tantos $\%$ de probabilidade de ser isto ou aquilo".  
#### Fórmula

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

#### Gráfico
Aqui nesta imagem retirada do site [Sigmoidal](https://sigmoidal.ai/binary-cross-entropy-regressao-logistica/) podemos ver como a função sigmoide funciona como um *interruptor suave*, mapeando qualquer valor de $z$ em uma probabilidade contínua entre 0 e 1.

<div style="margin: 1.5em auto;">
  <img class="diagram-75" src="/assets/img/redes_neurais/sigmoid-interruptor-suave.png" alt="Gráfico da função sigmoide mostrando como valores negativos tendem a 0, o ponto neutro em z=0 resulta em 0.5, e valores positivos tendem a 1" style="height: auto; display: block; margin: 0 auto;" />
</div>


#### Explicação extra
Caso mesmo assim não tenha ficado claro, podemos pensar em dividi-la em 3 zonas para um melhor entendimento:
- Valores muito negativos (ex: $-15$, $-5$): O resultado aproxima do $0$.
- O ponto neutro ($z = 0$): O resultado é exatamente **$0.5$** ($50\%$ de chance, total dúvida).
- Valores muito positivos (ex: $+5$, $+15$): O resultado aproxima do 1.

## Representação visual da rede neural
Com base em todas as informações que temos até aqui, podemos criar uma representação visual que mostra exatamente como é o fluxo de dados na nossa rede neural.

<div style="margin: 1.5em auto;">
  <img class="responsive-diagram" src="/assets/img/redes_neurais/Gemini_Generated_Image_26m0uc26m0uc26m0.avif" alt="Representação visual da rede neural: Input Layer com Glicose (x₁) e IMC (x₂), Bias (b) e Output Layer com σ(z) e ŷ (Probabilidade Diabetes)" style="height: auto; display: block; margin: 0 auto;" />
</div>


> Imagem criada usando o Nano Banana no Gemini

## Back Propagation
É o algoritmo fundamental usado para treinar e corrigir as redes neurais.
### Função de perda / custo (Loss Function)
Antes de ajustar os pesos e *bias* da rede precisamos medir quão ruim foi o palpite dado pela rede. Para isso comparamos o a resposta que o modelo nos forneceu com o vetor $\mathbf{\hat{y}}$ com a resposta real da pesquisa, que é armazenada pelo vetor $\mathbf{y}$, que também é chamado de *Vetor de Rótulo Real*, pois carrega as informações verdadeiras
#### Vetor de Rótulo Real ($\mathbf{y}$)
É um vetor simples em formato binário que carrega a informação que seria esperada na saída do modelo. No nosso caso, ele pode carregar o valor $0$ para azul ou $1$ para vermelho. 

#### Entropia Cruzada Binária - *BCE* (Binary Cross-Entropy ou Log Loss)
É uma função de perda utilizada em redes neurais que lidam com problemas de classificação para medir quão bom (ou ruim) foi o palpite da rede. Sua característica é penalizar fortemente previsões erradas, enquanto mantém penalidades baixas quando o modelo consegue chegar perto da previsão proposta. 

##### Função de Perda (Erro de um único paciente, denotada por $L$)

$$L(\hat{y}, y) = - \big[ y \cdot \log(\hat{y}) + (1 - y) \cdot \log(1 - \hat{y}) \big]$$

##### Gráfico
Aqui nesta imagem retirada do site [Sigmoidal](https://sigmoidal.ai/binary-cross-entropy-regressao-logistica/) podemos ver como a o nosso vetor de previsão (denotado por $\mathbf{\hat{y}}$ no nosso texto e como $\mathbf{\hat{p}}$ no exemplo deles) se comporta dentro da *BCE*:

<div style="margin: 1.5em auto;">
  <img class="diagram-75" src="/assets/img/redes_neurais/cross-entropy-punicao-confianca.png" alt="Gráfico da Cross-Entropy mostrando a punição da confiança: perda aumenta drasticamente quando a previsão está errada" style="height: auto; display: block; margin: 0 auto;" />
</div>

Apesar de assustar em um primeiro momento, veremos com base em alguns exemplos, que se trata de uma fórmula com uma lógica bem intuitiva. Ela é dividida em duas partes que se alternam com base na resposta. 

$$ L(\hat{y}, y) = - \big[ \textcolor{red}{y \cdot \log(\hat{y})} + \textcolor{blue}{(1 - y) \cdot \log(1 - \hat{y})} \big] $$

###### **Cenário A: um paciente que realmente tem diabetes**
Se $y = 1$, a segunda parte do parênteses $(1 - y)$ vira zero e desaparece:

$$L(\hat{y}, 1) = - \big[ 1 \cdot \log(\hat{y}) + \cancel{(1 - 1) \cdot \log(1 - \hat{y})} \big]$$

A fórmula fica simplificada para:

$$L(\hat{y}, 1) = - y \cdot \log(\hat{y})$$

- Se o modelo prever $\hat{y} = 0.95$ ($95\%$ de certeza): $-\log(0.95) \approx \mathbf{0.051}$ (Perda muito baixa $=$ Excelente acerto)
- Se o modelo prever $\hat{y} = 0.10$ ($10\%$ de certeza, errando feio): $-\log(0.10) \approx \mathbf{2.30}$ (Perda altíssima $=$ Erro)


###### **Cenário B: Um paciente que não tem diabetes**
Se $y = 0$, a primeira parte $y \cdot \log(\hat{y})$ vira zero e desaparece:

$$L(\hat{y}, 0) = - \big[ \cancel{0 \cdot \log(\hat{y})} + (1 - 0) \cdot \log(1 - \hat{y}) \big]$$

A fórmula fica simplificada para:

$$L(\hat{y}, 0) = -\log(1 - \hat{y})$$

- Se o modelo prever $\hat{y} = 0.05$ ($5\%$ de chance de ser diabético, ou seja, $95\%$ de ser azul): $-\log(1 - 0.05) \approx \mathbf{0.051}$ (Perda baixa $=$ Acerto)
- Se o modelo prever $\hat{y} = 0.90$ ($90\%$ de chance de ser diabético, errando feio): $-\log(1 - 0.90) \approx \mathbf{2.30}$ (Perda pesada $=$ Erro)




#### Função de Custo (Média de todas as perdas, denotada por $J$)
Enquanto a função de perda (*Loss*) é o erro de um único paciente, a função de custo (*Cost Function*) é a média de todas as perdas dos 752 pacientes. Ou seja, o modelo roda uma vez em cima de cada um dos pacientes, com os mesmos pesos e viés, para tentar prever se ele é diabético ou não, e então cria uma média aritmética de todas as perdas calculadas. 

$$J(\mathbf{w}, b) = \frac{1}{m} \sum_{i=1}^{m} L(\hat{y}^{(i)}, y^{(i)})$$

> Onde $m$ representa o total de pacientes. 


### Gradiente Descendente (*Gradient Descent*)
Outro passo importante para criar um sistema que consiga "aprender" por meio dos próprios erros, é o cálculo do gradiente descendente. Apesar do nome não ser muito intuitivo para quem não está acostumado com os termos matemáticos usados no cálculo, gradiente de uma função é um vetor que aponta para a direção de maior crescimento de uma função a partir de um determinado ponto. Gradiente **descendente**, por outro lado, como o nome sugere, faz o caminho inverso: aponta para a direção de menor crescimento.

Uma outra maneira possível de pensar sobre o GD (abreviação que irei usar daqui para frente ao me referir ao termo Gradiente Descendente) é pensar na ideia de otimizar o caminho para encontrar a reta da classificação linear. Inicialmente podemos gerar uma reta aleatória, e então analisar o resultado para ver quão bem ela representa o conjunto de dados que estamos buscando. Caso esta reta esteja muito longe, o GD aponta para a direção que ela deve mudar e além disso informa o tanto que ela deve mudar, de modo que ao tentar criar uma nova reta, o modelo consiga uma que se aproxima cada vez mais da reta que estamos almejando. Por isso, ao passo que a reta se aproxima da reta ideal, ela tende a diminir o "passo" em que ela se altera. 

#### Visualizando a função de custo
Uma analogia que podemos atribuir ao conceito do GD, é pensar numa pessoa com os olhos vendados que inicia uma caminhada no topo de uma montanha. Seu objetivo é chegar ao fundo sem enxergar o caminho, apenas testando com os pés para ver a direção que o morro tende a levar para "baixo". 

A montanha nada mais é do que a função de custo plotada num espaço tridimensional. 

https://youtube.com/shorts/H1j67Ri2RSg?si=lKytbq9pKjIQjax5

https://youtu.be/htfh2xrnlaE?si=x7F4OB9OR3UPKSvK&t=669