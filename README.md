# Gysin-IA: Assistente Virtual Humanizada

## Visão Geral
Gysin-IA é um projeto inovador que visa criar uma assistente virtual humanizada, integrada ao ChatGPT, com capacidade de memória para aprender sobre o usuário e se comunicar de forma natural.

## Características Principais
- Processamento de linguagem natural
- Análise de sentimento
- Geração de mapas mentais
- Sistema de memória e aprendizado contínuo
- Interface gráfica de usuário

## Requisitos
- Python 3.9+
- Bibliotecas: spacy, textblob, networkx, matplotlib, tkinter

## Instalação
1. Clone o repositório:git clone github.com
cd Gysin-IA
2. Crie e ative um ambiente virtual:
python -m venv venv
source venv/bin/activate # No Windows use venv\Scripts\activate
3. Instale as dependências:
pip install -e .
4. Baixe o modelo do spaCy para português:
python -m spacy download pt_core_news_sm
## Uso
Para iniciar a interface do usuário, execute:
python -m gysin_ia.interface.interface_usuario
## Estrutura do Projeto
```
gysin_ia/
├── core/
│ ├── language_model/
│ ├── memoria.py
│ └── mental_map_generator.py
├── interface/
│ └── interface_usuario.py
├── utils/
│ ├── exceptions.py
│ └── logger.py
├── tests/
├── config/
└── setup.py
```
## Desenvolvimento
- O projeto está em fase inicial de desenvolvimento.
- Contribuições são bem-vindas! Por favor, leia o arquivo CONTRIBUTING.md para detalhes sobre nosso código de conduta e o processo para enviar pull requests.

## Testes
Para executar os testes unitários:
python -m unittest discover tests
## Licença
Este projeto está licenciado sob a [MIT License](LICENSE).

## Contato
Stefano Gysin - stefanogysin@hotmail.com

Link do Projeto: [https://github.com/StefanoGysin/Gysin-IA](https://github.com/StefanoGysin/Gysin-IA)