---
title: IBM, Red Hat e software livre: a visão de um velho louco
date: 2026-05-06
source: https://herebedragons.com.br/ibm-red-hat-e-software-livre-a-visao-de-um-velho-louco/
description: ""
tags: []
---

# IBM, Red Hat e software livre: a visão de um velho louco

_ 24 Nov, 2025  _

Várias pessoas opinaram sobre o recente anúncio da Red Hat de alterar as condições de venda do seu software

Aqui ficam algumas ideias de alguém que já anda por cá há muito tempo e que esteve no meio de muito do que aconteceu, e que esteve em muitos lados da cerca.

* * *

## História antiga para compreender

![1_hksj-RwVECrR5qWkeWgLvQ](https://bear-images.sfo2.cdn.digitaloceanspaces.com/paulogpd/1_hksj-rwvecrr5qwkewglvq.webp)

_Foto disponivel em https://www.lpi.org/pt-br/blog/2023/07/30/ibm-red-hat-and-free-software-an-old-maddogs-view/_

Comecei a programar em 1969. Escrevi os meus programas em cartões perfurados e utilizei FORTRAN enquanto estudante universitário do ensino cooperativo. Aprendi a programar lendo um livro e praticando. Esse primeiro computador era um IBM 1130 e foi a minha primeira exposição à IBM ou a qualquer empresa de computadores.

De volta à universidade, juntei-me à Digital Equipment User’s Society (DECUS), que tinha uma biblioteca de software escrito pelos clientes da DEC e distribuído pelo preço de uma cópia (por vezes em fita de papel e outras vezes em fita magnética).

Nessa altura, havia muito poucos “programadores profissionais”. De facto, tive um professor que ensinava programação que me disse que eu NUNCA conseguiria ganhar a vida como “programador profissional”. Quem escrevia código nessa altura era um físico, ou um químico, ou um engenheiro eletrotécnico, ou um professor universitário e precisava do código para fazer o seu trabalho ou para investigação.

Uma vez satisfeita a sua própria necessidade, pode ter contribuído com o programa para a DECUS, para que esta o distribuísse… porque vender software era difícil e não era isso que fazia para ganhar a vida.

De facto, não só era difícil vender software, como também não se podia ter direitos de autor sobre o software nem pedir patentes para o mesmo. A forma de proteger o seu código era através do “segredo comercial” e do “direito contratual”. Isto significava que ou se tinha de criar um contrato com cada um dos utilizadores ou se tinha de distribuir o software em formato binário. Distribuir o seu software em formato binário era “difícil”, uma vez que não existiam muitas máquinas de uma só arquitetura e, se tivessem um sistema operativo (e muitas não tinham), havia muitos sistemas operativos que funcionavam numa dada arquitetura.

Uma vez que havia tão poucos computadores de uma determinada arquitetura e, se tinham um sistema operativo, havia muitos sistemas operativos para cada arquitetura (o DEC PDP-11 tinha mais de onze sistemas operativos), muitas empresas distribuíam o seu software sob a forma de código-fonte ou até enviavam um engenheiro para o instalar, fazer testes e provar que funcionava. Depois, se o cliente recebesse o código-fonte do software, este era muitas vezes colocado sob custódia para o caso de o fornecedor falir.

Lembro-me de negociar um contrato para um compilador COBOL eficiente em 1975, em que a taxa de licença era de 100 000 USD para uma cópia do compilador que funcionava num mainframe IBM e podia ser utilizado para fazer uma compilação de cada vez. O engenheiro da empresa demorou alguns dias a instalar o compilador, a pô-lo a funcionar e a efetuar os testes de aceitação. Sim, os advogados da minha empresa mantiveram a fita do código-fonte sob custódia.

Muitos outros utilizadores/programadores distribuíram o seu código no “Domínio Público”, para que outros utilizadores pudessem fazer o que quisessem com ele.

* * *

## O início dos anos 80 mudou tudo isso

Com a aplicação de leis de direitos de autor rigorosas aos binários e ao código fonte. Isto foi necessário para os ROMs que estavam a ser utilizados em jogos e (mais tarde) para o software que estava a ser distribuído para os sistemas CP/M e MS DOS baseados em Intel.

Uma vez que o software tinha direitos de autor, os criadores de software precisavam de licenças para indicar aos outros utilizadores quais eram os seus direitos na utilização desse software.

Para os utilizadores finais, tratava-se do infame EULA (o “Contrato de Licença de Utilizador Final” que ninguém lê) e, para os programadores, de um contrato de código-fonte que era emitido e assinado em muito menor número.

* * *

## As origens e a ascensão da Unix™

O Unix foi criado pelos Bell Labs em 1969. Durante anos, foi distribuído apenas dentro dos Bell Labs e da Western Electric, mas acabou por escapar para algumas universidades de INVESTIGAÇÃO, como a Universidade da Califórnia em Berkeley, o MIT, Stanford, CMU e outras, para que professores e alunos pudessem estudar e “brincar” com ele. Estas universidades acabaram por obter uma licença de código fonte para todo o campus por uma quantia extremamente pequena, e o código foi distribuído livremente entre elas.

A Universidade da Califórnia, em Berkeley, era a única entre essas universidades. Aninhada nas altas sequóias de Berkeley, Califórnia, com um clima maravilhoso, perto da vida cosmopolita e descontraída de São Francisco, foi uma das universidades que Ken Thompson escolheu para pegar numa fita magnética do UNIX e utilizá-la para ensinar a conceção de sistemas operativos a jovens estudantes ansiosos. Eventualmente, os estudantes e a equipa, trabalhando com Ken, conseguiram criar uma versão do UNIX que poderia ser considerada melhor do que o sistema UNIX da AT&T. O BSD Unix exigia memória virtual paginada, enquanto a AT&T ainda usava o modelo de memória swapping. Eventualmente, o BSD Unix tinha TCP/IP nativo, enquanto o AT&T UNIX só tinha uucp. O BSD Unix tinha um rico conjunto de utilitários, enquanto a AT&T tinha reduzido a base de utilitários na transição do System IV para o System V.

É por isso que muitas das primeiras empresas de Unix, incluindo a Sun Microsystems (com o SunOS), a DEC (com o Ultrix) e a HP (com o HP/UX), optaram por uma base BSD para os seus produtos exclusivamente binários.

Outro pormenor interessante da história foi John Lions. John era professor na Universidade de New South Wales, na Austrália, e estava muito interessado no que estava a acontecer nos Laboratórios Bell.

John tirou uma licença sabática em 1978 e viajou para os Bell Labs. Trabalhando em conjunto com Ken Thompson, Dennis Ritchie, Doug McIlroy e outros, escreveu um livro sobre a versão 6 do Unix que comentava todo o código-fonte do kernel do Unix e um comentário sobre a razão pela qual esse código tinha sido escolhido e o que fazia. Infelizmente, em 1979, o licenciamento do Unix foi alterado e John não pôde publicar o seu livro durante mais de vinte anos.

Infelizmente para a AT&T, o John tinha tirado fotocópias de rascunhos do seu livro e tinha-as dado aos seus alunos para comentários, perguntas e revisão. Quando o livro de John deixou de ser publicado, os alunos fizeram fotocópias do seu livro, e fotocópias das fotocópias, e fotocópias das fotocópias das fotocópias, cada uma delas tornando-se ligeiramente mais leve e difícil de ler do que a geração anterior.

Durante anos os programadores Unix mediram a sua “idade” na comunidade Unix pela geração do livro do John que possuíam. Tenho orgulho em dizer que tenho uma terceira geração de fotocópias.

Os esforços de John ensinaram a milhares de programadores como funcionavam os elementos do kernel Unix e os padrões de pensamento de Ken e Dennis no desenvolvimento do sistema.

> Eventualmente o livro do John foi lançado para publicação, e pode comprá-lo e lê-lo você mesmo. Se desejar, pode correr uma cópia da versão 6 do Unix num simulador chamado SIMH que corre em Linux. Pode ver como era uma versão inicial do Unix.

Eventualmente, algumas empresas comerciais também obtiveram licenças de código fonte da AT&T ao abrigo de contratos muito dispendiosos e restritivos. Esta licença dispendiosa foi também utilizada por pequenas escolas que não eram consideradas universidades de investigação. Eu sei, pois o Hartford State Technical College era uma dessas escolas e não consegui obter o Unix para os meus alunos no período de 1977 a 1980. Não só se tinha de pagar uma quantia astronómica pela licença, como se tinha de dizer à Bell Labs o número de série da máquina em que se ia colocar o código fonte. Se essa máquina se avariasse, tinha de ligar para os Bell Labs e dizer-lhes o número de série da máquina para onde ia transferir o código fonte.

Eventualmente, algumas empresas, como a Sun Microsystems, negociaram um acordo de redistribuição com a AT&T Bell Labs para vender cópias apenas binárias de sistemas do tipo Unix a uma taxa de licenciamento muito menos restritiva e muito menos dispendiosa do que obter o código-fonte diretamente da AT&T Bell Labs.

Eventualmente, estas empresas tornaram a redistribuição de sistemas do tipo Unix a sua forma normal de fazer negócios, uma vez que para distribuir o código-fonte derivado da AT&T aos seus clientes era necessário que o cliente tivesse uma licença de código-fonte da AT&T, que ainda era muito cara e muito difícil de obter.

Devo salientar que estas empresas não se limitaram a pegar no código da AT&T, a recompilar o código e a distribuí-lo. Contrataram muitos engenheiros e fizeram muitas alterações ao código da AT&T. Contrataram muitos engenheiros e fizeram muitas alterações ao código AT&T e algumas delas decidiram utilizar o código da Universidade da Califórnia em Berkeley como base dos seus produtos, tendo depois alterado o código com os seus próprios engenheiros. Muitas vezes, isto significava não só alterar elementos do kernel, mas também alterar os compiladores para se adaptarem à arquitetura e outras partes importantes do trabalho de engenharia.

* * *

## O projeto GNU

No início dos anos 80, Richard M. Stallman (RMS), um estudante do MIT, recebeu uma distribuição do Unix apenas em formato binário. Embora o MIT tivesse uma licença para todo o site do código fonte da AT&T, a empresa que fez essa distribuição para o seu hardware não vendia fontes facilmente e RMS ficou chateado por não poder alterar o SO para fazer as alterações de que precisava.

Assim, a RMS iniciou o projeto GNU (“GNU is not Unix”) com o objetivo de distribuir um sistema operativo livre que exigiria que as pessoas que distribuíssem binários se certificassem de que as pessoas que recebessem esses binários receberiam as fontes e a capacidade de corrigir erros ou fazer as revisões necessárias.

O RMS não tinha uma equipa de pessoas para o ajudar a fazer isto, nem tinha milhões de dólares para gastar em hardware e pessoal de testes. Assim, ele criou uma comunidade de pessoas em torno do projeto GNU e (mais tarde) da Free Software Foundation. Nós chamaremos esta comunidade de comunidade GNU (ou “GNU”) no resto deste artigo.

A RMS tinha um plano interessante, que consistia em criar software útil para as pessoas que o utilizavam numa grande variedade de sistemas operativos.

A primeira peça de software foi o emacs, um poderoso editor de texto que funcionava em todos os sistemas operativos e, à medida que os programadores o utilizavam, apercebiam-se do valor de utilizar os mesmos subcomandos e teclas em todos os sistemas em que trabalhavam.

Depois o GNU trabalhou num conjunto de compiladores, depois em utilitários. Todos os projetos foram úteis para os programadores, que por sua vez tornaram outras peças de código úteis para eles.

Em que é que o GNU não trabalhou? Um pacote de escritório. Poucos programadores gastaram muito tempo trabalhando em documentos de escritório.

* * *

## Licenças permissivas

Entretanto, estava a ser dada resposta a outra necessidade. As universidades que estavam a fazer investigação informática estavam a gerar código que precisava de ser distribuído.

O MIT e a Universidade da Califórnia em Berkeley estavam a gerar código que não queriam vender. Idealmente, queriam dá-lo para que outras pessoas o pudessem utilizar na investigação. No entanto, o software estava agora protegido por direitos de autor, pelo que estas universidades precisavam de uma licença que dissesse às pessoas o que podiam fazer com esse código protegido por direitos de autor. Mais importante ainda, na perspetiva da universidade, a licença também dizia aos utilizadores do software que não havia qualquer garantia de utilidade e que não deviam esperar apoio, nem a universidade podia ser responsabilizada por quaisquer danos resultantes da utilização do software.

Na altura, brincámos que as licenças nem sequer garantiam que os sistemas em que se colocava o software não se incendiassem e ardessem em chamas. Isto foi dito em tom de brincadeira, mas era uma consideração real.

Estas licenças (e outras mais) acabaram por ficar conhecidas como as licenças “permissivas” do Código Aberto, uma vez que faziam poucas exigências aos utilizadores do código fonte do software, conhecidos como “programadores”. Os programadores eram livres de criar distribuições apenas de binários e passar os binários aos utilizadores finais sem terem de tornar o código fonte (para além do código que receberam originalmente ao abrigo da licença) visível para o utilizador final.

Apenas a licença “restritiva” da GPL obrigava o programador a tornar as suas alterações visíveis para os utilizadores finais que recebiam os seus binários.

* * *

## Inicialmente, havia muita confusão em torno das diferentes licenças

Algumas pessoas pensaram que os binários criados pela utilização dos compiladores GNU também estavam cobertos pela GPL, apesar de as fontes que geraram as licenças serem completamente livres de qualquer licenciamento (ou seja, criadas pelo próprio utilizador).

Algumas pessoas pensavam que não se podia vender código licenciado GPL. A RMS refutou esse facto, mas admitiu que o código licenciado sob GPL significava normalmente que vender o código por grandes quantias de dinheiro era “difícil” por muitas razões.

No entanto muitas pessoas venderam o código. Empresas como a Walnut Creek (Bob Bruce) e a Prime Time Freeware for Unix (Richard Morin) vendiam compêndios de código organizados em CD-ROMs e (mais tarde) DVDs por dinheiro. Enquanto os programas que estavam nesses compêndios eram cobertos por licenças individuais de “Código Aberto”, o CD ou DVD inteiro poderia ter seu próprio copyright e licença. Mesmo que fosse “legal” copiar toda a ISO e produzir os seus próprios CDs e DVDs e vendê-los, provavelmente os criadores dos originais poderiam ter tido pensamentos duros em relação aos revendedores.

* * *

## O mercado Unix e a ascensão da Microsoft

Durante todo este tempo, os fornecedores de sistemas, como a Digital Equipment Corporation, a HP, a Sun e a IBM, estavam todos a criar sistemas operativos do tipo Unix baseados no AT&T System V ou em parte da Berkeley Software Distribution (em muitos casos, a partir do BSD Unix 4.x). Cada uma destas empresas contratou um grande número de engenheiros de software Unix, pessoal de documentação, pessoal de garantia de qualidade, gestores de produto, etc. Tinham edifícios enormes, muitos advogados e vendiam as suas distribuições por muito dinheiro. Muitas eram “empresas de sistemas” que forneciam o software juntamente com o seu hardware. Algumas, como a Santa Cruz Operations (SCO), criaram apenas uma distribuição de software.

Inicialmente, estas empresas produziam os seus próprios sistemas operativos proprietários e vendiam-nos juntamente com o hardware, pois consideravam que o hardware sem um sistema operativo era praticamente inútil, mas mais tarde separaram as vendas de hardware das vendas de sistemas operativos para oferecerem aos seus clientes uma maior flexibilidade na combinação de funções para resolver os problemas dos clientes.

No entanto, isto significava normalmente mais custos, tanto para o hardware como para o sistema operativo separado. Além disso, era difícil diferenciar-se dos seus concorrentes externos e internos à sua empresa. Provavelmente, o mais famoso destes conflitos foi o sistema operativo VMS da DEC e as várias ofertas Unix…. e até o PDP-11 contra o VAX.

A DEC tinha mais de 500 pessoas (na sua maioria engenheiros e pessoal de documentação) no grupo Digital Unix, juntamente com engenharia periférica e gestão de produtos para produzir o Digital Unix.

Grosso modo, cada empresa gastava cerca de 1 a 2 mil milhões de dólares por ano para vender os seus sistemas, investindo em recursos informáticos sofisticados para mostrar que o seu sistema do tipo Unix era o melhor.

* * *

## A ascensão da Microsoft e a morte do Unix

Entretanto, uma empresa de software em Redmond, Washington, estava a produzir e a vender os mesmos sistemas operativos para correr no PC, independentemente de o comprarmos à HP, à IBM ou à DEC, e este sistema operativo estava agora a subir no mundo, dirigindo-se para o lucrativo mercado dos servidores de hardware. Embora houvesse obviamente menos servidores do que sistemas de secretária, o preço da licença de um sistema operativo de servidor podia rondar os 30 000 dólares ou mais.

O mercado Unix estava preso entre uma rocha e um lugar difícil. Estava a tornar-se demasiado dispendioso continuar a desenvolver sistemas únicos do tipo Unix e a competir não só com outros fornecedores do tipo Unix, mas também a lutar contra o Windows NT. Até a O’Reilly Publishers, que durante anos produziu livros sobre os subsistemas e comandos Unix, estava a passar a produzir livros sobre o Windows NT.

* * *

## A ascensão do Linux

Foi então que o projeto do kernel Linux entrou em cena. O projeto do kernel foi possibilitado por seis considerações principais:

  * Uma grande quantidade de software estava disponível em projectos GNU. MIT, BSD e projectos de software independentes
  * Uma grande quantidade de informação sobre os aspectos internos do sistema operativo estava disponível na Internet
  * A Internet de alta velocidade estava a chegar a casa, e não apenas à indústria e ao mundo académico
  * Processadores potentes e de baixo custo, capazes de memória virtual paginada a pedido, não só estavam disponíveis no mercado, como estavam a ser substituídos por sistemas mais potentes e, por conseguinte, estavam disponíveis para construir um kernel de “passatempo”.
  * Muita sorte e oportunidade
  * Um chefe de projeto excecionalmente teimoso e com muito carisma.



Tendo começado no final de 1991, no final de 1993 “o projeto kernel” e muitos criadores de distribuições como “Soft Landing Systems”, “Yggdrasil”, “Debian”, “Slackware” e “Red Hat” floresceram.

Alguns deles foram iniciados como uma distribuição “comercial”, com a esperança e o sonho de ganhar dinheiro, e outros foram iniciados como um “projeto comunitário” para beneficiar “a comunidade”.

Ao mesmo tempo, as distribuições que se baseavam na Berkeley Software Distribution continuavam a ser travadas pelo longo processo judicial “Unix Systems Labs Vs BSDi” que estava a impedir a criação do “BSDlite” que seria utilizado para iniciar as várias distribuições BSD.

O Linux (ou GNU/Linux, como alguns lhe chamavam) começou a ganhar força, impulsionado pelas muitas distribuições e pela imprensa (incluindo revistas e jornais).

* * *

## O Linux era pinguins giros

Admito que o que se segue são as minhas próprias ideias sobre a popularidade do Linux em relação ao BSD, mas, na minha perspetiva, foi uma combinação de muitos factores.

Como disse antes, no final de 1993, o BSD ainda estava a ser travado pelo processo judicial, mas as empresas Linux estavam a avançar e, por isso, as empresas BSD (que eram apenas uma ou duas na altura) não tinham nada de novo para dizer à imprensa.

Outra razão pela qual as distribuições Linux avançaram foi a diferença no modelo. A GPL teve um efeito dinâmico no modelo de forçar o código fonte a sair com os binários. Mais tarde, muitas pessoas dos sistemas embebidos, ou empresas que queriam um sistema operativo barato para o seu sistema fechado, poderiam escolher software com uma licença MIT ou BSD, licença essa que não os obrigaria a enviar todo o seu código fonte aos seus clientes, mas a combinação da GPL para o kernel e a grande quantidade de código da Free Software Foundation chamou a atenção de muita imprensa e clientes.

As pessoas podiam iniciar um projeto de distribuição sem pedir autorização a NINGUÉM, o que acabou por dar origem a centenas de distribuições.

* * *

## O sistema X Window e o Projeto Athena

Devo também mencionar o Projeto Athena no MIT, que era originalmente um projeto de investigação para criar uma atmosfera cliente-servidor leve para estações de trabalho Unix.

Deste projeto surgiu o Kerberos, um sistema de autenticação baseado na rede, bem como o X Window System.

Nessa altura, a Sun Microsystems tinha conseguido fazer do NFS uma “norma” na indústria Unix e estava a tentar defender um sistema de janelas baseado em Display Postscript chamado “News”.

Outras empresas estavam à procura de alternativas e o sistema X Window baseado em cliente-servidor era promissor. No entanto, o X10.3, uma versão do Projeto Athena, necessitava de mais algum desenvolvimento que acabou por dar origem ao X11.x e, para além disso, havia Intrínsecos e Widgets (caixas de botões, caixas de rádio, barras de deslocamento, etc.) que davam o “look and feel” que as pessoas vêem num sistema de desktop moderno.

Estas necessidades levaram a que o desenvolvimento do X Window System saísse do MIT e do Projeto Athena para o X Consortium, pessoas pagas a tempo inteiro para coordenar o desenvolvimento. O X Consortium era financiado por membros de empresas e pessoas que sentiam que tinham algo a ganhar com o apoio do X. O X Consortium abriu em 1993 e fechou as suas portas em 1996.

Algumas dessas mesmas empresas decidiram contrariar o Unix System Labs, o consórcio criado pela Sun Microsystems e pela AT&T, pelo que formaram a Open Software Foundation (OSF) e decidiram estabelecer uma norma de código-fonte e de API para os sistemas Unix. Criada em 1988, fundiu-se com a X/Open em 1996 para formar o Open Group. Atualmente, mantêm uma série de normas e certificações formais.

Foram formados muitos outros consórcios. O Common Desktop Environment (ainda tenho muitos conhecimentos sobre isso) foi um deles. E parecia sempre que os consórcios começavam, eram bem financiados, depois as empresas que os financiavam olhavam em volta e diziam “porque é que eu havia de pagar por isto, todas as outras empresas o vão fazer” e essas empresas desistiam e deixavam o financiamento do consórcio secar.

* * *

## De poucos para muitos

Até aqui, caro leitor, vimos como o software era originalmente escrito por pessoas que precisavam dele, enquanto os “programadores profissionais” escreviam código para outras pessoas e precisavam de financiamento para o tornar rentável para eles. O “problema” dos programadores profissionais é que eles esperam ganhar a vida a escrever código. Têm de comprar comida, habitação e pagar impostos. Podem ou não usar o código que escrevem na sua vida quotidiana.

Também vimos uma época em que os sistemas operativos, na sua maioria, eram escritos ou por empresas de computadores, para tornar os seus sistemas utilizáveis, ou por entidades educacionais como projectos de investigação. À medida que o Linux amadurece e as normas fazem com que o “PC” médio de um fornecedor se torne cada vez mais eletricamente igual, o número de engenheiros necessários para fazer com que cada distribuição do Linux funcione num “PC” é mínimo.

Normalmente, os PCs têm tido dificuldade em diferenciar-se uns dos outros e o “preço” é cada vez mais uma das questões atenuantes. Ter de pagar por um sistema operativo é algo que nenhuma empresa quer fazer, e poucos utilizadores esperam pagar por ele também. Por isso, os fornecedores de hardware voltam-se cada vez mais para o Linux…., um sistema operativo que não têm de pagar nada para colocar na sua plataforma.

Recentemente, tenho visto algumas fissuras no dique. À medida que mais e mais utilizadores de FOSS se juntam a nós, colocam mais e mais exigências aos programadores, cujo número não está a crescer suficientemente rápido para manter todo o software a funcionar.

Os programadores FOSS dizem-me que há muito poucos, e por vezes nenhum, programadores a trabalhar em blocos de código. É claro que isto também pode acontecer com o código de fonte fechada, mas esta escassez atinge sobretudo áreas que não são consideradas “sexy”, como a garantia de qualidade, a engenharia de lançamento, a documentação e as traduções.

* * *

## Financiamento dos trabalhos

No início, havia apenas algumas pessoas a trabalhar em projectos que tinham relativamente poucas pessoas a utilizá-los. Eram apaixonados pelo seu trabalho e ninguém era pago.

Uma das primeiras vezes que ouvi qualquer tipo de rumores foi quando algumas pessoas descobriram algumas formas de ganhar dinheiro com o Linux. Um rumor que surgiu foi uma indignação que veio porque os programadores não queriam que as pessoas ganhassem dinheiro com código que tinham escrito e contribuído gratuitamente.

Eu entendia os sentimentos dessas pessoas, mas eu defendia o facto de que se não permitíssemos que as empresas ganhassem dinheiro com o Linux, o movimento iria avançar lentamente, como um melaço frio. Permitir que as companhias ganhem dinheiro faria com que o Linux avançasse rapidamente. Enquanto nós perdemos alguns dos primeiros desenvolvedores que não concordavam com isso, a maioria dos desenvolvedores que realmente contavam (incluindo Linus) viram a lógica nisso.

Por esta altura, várias empresas estavam a olhar para o “Open Source”. A Netscape estava a lutar com outras empresas que estavam a criar browsers e, por outro lado, havia os servidores Web, como o Apache, que eram necessários para fornecer servidores.

Ao mesmo tempo, a Netscape decidiu “abrir o código fonte” do seu código, numa tentativa de atrair mais programadores e reduzir os custos de produção de um browser e servidor de classe mundial.

* * *

## A comunidade

Ao longo da história do software foram surgindo “comunidades”. Nos primeiros tempos, as comunidades giravam em torno de grupos de utilizadores, ou grupos de pessoas envolvidas em algum tipo de projeto de software, trabalhando em conjunto para um objetivo comum.

Por vezes, estas eram formadas em torno das empresas de sistemas (DECUS, SHARE da IBM, Sun Microsystems, Sun-sites, etc.) e, mais tarde, de bulletin boards, newsgroups, etc.

Com o tempo, a “comunidade” expandiu-se para incluir pessoas de documentação, pessoas de tradução ou mesmo pessoas que apenas promovem o Software Livre e o “Código Aberto” por várias razões.

No entanto, nos últimos anos, tornou-se cada vez mais uma questão de as pessoas usarem software gratuito e não compreenderem o Software Livre. As mesmas pessoas que usavam software pirata, sem dar qualquer retorno à comunidade ou aos programadores.

* * *

## Arrepia-me os cabelos

Uma das outras questões relacionadas com o software é o conceito de “pirataria de software”, a cópia e utilização ilegal de software contra a sua licença.

Ao longo dos anos, algumas pessoas da “Comunidade FOSS” têm menosprezado a ideia de Propriedade Intelectual e mesmo a existência de direitos de autor, sem reconhecerem que sem direitos de autor não teriam qualquer controlo sobre o seu software. O software no domínio público não tem qualquer proteção contra pessoas que peguem no software, lhe façam alterações, criem uma cópia binária e a vendam por qualquer preço que o cliente pague. No entanto, algumas destas pessoas que defendem o software livre toleram a pirataria e fecham os olhos a esta prática.

Eu não sou uma dessas pessoas. Lembro-me do dia em que reconheci o valor da luta contra a pirataria de software. Eu estava numa conferência no Brasil quando disse à audiência que eles deveriam usar Software Livre. Eles responderam e disseram:

> “Oh, Sr. maddog, TODO o nosso software é gratuito!”

Naquela época quase 90% de todo o software para desktop no Brasil era pirateado, e assim com a facilidade de se obter software de graça, parte da utilidade do Software Livre (seu baixo custo) foi obliterada.

Uma organização, a [Business] Software Alliance (BSA), foi criada por empresas como a Oracle, a Microsoft, a Adobe e outras para encontrar e processar (normalmente) empresas e agências governamentais que utilizavam software não licenciado ou incorretamente licenciado.

Se todas as pessoas que utilizam o kernel Linux pagassem apenas um dólar por cada plataforma de hardware onde está a ser executado, poderíamos facilmente financiar a maior parte do desenvolvimento FOSS.

* * *

## Entrar na IBM

Uma pessoa na IBM, de nome Daniel Frye, tornou-se o meu elo de ligação com a IBM. O Dan tinha compreendido o modelo e as razões para ter Código Aberto.

Como muitas outras empresas de computadores (incluindo a Microsoft), havia pessoas na IBM que acreditavam no FOSS e estavam a trabalhar em projectos no seu próprio tempo.

Um dos objectivos de Daniel era encontrar e organizar algumas destas pessoas numa unidade FOSS dentro da IBM para ajudar a fazer avançar o Linux.

De vez em quando, era convidado para ir a Austin, no Texas, para me reunir com a IBM (o que, como funcionário da DEC, era muito estranho).

Uma vez eu estava lá e o Dan pediu-me, como Presidente da Linux International™, para falar numa reunião destas pessoas do “grupo Linux”. Eu dei a minha palestra e fui então encaminhado para uma “sala verde” para esperar enquanto o resto da reunião continuava. Passado algum tempo, tive de ir à casa de banho e, enquanto procurava, vi uma carta a ser projectada no ecrã em frente de todas aquelas pessoas da IBM. Era uma carta de Lou Gerstner, na altura o presidente da IBM. A carta dizia, de facto, que no passado a IBM tinha sido uma empresa de código fechado, a não ser que existissem razões comerciais para ser de código aberto. No futuro, continuava a carta, a IBM seria uma empresa de código aberto, a menos que houvesse razões comerciais para ser de código fechado.

Esta carta causou-me arrepios nas costas, porque trabalhando na DEC, eu sabia como era difícil pegar num código escrito pelos engenheiros da DEC e torná-lo “software livre”, mesmo que a DEC não tivesse planos para vender esse código … .nenhum plano para o tornar disponível ao público. Depois de passar por este processo, os engenheiros da DEC disseram-me “nunca mais”. Esta declaração de Gerstner inverteu o processo. Cabia agora aos empresários provar porque é que não podiam tornar o código aberto.

Sei que haverá muita gente que me dirá que “nem pensar” que Gerstner disse isso. Citarão exemplos de como a IBM não é “aberta”. Dir-vos-ei que uma coisa é um Presidente e um Diretor Executivo tomarem uma decisão dessas e outra é uma grande empresa como a IBM implementá-la. É preciso tempo e é preciso um plano de negócios para que uma empresa como a IBM mude a sua atividade.

Foi por esta altura que a IBM fez o seu famoso anúncio de que ia investir mil milhões de dólares americanos no “Linux”. É possível que também tenham dito “Open Source”, mas perdi a noção do momento em que isso aconteceu. Este anúncio apanhou o mundo de surpresa, pelo facto de uma empresa de computadores tão grande e séria fazer esta declaração.

Um mês ou dois depois disto, Dan encontrou-se comigo novamente, olhou-me diretamente nos olhos e perguntou se a comunidade Linux poderia considerar a IBM a tentar “tomar conta do Linux”, se poderiam aceitar o “elefante dançante” a entrar na comunidade Linux, ou se teriam medo que a IBM esmagasse o Linux.

Disse a Dan que tinha a certeza de que as “pessoas que contavam” na comunidade Linux veriam a IBM como um parceiro.

Pouco tempo depois, apercebi-me de que a IBM estava a contratar programadores Linux para que pudessem trabalhar a tempo inteiro em várias partes do Linux, e não apenas a tempo parcial como anteriormente. Conheci pessoas que estavam a trabalhar em partes tão díspares do “Linux” como o Servidor Web Apache que eram pagas pela IBM.

Cerca de um ano depois, a IBM fez outra declaração. Tinham recuperado o investimento de mil milhões de dólares e iam investir mais mil milhões de dólares.

Estava num evento sobre Linux na cidade de Nova Iorque quando ouvi dizer que a IBM tinha vendido a sua divisão de computadores portáteis e de secretária à Lenovo. Eu sabia que, embora essa divisão ainda fosse rentável, não o era ao ponto de poder apoiar a IBM. Por isso, a IBM vendeu essa divisão, comprou a Price Waterhouse Cooper (duplicando o tamanho do seu departamento de integração) e direccionou os seus esforços para a criação de soluções empresariais, que ERAM mais rentáveis.

Havia ainda uma outra questão, mais subtil. Antes desse anúncio, literalmente um dia antes do anúncio, se um vendedor da IBM tivesse usado qualquer coisa que não fosse hardware IBM para criar uma solução, poderia ter havido um inferno para pagar. No entanto, nesse evento Linux, foi anunciado que a IBM estava a oferecer dois computadores portáteis da Apple como prémios num concurso. As implicações desse prémio não me passaram despercebidas. Dois dias antes desse anúncio, se o pessoal de marketing da IBM tivesse oferecido um prémio de um produto que não fosse da IBM, provavelmente teriam sido despedidos.

No futuro, uma solução comercial da IBM poderá utilizar QUALQUER hardware e QUALQUER software, não apenas o da IBM. Isto foi fantástico. E mostrou que a IBM estava a apoiar o Open Source, porque o Open Source permitia aos seus fornecedores de soluções criar melhores soluções a um custo mais baixo. É tão simples quanto isso.

A Lenovo, com as suas despesas gerais mais reduzidas e a sua atividade concentrada, poderia facilmente obter um lucro razoável com esses sistemas de gama baixa, especialmente quando a IBM pode ser um bom cliente.

A IBM já não era uma “empresa de computadores”. Era uma empresa de soluções empresariais. Mais tarde, a IBM vendeu a sua divisão de pequenos servidores à Lenovo, praticamente pela mesma razão.

Assim, quando a IBM quis fornecer uma solução de código aberto para as suas soluções empresariais, que distribuição iria adquirir? A Red Hat.

* * *

## E depois havia o SCO

Mencionei anteriormente a “SCO” como uma distribuição de Unix que era muito parecida com a Microsoft. A SCO criou distribuições, na sua maioria baseadas no código AT&T (em vez do Berkeley) e até assumiu a distribuição do Xenix da Microsoft quando esta deixou de o querer distribuir.

As Operações de Santa Cruz, localizadas nas montanhas de Santa Cruz, com vista para a bela Baía de Monterey.

Fundada por uma equipa de pai e filho, Larry e Doug Michels, tinha um grande grupo de programadores e provavelmente distribuiu mais licenças para Unix do que qualquer outro fornecedor. Especializaram-se em sistemas de servidores que conduziam muitos hotéis, restaurantes, etc., utilizando terminais de células de caracteres e, mais tarde, X-terms e afins.

O Doug, em particular, é um tipo porreiro. Foi o Doug, quando fazia parte do Conselho de Administração do Uniforum, que INSISTIU em que fosse atribuído a Linus um prémio “Lifetime Achievement”, com a tenra idade de 27 anos.

Trabalhei com o Doug em vários projectos, incluindo o Common Desktop Environment (CDE) e gostei de trabalhar com os seus colaboradores.

Mais tarde Doug e Larry venderam a SCO para o Caldera Group, criadores do Caldera Linux. Com sede em Utah, a equipa da Candera era um spin-off da Novell. Pelo que pude ver, a Caldera não estava muito interessada no Linux “FreeDOM” mas sim em ter um “Unix barato” livre de royalties da AT&T, mas ainda usando código da AT&T. Eles continuamente buscaram acordos com software de código fechado que eles poderiam ligar em sua distribuição Linux para dar valor.

Esta compra formou a base do que ficou conhecido como “Bad SCO” (quando a Caldera mudou o seu nome para “SCO”), e que rapidamente adoptou uma tática comercial de processar os vendedores de Linux porque a “SCO” dizia que o Linux tinha código fonte da AT&T e era uma violação dos seus termos de licenciamento.

Isto causou um grande alvoroço no Mercado Linux, com as pessoas sem saber se o Linux deixaria de ser distribuído.

É claro que a maioria de nós na comunidade Linux sabia que esses desafios eram falsos. Uma das afirmações que a SCO fez foi que eles possuíam os direitos autorais do código da AT&T. Eu sabia que isto era falso porque li o acordo entre a AT&T e a Novell (a DEC era uma licenciada de ambas, por isso partilharam o contrato connosco) e sabia que, no máximo, a Santa Cruz Operations tinha o direito de sub-licenciar e cobrar royalties….mas admito que o contrato era muito confuso.

No entanto, ninguém sabia quem iria financiar a ação judicial que iria ocorrer em breve.

A IBM entrou no bar (tal como a Novell, a Red Hat e várias outras) e, durante os anos seguintes, a batalha legal prosseguiu com a SCO a apresentar queixa em tribunal e os “bons da fita” a derrubá-las. Pode ler mais sobre este assunto na Wikipedia.

No final, os tribunais consideraram que, no máximo, a SCO tinha um problema com a própria IBM sobre um contrato extinto, e o Linux estava livre.

Mas sem a IBM, a comunidade Linux poderia estar em apuros. E o facto de a “Big Blue” estar na batalha deu a muitos vendedores e utilizadores de Linux a confiança de que as coisas iriam correr bem.

* * *

## Red Hat e RHEL

Agora chegamos à Red Hat e ao seu percurso.

Conheci a Red Hat na altura em que Bob Young se apercebeu de que a maior parte dos CDs que a sua empresa tinha no seu corpo de ACC eram desta pequena empresa em Raleigh, Carolina do Norte.

Bob viajou até lá e encontrou três programadores que eram excelentes do ponto de vista técnico, mas não eram os mais fortes do ponto de vista comercial e de marketing.

Bob comprou a empresa e ajudou a desenvolver as políticas da empresa. Defendeu servidores maiores, mais conetividade com a Internet, de modo a distribuir mais cópias do Red Hat. Foi Bob que salientou que “o Linux é catsup, e eu vou fazer com que o Red Hat™ seja igual ao “Heinz™”.

A Red Hat desenvolveu o modelo de negócio de venda de serviços e tornou-se rentável com esse objetivo. Eventualmente, a Red Hat saiu com uma das IPOs mais lucrativas da época.

A Red Hat passou por uma série de presidentes, cada um deles com as competências necessárias na altura, até que finalmente as necessidades da IBM corresponderam aos desejos dos accionistas da Red Hat.

Não é segredo que a Red Hat não se importava com o desktop, a não ser como uma plataforma de desenvolvimento para o RHEL. Eles desistiram de seu desenvolvimento de desktop para o Fedora. A Red Hat preocupava-se com a empresa, com as empresas que estavam dispostas a pagar preços elevados pelo suporte que a Red Hat lhes ia vender com a garantia de que os clientes teriam o código-fonte no caso de precisarem dele.

Essas empresas levam a sério sua necessidade de computadores, mas não querem fazer o investimento em funcionários para oferecer o nível de suporte de que precisam. Por isso, pagam à Red Hat. Mas a maioria dessas empresas tem Apple ou Microsoft no desktop e não se importam em ter o Fedora lá. Eles querem que o RHEL seja sólido e tenha esse telefone pronto, e estão dispostos a pagar por isso.

As alternativas são comprar uma solução de código fechado e lutar para obter o código fonte quando precisar dele ou negociar (numa base de servidor) uma solução que não é uma solução de sistema de hardware/software necessária para a IBM.

* * *

## Empresas de sistemas “Full Stack” versus outras

Há alguns anos, a Oracle tomou a decisão de comprar a propriedade intelectual da Sun Microsystems. É claro que os seus produtos funcionavam em muitos sistemas operativos diferentes, mas a Oracle percebeu que, se tivesse o controlo total do hardware, do sistema operativo e da base de aplicações (neste caso, o seu principal motor de base de dados Oracle), criaria a “Oracle imparável”.

Porque é que uma empresa de sistemas full-stack é preferível? Pode fazer alterações e correcções à pilha completa que beneficiam as suas aplicações e não tem de convencer/cajúlar/argumentar com as pessoas para as introduzir. Da mesma forma, pode testar a pilha completa para detetar ineficiências ou pontos fracos.

Já trabalhei para empresas “full-stack”. Nós suportávamos o nosso próprio hardware. Os controladores de dispositivos que escrevemos tinham diagnósticos que o sistema operativo podia tornar visíveis para os administradores de sistemas, para lhes dizer que os dispositivos estavam prestes a falhar e para permitir que esses dispositivos fossem trocados. Criámos funcionalidades no sistema que beneficiaram os nossos produtos de bases de dados e os nossos produtos de rede. As coisas podiam ser mais simples.

A IBM é uma empresa full-stack. A Apple é uma empresa full-stack. Os seus produtos tendem a ser mais caros, mas muitas pessoas sérias pagam mais por eles.

* * *

## Por que as empresas pagariam para usar o RHEL?

Certas empresas (aquelas a que chamamos “empresas”) não são universidades ou amadores. Essas empresas (e governos) utilizam termos como “missão crítica” e “sempre ativo”. Normalmente, não medem o seu número de computadores em dezenas ou centenas, mas em milhares…. e precisam deles para funcionar bem.

Falam de “Tempo médio até à falha” (MTTF) e de “Tempo médio até à reparação” (MTTR) e querem ter “Termos de Acordos de Serviço” (TSA) que falam de tantas horas de tempo de atividade que são garantidas (99,999% de tempo de atividade) com penalizações se não forem cumpridas. E, como regra geral, as empresas de informática sabem que, por cada “9” à direita da vírgula decimal, é necessário investir 100 vezes mais trabalho e despesas para lá chegar.

E, normalmente, nestes “Termos de Serviço” também se fala do número de “Pontos de Contacto” que existem entre o cliente e o fornecedor de serviços. Quanto menor for o número de “pontos de contacto”, menor será o custo do contrato, porque o “ponto de contacto” fornecido pelo cliente terá mais conhecimentos sobre o sistema e o problema do que o utilizador médio.

Além disso, nestes contratos, o cliente não recorre ao que nós, no sector, chamamos “apoio de primeira linha”. O cliente já aplicou todos os patches, reiniciou o sistema e certificou-se de que o rato está ligado. Por isso, o cliente telefona para um número especial e recebe a segunda ou terceira linha de apoio.

Por outras palavras, pessoas sérias. Pessoas muito sérias. E essas pessoas muito sérias estão dispostas a gastar dinheiro muito sério para o conseguir.

Trabalhei tanto para as empresas que queriam comprar esses serviços como para as empresas que precisavam de os prestar.

Muitas pessoas compreenderão que quanto maior for o número de sistemas sob contrato, maior será o número de problemas. Do mesmo modo, quanto maior for o número de sistemas sob contrato, menor será o custo da prestação de serviços por sistema, se for distribuído uniformemente por todos os clientes e sistemas que necessitam desse apoio empresarial.

A IBM tem sido normalmente uma das empresas que presta um apoio realmente sério.

* * *

## Ligar tudo

A IBM ainda tinha muitos sistemas operativos e soluções que utilizava no seu negócio de soluções empresariais, mas precisava de uma solução Linux que pudesse utilizar como uma solução de pilha completa, tal como a Oracle fazia. Dando à IBM a capacidade de integrar o hardware, o sistema operativo e as soluções para se adaptar melhor ao cliente.

Do mesmo modo, a Red Hat Software, com a sua solução RHEL, tinha a reputação e a engenharia necessárias para fornecer uma solução empresarial.

A Red Hat tinha-se concentrado em servidores empresariais, ao contrário de outras distribuições bem conhecidas, com a sua versão comunitária “Fedora” a atuar como uma base experimental para novas ideias a serem integradas no RHEL mais tarde. No entanto, o RHEL era o foco de negócios da Red Hat.

Também deve ser apontado que algumas partes do software vieram apenas da Red Hat. Havia poucas “pessoas da comunidade” que trabalharam em algumas partes da distribuição chamada “RHEL”. Então, enquanto muitas das peças foram protegidas por direitos autorais e lançadas sob alguma versão da GPL, muitas contribuições que compunham o RHEL vieram apenas da Red Hat.

A Red Hat também tinha uma boa reputação na comunidade Linux, libertando todo o seu código fonte para a comunidade em geral e cobrando pelo suporte.

No entanto, com o passar do tempo, alguns clientes desenvolveram um padrão de comprar um pequeno número de sistemas RHEL, e então usar a versão compatível “bug-for-bug” do Red Hat de alguma outra distribuição. Isso, é claro, economizava o dinheiro do cliente, mas também reduzia a quantidade de receita que a Red Hat recebia pela mesma quantidade de trabalho. Isso forçou a Red Hat a cobrar mais por cada licença vendida, ou demitir funcionários da Red Hat, ou não fazer projetos que poderiam ter financiado de outra forma.

Então, recentemente, a Red Hat/IBM tomou uma decisão de negócios para limitar seus clientes àqueles que comprariam uma licença deles para cada sistema que rodaria RHEL e apenas distribuir seu código-fonte e as informações necessárias sobre como construir essa distribuição para esses clientes. Assim, as pessoas que recebessem esses binários receberiam os códigos-fonte para poderem corrigir bugs e alargar o sistema operativo como desejassem…… Esta era, e é, a essência da GPL.

A maioria, se não todos, os artigos que li diziam algo como “A IBM/Red Hat parece estar a seguir a GPL… mas… mas… mas… a comunidade!”.

Que comunidade? Existem muitas distribuições para pessoas que não precisam do mesmo nível de engenharia e suporte que a IBM e a Red Hat oferecem. A Red Hat, e a IBM, continuam a enviar as suas alterações ao código GPL “upstream” para fluir para todas as outras distribuições. Continuam a partilhar ideias com a comunidade em geral.

Nos primeiros dias do porte DEC Linux/alpha eu usei Red Hat porque eles eram a única distribuição que trabalhava junto com a DEC para colocar os bits. Mais tarde outras distribuições seguiram para o Alpha a partir do trabalho que a Red Hat tinha feito. Francamente, eu nunca usei “RHEL” e não uso Fedora há muito tempo. Preferência pessoal.

No entanto, vejo agora muita gente a sair da toca e a bater no peito e a dizer que vão proteger o investimento das pessoas que querem usar o RHEL gratuitamente.

Eu vi desenvolvedores de várias distribuições fazerem camisetas declarando que eles não são “Freeloaders”. Não sei quem terá chamado “freeloader” a qualquer um dos criadores do CentOS ou do Rocky Linux, do Alma ou de qualquer outro “clone” de qualquer outra distribuição. Eu já criei distribuições suficientes no meu tempo para saber que fazer isso não é “de graça”. É preciso trabalho.

No entanto, direi que há muitas pessoas que usam esses clones e não retribuem à comunidade de nenhuma maneira, forma ou jeito que eu considero “aproveitadores”, e que provavelmente seriam as pessoas que assinam um acordo comercial com a IBM/Red Hat e depois não querem cumprir esse acordo. Para esses aproveitadores, existem muitas outras distribuições de Linux que ficariam “felizes” em tê-los usando suas distribuições.

* * *

## Uma nota pessoal

Como afirmei acima, estive na comunidade “Open Source” antes de existir Open Source, antes de existir a Free Software Foundation, antes de existir o projeto GNU.

Tenho 73 anos de idade e passei mais de 50 anos na “comunidade”. Tenho marcas de chicote nas costas por promover o código-fonte e fornecer fontes mesmo quando poderia ter sido despedido ou levado a tribunal por isso, porque o cliente precisava. A maioria das pessoas que se riram de mim por apoiar o Linux quando eu trabalhava para o Digital Unix Group estão agora a trabalhar para empresas Linux. Isso é bom. Tenho uma pele grossa, mas as marcas do chicote ainda estão lá.

Há muitas maneiras de ajudar a construir esta comunidade que não têm nada a ver com a capacidade de escrever código, escrever documentação ou até mesmo gerar um relatório de erros razoável.

Simplesmente promover o Software Livre nas suas escolas, empresas, governos e compreender a comunidade seria um longo caminho. Começar um Clube Linux (lpi.org/clubs) na sua escola ou ajudar outros a atualizar para Linux (upgradetolinux.com) são formas de os utilizadores de Linux (quer sejam indivíduos, empresas, universidades ou governos) poderem contribuir para a comunidade.

Mas muitos dos parasitas nem sequer o fazem.

Até agora vi quatro distribuições diferentes a dizer que vão continuar a produção de “não RHEL”, gerando ainda mais distribuições para o utilizador médio dizer “qual devo usar”? Se eles realmente querem fazer isso, por que não trabalhar juntos para produzir uma boa distribuição? Por que não fazer de suas próprias distribuições um concorrente do RHEL? Por quanto tempo eles vão continuar batendo no peito quando descobrirem que não podem ganhar dinheiro fazendo isso?

A SuSE disse que iria investir dez milhões de dólares no desenvolvimento de um concorrente do RHEL. Fantástico! COMPETE. Crie um concorrente empresarial para a Red Hat com os mesmos canais de negócios, equipa de suporte mundial, etc. etc. Descobrirá que não é barato fazer isso. Dez milhões podem ser suficientes para começar.

Minha resposta para tudo isso? Os clientes RHEL terão de decidir o que querem fazer. Tenho certeza de que a IBM e a Red Hat esperam que seus clientes vejam o valor do RHEL e o suporte que a Red Hat/IBM e seus parceiros de canal fornecem para ele.

O resto dos clientes que apenas querem comprar uma cópia do RHEL e depois correr uma distribuição “livre” em todos os seus outros sistemas, independentemente da forma como é criada, bem, parece que a IBM já não quer fazer negócio com eles, pelo que terão de recorrer a outros fornecedores que tenham distribuições de Linux com capacidade empresarial e que possam tolerar esse tipo de clientes. Gostaria também de salientar que a IBM e a Red Hat apresentaram um conjunto de condições comerciais aos seus clientes, que são livres de as aceitar ou rejeitar. Depois, a IBM e a Red Hat são livres de criar outro conjunto de condições comerciais para outro conjunto de clientes.

Quero que as pessoas saibam que não tenho qualquer ódio por pessoas e empresas que estabelecem condições comerciais, desde que não violem as licenças que lhes são concedidas. Negócios são negócios.

No entanto, gostaria de salientar que, por mais “maléficas” que a Red Hat e a IBM tenham sido retratadas nesta mudança de negócio, não há qualquer menção a todas as empresas que apoiam as “Licenças Permissivas” de Código Aberto, que não garantem as fontes aos seus utilizadores finais, ou que oferecem apenas Licenças de “Código Fechado”….que não permitem e nunca permitiram que se fizessem clones….estas pessoas e empresas não têm qualquer direito de atirar pedras (e vocês sabem quem são).

A Red Hat e a IBM estão a disponibilizar as suas fontes a todos aqueles que recebem os seus binários ao abrigo de um contrato. Essa é a GPL.

Para todos os pesquisadores, estudantes, amadores e pessoas com pouco ou nenhum dinheiro, existem literalmente centenas de distribuições que podem escolher, e muitas que funcionam noutras arquitecturas interessantes que o RHEL nem sequer aborda.

* * *

**Jon “maddog” Hall** é Presidente Emérito do Conselho do Linux Professional Institute. Desde 1969, o Sr. Hall tem atuado como programador, projetista de sistemas, administrador de sistemas, gerente de produto, gerente de marketing técnico, autor e educador, atualmente trabalhando como consultor independente. O Sr. Hall tem se concentrado em sistemas Unix desde 1980 e em sistemas Linux desde 1994, quando conheceu Linus Torvalds e reconheceu corretamente a importância comercial do Linux e do software livre e de código aberto. Como Diretor Executivo da Linux International™, o Sr. Hall viajou o mundo falando sobre os benefícios do software de código aberto. Ele é bacharel em Comércio e Engenharia pela Universidade Drexel e mestre em Ciência da Computação pelo RPI, em Troy, Nova York.
