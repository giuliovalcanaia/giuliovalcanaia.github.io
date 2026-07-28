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
# O problema da Diabetes

$$
y = w_1 x_1 + w_2 x_2 + b
$$
