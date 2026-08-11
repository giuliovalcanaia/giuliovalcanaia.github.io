---
title: Como configurar o modo convidado dentro dos navegadores
description: Aprenda a ativar o modo convidado obrigatório no Google Chrome e no Microsoft Edge por meio de políticas de registro do Windows, ideal para laboratórios de informática e ambientes compartilhados.
date: 2026-08-11 10:00:00 -0300
categories:
  - Laboratório de Informática
tags:
  - Chrome
  - Edge
  - Dicas
---

Ambientes de laboratório são sempre problema quando se trata de uso compartilhado de computadores. O aluno chega, mexe nas configurações do navegador, muda o plano de fundo, esquece sua conta logada... a lista de problemas é quase infinita.

## Políticas do Google Chrome Enterprise

Para contornar este problema de modo simples e direto usamos uma abordagem que modifica as configurações das políticas do Google Chrome.
É possível encontrar a documentação de todas as políticas disponíveis e o que cada uma delas faz aqui: [Lista de políticas do Chrome Enterprise](https://chromeenterprise.google/policies/).

### Modificar os Registros do Windows para forçar o Modo Convidado no Chrome

Abra o Prompt de Comando (CMD) ou o PowerShell como Administrador e execute:

```
reg add "HKLM\SOFTWARE\Policies\Google\Chrome" /v BrowserGuestModeEnforced /t REG_DWORD /d 1 /f
```

Pronto. Agora toda vez que o Google Chrome for fechado, ele exclui automaticamente todas as modificações feitas pelos alunos (inclusive contas e logins). Ao abrir, o usuário se depara com uma instância padrão do navegador, como é possível ver na imagem abaixo.

<style>
  .diagram-75 { width: 75%; }
  @media (max-width: 768px) {
    .diagram-75 { width: 100%; }
  }
</style>

<div style="margin: 1.5em auto;">
  <img class="diagram-75" src="/assets/img/modo-convidado-chrome.png" alt="Tela do Google Chrome aberta no modo convidado" style="height: auto; display: block; margin: 0 auto;" />
</div>

### Remover política e reverter modificações

Caso você não goste da proposta do modo convidado, é possível reverter facilmente a modificação:

```
reg delete "HKLM\SOFTWARE\Policies\Google\Chrome" /v BrowserGuestModeEnforced /f
```

## Políticas do Microsoft Edge

O Google Chrome e o MS Edge são construídos em cima da mesma base, que é o Chromium, por isso, é possível aplicar a mesma configuração ao Edge.

### Modificar os Registros do Windows para forçar o Modo Convidado no Edge

Para fazer o Edge abrir obrigatoriamente na tela de Convidado/Visitante, abra o Prompt de Comando (CMD) ou PowerShell como Administrador e execute:

```
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v BrowserGuestModeEnforced /t REG_DWORD /d 1 /f
```

Para remover essa restrição e voltar ao comportamento padrão:

```
reg delete "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v BrowserGuestModeEnforced /f
```
