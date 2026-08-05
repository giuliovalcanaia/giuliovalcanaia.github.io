---
title: Modificando APK Android via engenharia reversa
description: Neste tutorial vou estar mostrando como modificar os arquivos Smali de um aplicativo e desta forma impedi-lo de exibir anúncios. Como exemplificação, vou estar demonstrando com o aplicativo Touch RPN (HP-12C).
date: 2026-08-04 10:00:00 -0300
categories:
  - Android
tags:
  - ADB
  - Java
  - Android
  - Mobile
---
## Pré-requisitos
Antes de darmos início ao procedimento, precisamos garantir que estes pacotes estejam instalados no sistema. Aqui para o tutorial, vou utilizar como exemplo um sistema Arch Linux. 

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

### Touch RPN
Por fim e não menos importante, o seu celular precisa estar com o aplicativo Touch RPN instalado. É possível encontrar o link da Play Store clicando aqui: [Touch RPN](https://play.google.com/store/apps/details?id=co.epxx.touch12if&pcampaignid=web_share).


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

Faça o download de todos os arquivos de uma vez com o script abaixo. Ele lê os caminhos diretamente do celular e executa o `adb pull` automaticamente:

```bash
PACKAGE="co.epxx.touch12if"
for path in $(adb shell pm path $PACKAGE | cut -d: -f2); do
    adb pull "$path"
done
```

> **Prefere fazer manualmente?** Os caminhos de instalação são exclusivos de cada aparelho — o hash (`~~...==`) e o sufixo (`-kDqsz...`) serão diferentes no seu celular. Copie cada caminho exatamente como apareceu na saída do `adb shell pm path` e execute os comandos `adb pull` um a um. No meu caso, os caminhos foram os seguintes:

```bash
adb pull /data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/base.apk
adb pull /data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/split_config.arm64_v8a.apk
adb pull /data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/split_config.es.apk
adb pull /data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/split_config.pt.apk
adb pull /data/app/~~e_sjbpITMR3g78ieZOS48g==/co.epxx.touch12if-kDqszpnfPZvm-jQh0uFD4Q==/split_config.xxhdpi.apk
```

Agora, dentro da pasta de trabalho, você deve estar com estes arquivos:
```
Permissions Size User   Date Modified Name
.rw-r--r--  7.7M giulio  4 Aug 10:29  APKEditor.jar
.rw-r--r--   33M giulio  4 Aug 10:49  base.apk
.rw-r--r--   33k giulio  4 Aug 10:49  split_config.arm64_v8a.apk
.rw-r--r--   25k giulio  4 Aug 10:49  split_config.es.apk
.rw-r--r--   37k giulio  4 Aug 10:49  split_config.pt.apk
.rw-r--r--   67k giulio  4 Aug 10:49  split_config.xxhdpi.apk
```

O próximo passo é consolidar os arquivos em uma única APK:
```bash
java -jar APKEditor.jar m -i . -o touch12i_merged.apk
```

Agora vamos descompilar e entrar na pasta que contém os arquivos:
```bash
apktool d touch12i_merged.apk -o touch12i_src
cd touch12i_src
```

Você deve encontrar algo assim lá dentro:
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

## Desativar o código dos anúncios

O TouchRPN carrega anúncios de duas formas: um **banner** na parte inferior da tela e um **anúncio em tela cheia** quando o app volta para o primeiro plano. Apenas remover as permissões de internet no `AndroidManifest.xml` não é suficiente, pois o app ainda tenta criar os objetos de anúncio e pode travar ou exibir erros. O ideal é anular os métodos que instanciam e carregam esses anúncios diretamente no código Smali.

> Os arquivos `.smali` são a representação em assembly do bytecode Java. Eles ficam dentro da pasta `smali/` e nomeiam as classes do app seguindo a estrutura de pacotes. Por exemplo, a classe `co.epxx.touch12if.AndroActivity` fica em `smali/co/epxx/touch12if/AndroActivity.smali`.


### 1. Desativar a criação do banner

No arquivo `AndroActivity.smali`, localize o método `create_ad()`. Ele é responsável por instanciar o objeto `AdView` (banner do AdMob) e adicioná-lo ao layout da tela.
```bash
nvim smali/co/epxx/touch12if/AndroActivity.smali
```

Você encontrará algo assim:

```
.method private final create_ad()V
    .locals 6
    ...
    (centenas de linhas)
    ...
    return-void
.end method
```

Substitua **todo o conteúdo** entre `.method` e `.end method` por:

```
.method private final create_ad()V
    .locals 0
    return-void
.end method
```

> **Resultado:** o banner nunca é criado nem adicionado à interface.

### 2. Desativar o carregamento do banner

Ainda no mesmo arquivo (`AndroActivity.smali`), localize o método `load_ad_post_eea()`. Ele constrói a requisição de anúncio e chama `loadAd()`.

```
.method private final load_ad_post_eea()V
    .locals 2
    ...
    return-void
.end method
```

Substitua por:

```
.method private final load_ad_post_eea()V
    .locals 0
    return-void
.end method
```

> **Resultado:** mesmo que o banner existisse, ele nunca receberia uma requisição de carregamento.

### 3. Desativar a busca do anúncio em tela cheia

Agora no arquivo `AppOpenManager.smali`, localize o método `fetchAd()`. Ele verifica se já há um anúncio carregado e, se não houver, busca um novo na internet.

```bash
nvim smali/co/epxx/touch12if/AppOpenManager.smali
```

Localize:
```
.method public final fetchAd()V
    .locals 4
    ...
    return-void
.end method
```

Substitua por:

```
.method public final fetchAd()V
    .locals 0
    return-void
.end method
```

> **Resultado:** o app nunca busca o anúncio em tela cheia na internet.

### 4. Desativar a exibição do anúncio em tela cheia

Ainda no `AppOpenManager.smali`, localize o método `onStart()`. Ele é chamado automaticamente pelo ciclo de vida do Android quando o app volta para o primeiro plano e é responsável por exibir o anúncio em tela cheia se ele estiver disponível. Caso ele não ache o anúncio, o aplicativo fica travado com a logo em tela cheia. O método abaixo corrige esses problemas e permite voltar a usar o aplicativo mesmo depois de fechar e retornar.

**Atenção:** este método possui uma anotação `@OnLifecycleEvent` que **deve ser preservada**.

```
.method public final onStart()V
    .locals 10
    .annotation runtime Landroidx/lifecycle/OnLifecycleEvent;
        value = .enum Landroidx/lifecycle/Lifecycle$Event;->ON_START:Landroidx/lifecycle/Lifecycle$Event;
    .end annotation
    ...
    (centenas de linhas)
    ...
    return-void
.end method
```

Substitua por:

```
.method public final onStart()V
    .annotation runtime Landroidx/lifecycle/OnLifecycleEvent;
        value = .enum Landroidx/lifecycle/Lifecycle$Event;->ON_START:Landroidx/lifecycle/Lifecycle$Event;
    .end annotation

    .locals 1
    iget-object v0, p0, Lco/epxx/touch12if/AppOpenManager;->myApplication:Lco/epxx/touch12if/AndroApp;
    invoke-virtual {v0}, Lco/epxx/touch12if/AndroApp;->midsplash_disarm_ad()V
    return-void
.end method
```

> **Resultado:** o evento de retorno ao primeiro plano não dispara mais nenhuma lógica de anúncio.

### Resumo das alterações

| Arquivo                | Método               | Efeito                                           |
| ---------------------- | -------------------- | ------------------------------------------------ |
| `AndroActivity.smali`  | `create_ad()`        | Banner nunca é instanciado                       |
| `AndroActivity.smali`  | `load_ad_post_eea()` | Banner nunca carrega conteúdo                    |
| `AppOpenManager.smali` | `fetchAd()`          | App nunca busca anúncio em tela cheia            |
| `AppOpenManager.smali` | `onStart()`          | App nunca exibe anúncio em tela cheia e desarma a logo ao retornar |

## Compilar
Volte para a pasta anterior e execute o Apktool para reconstruir o aplicativo:
```bash
cd ..
apktool b touch12i_src -j 2 -o touch12i_noads_unaligned.apk
```

Alinhe a APK para otimizar a estrutura do arquivo:
```bash
zipalign -p -v 4 touch12i_noads_unaligned.apk touch12i_noads.apk
```

## Assinar
Para que o Android aceite a instalação, é necessário assinar o arquivo APK. Para isso, crie uma chave:
```bash
keytool -genkey -v -keystore minha_chave.keystore -alias meu_alias -keyalg RSA -keysize 2048 -validity 10000
```
> Você pode preencher qualquer coisa nas perguntas ou apenas dar <kbd>Enter</kbd>, mas guarde a senha que escolher. No final escreva `yes` para finalizar a criação.

Assine a APK modificada:
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
Agora basta remover a instalação atual da calculadora:
```bash
adb uninstall co.epxx.touch12if
```

E instalar a nova versão:
```bash
adb install -i com.android.vending touch12i_noads.apk
```
> O parâmetro `-i com.android.vending` faz o Android registrar a APK como se tivesse sido instalada pela Play Store. Isso evita alertas de segurança e mantém o comportamento esperado pelo sistema.

## Conclusão
A partir deste ponto você pode voltar para o seu Android e abrir o aplicativo da calculadora normalmente e observar que nenhum anúncio será carregado ou exibido na interface. Não foram feitos testes para futuras atualizações da Play Store, por isso é bem provável que assim que o aplicativo receber uma atualização, os anúncios voltem, uma vez que as modificações feitas serão perdidas.

Para evitar que a Play Store atualize o app automaticamente e sobrescreva a sua versão modificada, siga os passos abaixo:

1. Abra a **Play Store**, procure pelo **TouchRPN** e entre na página do aplicativo.
2. Toque nos **três pontos (⋮)** no canto superior direito.
3. Desmarque a opção **"Atualizar automaticamente"**.

Por meio deste tutorial foi possível aprender como modificar, mesmo que de maneira simples, o bytecode de uma aplicação Android e então entender que é possível adaptar e estudar o código de uma aplicação android funcional. 
