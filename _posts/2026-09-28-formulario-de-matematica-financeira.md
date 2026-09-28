---
title: "Formulário de Matemática Financeira"
date: 2026-09-28 10:00:00 -0300
categories:
  - Matemática Financeira
tags:
  - matemática financeira
  - fórmulas
  - juros simples
  - juros compostos
  - desconto
  - taxas equivalentes
math: true
description: "Compilação de fórmulas de capitalização simples, desconto, juros compostos, taxas equivalentes e convenções financeiras."
---

Este post reúne as principais fórmulas de **Matemática Financeira** para consulta rápida. Ele pode ser usado como material de apoio aos posts sobre uso da HP-12C e exercícios resolvidos.

## Notação

- $C$ ou $VP$: Capital / Valor Presente
- $M$ ou $VF$: Montante / Valor Futuro
- $J$: Juros
- $i$: Taxa de juros (forma decimal)
- $n$: Prazo (unidade de tempo alinhada à taxa $i$)

## Capitalização Simples

### Porcentagem e Variação Percentual
- **Parte:**
   $$\text{Parte} = \text{Taxa} \times \text{Total}$$
- **Variação percentual ($\Delta\%$):**
   $$\Delta\% = \frac{\text{Valor Final} - \text{Valor Inicial}}{\text{Valor Inicial}}$$
- **Aumento de $p\%$:**
   $$\text{Valor Final} = \text{Valor Inicial} \times (1 + p)$$
- **Desconto de $p\%$:**
   $$\text{Valor Final} = \text{Valor Inicial} \times (1 - p)$$
- **Valor anterior a um aumento:**
   $$\text{Valor Inicial} = \frac{\text{Valor Final}}{1 + p}$$

### Juros Simples

- **Juros:**
   $$J = C \cdot i \cdot n$$
- **Montante:**
   $$M = C + J = C \cdot (1 + i \cdot n)$$
- **Capital:**
   $$C = \frac{M}{1 + i \cdot n}$$
- **Prazo:**
   $$n = \frac{\frac{M}{C} - 1}{i}$$
- **Taxa:**
   $$i = \frac{\frac{M}{C} - 1}{n}$$

### Imposto sobre o Juro

- **Montante líquido:**
   $$M_{\text{líquido}} = C + J \cdot (1 - \text{alíquota})$$

## Desconto Simples

- $N$: Valor Nominal (resgate)
- $V$: Valor Atual (liberado)
- $D$: Desconto
- $d$: Taxa de desconto

### Desconto Comercial (Por Fora)

- **Desconto:**
   $$D = N \cdot d \cdot n$$
- **Valor Atual:**
   $$V = N - D = N \cdot (1 - d \cdot n)$$
   
- **Valor Nominal:**
   $$N = \frac{V}{1 - d \cdot n}$$

### Desconto Racional (Por Dentro)

- **Valor Atual:**
   $$V = \frac{N}{1 + i \cdot n}$$
- **Desconto:**
   $$D = N - V = V \cdot i \cdot n$$
- **Desconto em função do Valor Nominal:**
   $$D = \frac{N \cdot i \cdot n}{1 + i \cdot n}$$

### Taxa Efetiva do Desconto Comercial

- **Linear:**
   $$i = \frac{D}{V \cdot n}$$
- **Composta:**
   $$i = \left(\frac{N}{V}\right)^{\frac{1}{n}} - 1$$

### Com Despesa Administrativa

- **Valor Atual Líquido:**
   $$V = N - D_{\text{comercial}} - (\text{taxa adm} \times N)$$

## Juros Compostos

### Montante e Valor Presente

- **Montante:**
   $$M = C \cdot (1 + i)^n$$
- **Capital / Valor Presente:**
   $$C = \frac{M}{(1 + i)^n}$$
- **Juros:**
   $$J = M - C$$
- **Taxa:**
   $$i = \left(\frac{M}{C}\right)^{\frac{1}{n}} - 1$$
- **Prazo:**
   $$n = \frac{\ln(M/C)}{\ln(1 + i)}$$

### Fluxos de Caixa
- **Avançar no tempo (Futuro):**
   $$VF = VP \cdot (1 + i)^n$$
- **Recuar no tempo (Presente):**
   $$VP = \frac{VF}{(1 + i)^n}$$

### Taxas Equivalentes

- **Relação entre prazos:**
   $$(1 + i_{\text{maior}}) = (1 + i_{\text{menor}})^k$$
> _(onde $k$ é a quantidade de períodos menores dentro do período maior)_
- **Exemplos de equivalência:**
   $$1 + i_a = (1 + i_s)^2 = (1 + i_t)^4 = (1 + i_m)^{12}$$
- **Fórmula genérica para qualquer prazo:**
   $$i_{\text{quero}} = (1 + i_{\text{tenho}})^{\frac{n_{\text{quero}}}{n_{\text{tenho}}}} - 1$$

### Taxa Nominal e Efetiva

- **Taxa proporcional do período de capitalização:**
   $$i = \frac{i_{\text{nominal}}}{k}$$
> _(onde $k$ é o número de capitalizações no ano)_
- **Taxa Efetiva Anual:**
   $$i_{\text{ef}} = \left(1 + \frac{i_{\text{nominal}}}{k}\right)^k - 1$$
- **Taxa Nominal a partir da Efetiva:**
   $$i_{\text{nominal}} = k \cdot \left[(1 + i_{\text{ef}})^{\frac{1}{k}} - 1\right]$$
   
### Convenções para Períodos Não Inteiros ($n = \text{parte inteira} + \text{fração}$)

- **Convenção Exponencial:**
   $$M = C \cdot (1 + i)^n \quad \text{(com } n \text{ fracionário direto)}$$
- **Convenção Linear:**
   $$M = C \cdot (1 + i)^{\text{parte inteira}} \cdot (1 + i \cdot \text{fração})$$

