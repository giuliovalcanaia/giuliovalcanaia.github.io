---
title: Remover anúncios de aplicativos android
description: Neste tutorial vou estar mostrando como bloquear um aplicativo de acessar a internet e por meio deste método impedi-lo de exibir anúncios. Como forma de exemplificação, vou estar demonstrando com o aplicativo Touch RPN (HP-12C)
date: 2026-08-04 10:00:00 -0300
categories:
  - Android
tags:
  - ADB
  - Java
  - Android
  - Mobile
math: true
---
## Pré-requisitos
Antes de darmos início ao procedimento, precisamos garantir que estes pacotes estejam instalados no sistema. Aqui para o tutorial, vou utilizar como exemplo um sistema ArchLinux. 

Caso você esteja utilizando Ubuntu ou alguma outra distribuição, o procedimento é equivalente. Basta você procurar na internet ou pedir ajuda para alguma ferramenta de IA sobre como fazer a instalação de cada um dos pacotes abaixo.

### Pasta de trabalho

Crie uma pasta para organizar os arquivos que serão gerados durante o processo:

```bash
mkdir -p ~/touchrpn-apk && cd ~/touchrpn-apk
```

### Pacotes necessários

| Pacote / Ferramenta     | Finalidade no Tutorial                                         |
| ----------------------- | -------------------------------------------------------------- |
| Java Environment        | Necessário para executar o APKEditor, `keytool` e `apksigner`. |
| Android Tools (ADB)     | Para comunicação via USB e extração/instalação via `adb`.      |
| Android SDK Build Tools | Fornece os utilitários `zipalign` e `apksigner`.               |
| Apktool                 | Para descompilar e reempacotar a APK (`.smali`, `.xml`).       |
| cURL                    | Para baixar o `APKEditor.jar`.                                 |
| Editor de Texto         | Para edições no `AndroidManifest.xml` ou código Smali.         |

Você pode instalar todos os pacotes de uma vez com o comando abaixo:

```bash
sudo pacman -S jdk-openjdk
sudo pacman -S android-tools
sudo pacman -S curl
sudo pacman -S neovim
yay -S android-sdk-build-tools
yay -S android-apktool-bin
```

### APKEditor

