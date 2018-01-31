# Portal Modelo: Componente para migração do Portal Modelo do 1 e 2 para o 3


## Introdução

Este pacote faz a migração do Portal Modelo versões 1 e 2 para a nova versão
3.0.

Ele é um pacote específico para o Portal Modelo e é pouco provável sua
utilização fora deste contexto.

## Procedimento de Migração

### Migração do Portal Modelo 3 

O Portal Modelo 2.0 foi criado utilizando a versão 2.5 do Plone, enquanto o Portal Modelo 3.0 é construído sobre a versão 4.3 do Plone. No período contido entre o lançamento do Portal Modelo 2 e do Portal Modelo 3 o Plone teve 8 versões e [http://plone.org/products/plone/releases/ 55 releases] e, para qualquer software, uma atualização com tantos passos intermediários torna-se complexa e deveria ser muito bem estudada.

É importante lembrar que a equipe de desenvolvimento do Plone tem dedicado um cuidado especial ao tópico da atualização de versões e que se estivéssemos falando apenas de conteúdos criados com os tipos de conteúdo padrão do Plone a migração entre as versões seria apenas uma questão de copiar a base do site antigo para o site novo e ativar o mecanismo de migração contido no próprio Plone.

Porém, o Portal Modelo 2 continha diversos produtos adicionais (de terceiros), como por exemplo o !PlonePopoll, CMFSin, !PloneGazette, Poi e etc, e estes foram descontinuados ou não possuem um mecanismo de migração completo e confiável. Isto, somado ao fato de que a própria arquitetura da informação do Portal Modelo 3 foi reestruturada, elimina uma migração utilizando apenas o mecanismo padrão do Plone.

A abordagem detalhada neste documento para realizar esta migração entre diferentes versões do Portal Modelo é a de exportarmos todo o conteúdo para um formato intermediário, realizar a serialização dos dados do portal como arquivos em formato ''[http://pt.wikipedia.org/wiki/JSON JSON]'' no sistema de arquivos, e realizar a importação dos mesmos em uma nova estrutura com o Portal Modelo 3 instalado, usando um mecanismo disponível nessa nova versão.


### Exportação dos Dados 

Para a realização da exportação dos dados de um Portal Modelo 2 existente, é preciso incluir mais dois pacotes Python na sua instalação: ''simplejson'' e ''collective.jsonify''. Vamos assumir neste tutorial que a instalação do Portal Modelo 2 foi feita através do seu [wiki:PortalModelo20 instalador padrão] e, portanto, há um Python independente só para o portal. Se for diferente disso, você deverá referenciar nos comandos abaixo o Python que roda o portal.

Como o Portal Modelo 2 utiliza o Python 2.4 é preciso garantir que a versão do ''simplejson'' seja a [https://pypi.python.org/pypi/simplejson/2.1.0 2.1.0], que é a compatível com esta versão do Python, e isto é feito durante a instalação do pacote, usando o comando ''easy_install'' do mesmo interpretador Python usado para a execução do portal. A versão do easy_install disponível no Python do Portal Modelo 2 é a 0.6 e, antes disso, será preciso atualizá-la para a 1.4.2, que é mais recente versão compatível com o Python 2.4:


```
$ cd /var/interlegis/PortalModelo-2.0/Python-2.4/bin
```
```
$ sudo ./easy_install -U 'setuptools==1.4.2'
```

Só então será possível instalar o '''simplejson''':

```
$ sudo ./easy_install -Z 'simplejson==2.1.0'
```

Caso o comando ''easy_install'' não esteja disponível, sua instalação deverá ser feita da seguinte maneira:

```
$ cd /tmp
$ wget --no-check-certificate https://bitbucket.org/pypa/setuptools/raw/bootstrap-py24/ez_setup.py
$ sudo python ez_setup.py
```

Para a instalação do pacote '''collective.jsonify''' é necessário [https://github.com/collective/collective.jsonify baixá-lo do repositório GitHub], descompactá-lo e então instalá-lo no mesmo interpretador Python do Portal Modelo 2:

```
$ mkdir /tmp/collective.jsonify
$ cd /tmp/collective.jsonify
$ wget --no-check-certificate https://github.com/collective/collective.jsonify/archive/master.zip
$ unzip master.zip
$ cd collective.jsonify-master
$ sudo /var/interlegis/PortalModelo-2.0/Python-2.4/bin/python setup.py install
```
Depois de instalado o pacote "coleective.jsonify", basta adicionar os itens get_item e get_children (external methods para acessos remotos) na raiz do local onde se encontra o Portal Modelo. 

Para isso, acesse a ZMI e adicione um External Method para o get_item e outro para o get_children. Nos dois casos o "Module Name" sera "json_methods" e o nome da função sera o mesmo do id. 

