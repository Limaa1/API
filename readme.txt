Instruções para uso execução da API:

1 - Rodar o programa ipget.py para pegar os ips de listar tor distintas e salva-las em um banco de dados, ressaltando que não será possível fazer o request 2 vezes dentro de 30 minutos devido limite imposto por uma das listas. Antes de realizar o request o programa irá limpar todos os dados na tabela selecionada.

2 - Criar a imagem docker para rodar o programa dentro do container e executá-lo. Todos os parâmetros para a criação da imagem já foram definidos no Dockerfile.

3 - Utilizar os endereços /main (endpoint get 1) e /ipativos (endpoint get 3) para visualização dos ips em html. 

4 - Para a utilização do método post, executá-lo em uma plataforma de API, como por exemplo o Postman,  para a inclusão de ips que não devem aparecer no endpoint get 3.

5 - Utilizar os endereços /get (endpoint get 1) e /ativos (endpoint get 3) para utilização dos endpoint get em json.

6 - Documentação está localizada em /swagger.