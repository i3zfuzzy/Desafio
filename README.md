# Projeto de Monitoramento de Cotações de Moedas

Este é um sistema simples desenvolvido em Python com o framework Django que permite o monitoramento e exibição de cotações de moedas. O sistema utiliza a API do Vatcomply para coletar e exibir as cotações do dólar em relação ao real, euro e iene (JPY) em um gráfico interativo fornecido pelo Highcharts.

## Funcionalidades

- Consulta de cotações do dólar em relação ao real, euro e iene.
- Visualização das cotações em um gráfico interativo.
- Possibilidade de definir um intervalo de datas para consulta, respeitando um limite de até 5 dias úteis.

## Pré-requisitos

Certifique-se de ter o seguinte instalado:

- Python 3.x
- Django
- Biblioteca Highcharts

## Instalação e Configuração

1. Clone o repositório para o seu ambiente local.
2. Instale as dependências necessárias utilizando o `requirements.txt`.
3. Configure a API do Vatcomply de acordo com as instruções de documentação fornecidas.
4. Execute as migrações do Django para configurar o banco de dados.
5. Inicie o servidor local.

```bash
git clone https://github.com/SEU_USUARIO_DO_GITHUB/nome-do-repositorio.git
cd nome-do-repositorio
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Acesse o aplicativo em seu navegador via `http://localhost:8000` (ou a porta que você configurou).

## Estrutura do Projeto

- `app/` - Contém os arquivos relacionados à aplicação principal.
- `templates/` - Arquivos de template HTML para a renderização da página.

## Contribuição

Sinta-se à vontade para contribuir para o projeto. Basta seguir o fluxo padrão do Git para solicitações pull.

## Licença

Este projeto é licenciado sob a [MIT License](https://opensource.org/licenses/MIT).

---
Este é um projeto de exemplo e sua implementação pode variar dependendo das necessidades específicas e da arquitetura do sistema. Certifique-se de realizar testes e ajustes adicionais de acordo com seus requisitos específicos.