# API Grade

Este projeto faz parte da Disciplina **Arquitetura de Software** da Pós-Graduação em Engenharia de Software da PUC-RIO.

O objetivo é criar uma aplicação que se comunique com componentes de mercado e desenvolvidos internamente.

A aplicação escolhida para este projeto é a Grade de Programação. Uma ferramenta útil para criação de grades de programação de canais de TV.

Grandes empresas de Mídia e Entretenimento (M&E) possuem necessidade de gerenciar a programação dos seus canais, sejam eles distribuídos por meio terreste (Over The Air - OTA) ou pela internet (Over The Top - OTT). Para fazer a gestão e gerar playlist de todos os conteúdos que irão passar em um canal é necessário ter uma ferramenta que crie a ordenação destes itens, como é o caso do **Grade** . Uma vez feita esta programação podemos consultar a base e buscar o planejamento dos itens para cada dia da semana.


## Como executar
Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.

Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

 É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Para criação de ambiente virtual, execute o seguinte comando:

```
python3 -m venv nome_do ambiente_virtual
```
Para ativar o ambiente virtual execute o seguinte comando:
```
source env/bin/activate
```
O comando a seguir instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.
```
(env)$ pip install -r requirements.txt
```
Após a criação do ambiente virtual e instalar os arquivos/bibliotecas de requirements.txt, basta executar a API com o seguinte comando:
```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução. Você será redirecionado para Swagger, onde terá acesso às documentações das APIs.

## Como executar através do Docker

Certifique-se de ter o **Docker** instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile no terminal e seus arquivos de aplicação e Execute como administrador o seguinte comando para construir a imagem Docker:

> $ docker build -t grade-backend .

Uma vez criada a imagem, para executar o container basta executar, como administrador, seguinte o comando:

> $ docker run -p 5000:5000 grade-backend

Uma vez executando, para acessar a API, basta abrir o http://localhost:5000/#/ no navegador.


## Como funciona o Back end

O Back end é composto por um banco de dados Sqlite3 com um tabela chamada **item_grade**. Ela guarda todos os itens de grade que foram cadastrados.
Para operações de leitura e escrita no banco foram criadas rotas, que estão escritas no arquivo principal do código (app.py).
foram criadas as seguintes rotas:

- **post item_grade**: Adiciona um novo item de grade no banco de dados;
-  **get itens_grade**: Retorna uma representação da listagem de itens de grade;
- **get item_grade**: Faz a busca por um item de grade a partir do ID do item;
- **get itens_grade/titulo**: Faz a busca pelos itens de grade a partir do título;
- **get itens_grade/data_exib**: Faz a busca pelos itens de grade a partir de uma data.
- **delete item_grade**: Exclui um item de grade a partir do ID do item;

## Melhoria Contínua  
  
Este trabalho é um MVP de pós-graduação. O objetivo principal aqui é aplicar os conhecimentos adquiridos no módulo de arquitetura de software, como micro serviços, padrões arquiteturais e conteinerização.

Alguns pontos foram identificados mas não foram tratados neste projetos. Segue proposta de melhorias para o correlation:

- Página de login.
- Página de Admin para gestão de acessos e perfis.
- Visualização gráfica da grade de programação (gráfico de GANTT).

## Sobre o autor 

O autor deste projeto é Wellington Melo (Ton Melo), Global MBA, engenheiro eletricista com especialização em engenharia de automação. No momento da criação deste projeto atuo líder do time de governança técnica na Globo e estou buscando conhecimento mais profundo em arquitetura e desenvolvimento de sistemas de TI.