O **[APKEditor](https://github.com/REAndroid/APKEditor)** é uma ferramenta Java essencial para mesclar *Split APKs* (`base.apk` + `split_config.*.apk`) em uma única APK funcional antes de descompilar com o Apktool.

Download direto:

```bash
curl -L -o APKEditor.jar "https://github.com/REAndroid/APKEditor/releases/download/V1.4.9/APKEditor-1.4.9.jar"
```

> Aqui a versão utilizada é a 1.4.9, porém, a depender do momento que você está lendo este tutorial, talvez você precise acessar o [repositório](https://github.com/REAndroid/APKEditor/releases) do GitHub e verificar se não existe alguma release nova.

## Ativar modo desenvolvedor

Para que o computador consiga se comunicar com o celular via ADB, é necessário habilitar as **Opções do desenvolvedor** e depois ativar a **Depuração USB**. No Samsung Galaxy A56 o caminho é o seguinte:

1. Abra o aplicativo **Configurações**.
2. Role até o fim e toque em **Sobre o telefone**.
3. Toque em **Informações de software**.
4. Encontre o item **Número de compilação** e toque rapidamente sobre ele **7 vezes** consecutivas.
5. O sistema pedirá a senha ou o PIN de desbloqueio do aparelho. Digite-o para confirmar.
6. Uma notificação curta aparecerá informando que o modo desenvolvedor foi ativado.

Volte à tela inicial das **Configurações** e agora você verá o menu **Opções do desenvolvedor** logo acima de **Sobre o telefone**. Entre nele e ative a chave **Depuração USB**. O celular mostrará um aviso de segurança — confirme para permitir.

### Testar a conexão

Conecte o celular ao computador via cabo USB. No terminal do Linux, execute:

```bash
adb devices
```

Se tudo estiver certo, você verá algo parecido com isso:

```
List of devices attached
RXXXXXXAAA	device
```

## Extrair APK
Procure pelo nome do pacote que você quer extrair. Aqui, como eu não sabia exatamente o nome do pacote, eu coloquei um filtro `grep "touch"`
```bash
adb shell pm list packages | grep "touch"
```

Saída
```
package:co.epxx.touch12if
package:com.sec.android.mimage.photoretouching
```

Agora que sabemos que o nome do pacote é `co.epxx.touch12if`, podemos obter o caminho de instalação (ou caminhos, como é o caso dos pacotes subdivididos):
```bash
adb shell pm path co.epxx.touch12if
```

Saída
```
package:/data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/base.apk
package:/data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/split_config.arm64_v8a.apk
package:/data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/split_config.es.apk
package:/data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/split_config.pt.apk
package:/data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/split_config.xxhdpi.apk
```

Faça download de cada um dos arquivos citados na saída por meio do `adb pull`:

```bash
adb pull /data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/base.apk
adb pull /data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/split_config.arm64_v8a.apk
adb pull /data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/split_config.es.apk
adb pull /data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/split_config.pt.apk
adb pull /data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/split_config.xxhdpi.apk
```

Agora, dentro da pasta de trabalho, devemos estar com estes arquivos:
```
Permissions Size User   Date Modified Name
.rw-r--r--  7.7M giulio  4 Aug 10:29  APKEditor.jar
.rw-r--r--   33M giulio  4 Aug 10:49  base.apk
.rw-r--r--   33k giulio  4 Aug 10:49  split_config.arm64_v8a.apk
.rw-r--r--   25k giulio  4 Aug 10:49  split_config.es.apk
.rw-r--r--   37k giulio  4 Aug 10:49  split_config.pt.apk
.rw-r--r--   67k giulio  4 Aug 10:49  split_config.xxhdpi.apk
```

O próximo passo é consolidar os arquivos em um único apk:
```bash
java -jar APKEditor.jar m -i . -o touch12i_merged.apk
```

Agora vamos descompilar e entrar na pasta que contém os arquivos
```bash
apktool d touch12i_merged.apk -o touch12i_src
cd touch12i_src
```

Devemos encontrar algo assim lá dentro
```
Permissions Size User   Date Modified Name
.rw-r--r--   19k giulio  4 Aug 10:56  AndroidManifest.xml
.rw-r--r--  3.5k giulio  4 Aug 10:56  apktool.yml
drwxr-xr-x     - giulio  4 Aug 10:56  assets
drwxr-xr-x     - giulio  4 Aug 10:56  lib
drwxr-xr-x     - giulio  4 Aug 10:56  original
drwxr-xr-x     - giulio  4 Aug 10:56  res
drwxr-xr-x     - giulio  4 Aug 10:56  smali
drwxr-xr-x     - giulio  4 Aug 10:56  smali_classes2
drwxr-xr-x     - giulio  4 Aug 10:56  smali_classes3
drwxr-xr-x     - giulio  4 Aug 10:56  unknown
```

## Editar o manifesto Android
O próximo passo é editar o arquivo `AndroidManifest.xml`
```bash
nvim AndroidManifest.xml
```

E agora vamos procurar pelas linhas abaixo e removê-las
```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
```

> Esta é a etapa principal do tutorial. A partir deste momento o aplicativo terá todas as requisições bloqueadas pelo sistema Android

## Compilar
Volte para a pasta anterior e execute o Apktool para reconstruir o aplicativo:
```
cd ..
apktool b touch12i_src -j 2 -o touch12i_noads_unaligned.apk
```

Alinhe o APK para otimizar a estrutura do arquivo
```
zipalign -p -v 4 touch12i_noads_unaligned.apk touch12i_noads.apk
```

## Assinar
Para que o Android aceite a instalação, precisamos assinar o arquivo APK. Para isso, criamos uma chave
```bash
keytool -genkey -v -keystore minha_chave.keystore -alias meu_alias -keyalg RSA -keysize 2048 -validity 10000
```
> Você pode preencher qualquer coisa nas perguntas ou apenas dar <kbd>Enter</kbd>, mas guarde a senha que escolher. No final escreva `yes` para finalizar a criação.

Assine o apk modificado
```bash
apksigner sign --ks minha_chave.keystore --ks-key-alias meu_alias touch12i_noads.apk
```
> Entre com a sua senha e pressione <kbd>Enter</kbd>

## Limpar dados do app original

Antes de remover a versão original, é recomendável limpar todos os dados e cache do aplicativo para evitar conflitos com a nova instalação:

```bash
adb shell pm clear co.epxx.touch12if
```

Este comando apaga cache, preferências e arquivos temporários — equivalente a ir em **Configurações > Aplicativos > TouchRPN > Armazenamento > Limpar dados** no celular.

## Instalar
Agora basta remover a instalação atual da calculadora
```bash
adb uninstall co.epxx.touch12if
```

E instalar a nova versão 
```bash
adb install -i com.android.vending touch12i_noads.apk
```