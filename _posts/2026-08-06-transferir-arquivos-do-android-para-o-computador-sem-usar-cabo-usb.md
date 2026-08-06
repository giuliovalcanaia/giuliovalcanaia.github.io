---
title: Transferir arquivos do Android para o computador sem usar cabo USB
description: Aprenda a transferir arquivos entre Android e computador sem cabo USB usando SFTP, chaves SSH e SSHFS para montar o celular no sistema de arquivos do Linux com segurança e praticidade.
date: 2026-08-06 10:00:00 -0300
categories:
  - Android
tags:
  - Android
  - SFTP
  - FTP
---

## Introdução
Transferir arquivos quando não se tem um cabo USB por perto pode ser um verdadeiro pesadelo. Felizmente existem soluções alternativas que possibilitam a transferência de arquivos de maneira segura a qualquer momento em qualquer lugar, sem cabos USB, em alta velocidade, por meio da rede Wi-Fi.

## Secure File Transfer Protocol
Também conhecido por *SSH File Transfer Protocol* e abreviado por **SFTP**, é um protocolo que permite a transferência, gerenciamento e manipulação de arquivos entre dispositivos através de uma conexão de internet.

Diferentemente do protocolo FTP tradicional (_File Transfer Protocol_), o SFTP roda sobre o protocolo SSH. Isso implica dizer que todo tráfego é protegido por criptografia de ponta a ponta em uma única porta, garantindo segurança, integridade de dados e facilidade de acesso.

### Autenticação
O login pode ser feito tanto por usuário e senha, quanto por um par de chaves SSH, oferecendo maior segurança e facilidade de acesso.

## Primitive FTPd
No lado do Android precisamos configurar o servidor de arquivos. Para isto, utilizaremos o aplicativo open source [Primitive FTPd](https://github.com/wolpi/prim-ftpd) que pode ser baixado diretamente via página de [releases](https://github.com/wolpi/prim-ftpd/releases) ou por meio da loja [F-Droid](https://f-droid.org/pt_BR/).

### Configuração
#### Habilitar apenas SFTP
A primeira configuração que iremos fazer no nosso servidor é desabilitar o protocolo FTP e permitir apenas o SFTP, garantindo assim maior segurança de dados.

<style>
  .video-50 {
    width: 30%;
    margin: 0 auto;
    display: block;
  }
  @media (max-width: 768px) {
    .video-50 {
      width: 50%;
    }
  }
</style>

<div style="margin: 1.5em auto; text-align: center;">
  <video class="video-50" autoplay loop muted playsinline style="height: auto;">
    <source src="/assets/videos/primitive-ftpd-config.webm" type="video/webm">
    Seu navegador não suporta vídeos WebM.
  </video>
</div>

#### Autenticação por chave pública
Neste momento abrimos as configurações do celular e habilitamos a _Autenticação da chave pública_. No momento da escrita deste tutorial ela está logo acima da configuração que alteramos anteriormente ao [habilitar apenas o SFTP](#habilitar-apenas-sftp).

##### Par de chaves
Para criar o par de chaves e permitir uma conexão segura, iremos abrir o terminal e rodar o comando abaixo para criar um par de chaves por meio do algoritmo de criptografia de curva elíptica Ed25519
```bash
ssh-keygen -t ed25519 -C "celular-android"
```
> Você pode ir preenchendo com as informações que ele solicita ou só ir pressionando <kbd>Enter</kbd> para cada uma das perguntas.

As chaves serão salvas no caminho padrão `~/.ssh/id_ed25519` e a chave pública pode ser visualizada por meio do comando abaixo
```bash
awk '{print $1, $2}' ~/.ssh/id_ed25519.pub
```

Agora você deverá copiar a saída do terminal. É uma string mais ou menos neste formato

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDexample
```

Essa string deverá ser copiada e enviada ao dispositivo android e inserida no campo _Add public key for auth_

<div style="margin: 1.5em auto; text-align: center;">
  <video class="video-50" autoplay loop muted playsinline style="height: auto;">
    <source src="/assets/videos/primitive-ftpd-auth.webm" type="video/webm">
    Seu navegador não suporta vídeos WebM.
  </video>
</div>

> Lembre-se! Guarde a chave privada (`~/.ssh/id_ed25519`, sem `.pub`) num lugar seguro e nunca compartilhe-a com ninguém. A string acima é a chave pública, que deve ser inserida no app.


#### Iniciar servidor
Na sequência iniciamos o servidor clicando no canto superior direito no ícone do triângulo.

<div style="margin: 1.5em auto; text-align: center;">
  <img class="video-50" src="/assets/img/iniciar-servidor.avif" alt="Iniciar servidor Primitive FTPd" style="height: auto;">
</div>

#### Teste de conexão
Neste momento já estamos com tudo pronto para iniciar o teste de conexão. Entre com o comando abaixo no terminal substituindo _IP_DO_CELULAR_ pelo seu ip
```bash
sftp -b - -P 1234 -i ~/.ssh/id_ed25519 user@IP_DO_CELULAR <<< "exit"
```
> Lembre-se de verificar em qual porta o servidor está operando

Ele deverá conectar e então imediatamente se desconectar e sair do sftp

## Criar ponto de montagem 
Agora que já temos toda a parte da configuração feita podemos finalmente partir para a montagem e acesso dos arquivos na máquina de destino.

Crie uma pasta para servir de ponto de montagem
```bash
mkdir -p ~/mnt/celular
```

Comando para montar o armazenamento do celular no computador
```bash
sshfs -p 1234 -o IdentityFile=~/.ssh/id_ed25519,reconnect user@IP_DO_CELULAR:/ ~/mnt/celular
```

Depois disso uma pasta vai aparecer no seu sistema de arquivos. É possível testar assim:
```bash
ls -la ~/mnt/celular
```
> Às vezes a primeira conexão demora um pouco e por isso pode parecer que o comando travou

Caso você queira desmontar (lembre-se de desmontar ao terminar de usar, caso contrário o ponto de montagem ficará bloqueado)
```bash
fusermount -u ~/mnt/celular
```

> Não se esqueça de autorizar o acesso ao sistema de arquivos (no banner vermelho na parte inferior no aplicativo)

## Tipos de armazenamento

O **Primitive FTPd** oferece cinco modos de compartilhamento de armazenamento. Dependendo da opção escolhida, o app pode solicitar permissão de acesso ao sistema de arquivos do Android — especialmente nos modos que precisam varrer diretórios fora do escopo padrão do aplicativo. Abaixo, o que cada um faz e quando usá-lo.

### 1. Sistema de arquivos antigo e simples
Este modo acessa diretamente o sistema de arquivos tradicional do Android. Em versões mais recentes do sistema, ele costuma operar com **acesso somente leitura** por limitações de permissão impostas pelo Android. Serve bem para visualizar arquivos, mas não permite enviar ou editar nada no celular. O próprio app indica no rodapé que, caso a conexão seja somente leitura, é preciso conferir as permissões ou mudar de modo.

### 2. Super usuário (root)
Disponível apenas em dispositivos com acesso **root**. Com ele, o servidor enxerga todo o sistema de arquivos sem restrições de permissão, permitindo leitura e escrita em qualquer pasta. É a opção mais poderosa, mas exige um aparelho modificado e cuidado redobrado para não alterar arquivos do sistema por acidente.

### 3. Framework de acesso ao armazenamento do Android (SAF)
O **SAF** (*Storage Access Framework*) é a API moderna do Android para acesso a arquivos. Ele é ideal quando você precisa acessar o **cartão SD** ou outras mídias externas, pois trabalha com permissões delegadas pelo próprio sistema operacional. Neste modo, o app pede ao usuário que escolha quais pastas compartilhar, e o servidor enxerga exatamente aquela seleção — com leitura e escrita habilitadas, desde que autorizadas.

### 4. Apenas leitura SAF (mais rápido!)
Uma variante do modo SAF que abre mão da escrita em troca de **maior velocidade**. Como o servidor não precisa gerenciar alterações, a listagem e a transferência de arquivos para o computador ficam mais ágeis. Use esta opção quando o objetivo for apenas copiar arquivos do celular para a máquina, sem modificar nada no dispositivo.

### 5. Pastas virtuais
Este modo cria uma **visão unificada** que combina todos os outros tipos de armazenamento em uma única árvore de diretórios. É a opção mais flexível: você enxerga de uma só vez o sistema de arquivos interno, cartão SD e quaisquer locais autorizados via SAF. Para o uso no dia a dia, **esta é a opção recomendada**, pois elimina a necessidade de ficar trocando de perfil toda vez que o arquivo desejado está em um local diferente.
