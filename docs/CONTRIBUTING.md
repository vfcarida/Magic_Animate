# Guia de Contribuição

Bem-vindo ao projeto Magic Animate! Agradecemos o seu interesse em contribuir para o nosso repositório de animação de imagens baseada em difusão com MagicAnimate e DensePose.

Este guia orienta o processo de contribuição, as ferramentas de formatação, linting, cobertura de testes e fluxo de Pull Requests (PR). O nosso objetivo é manter o código sempre com a maior qualidade possível seguindo o padrão de projetos Open-Source modernos.

## Sumário

- [Como Contribuir](#como-contribuir)
- [Padrões de Código e Estilo](#padrões-de-código-e-estilo)
- [Testes](#testes)
- [Estrutura do Repositório](#estrutura-do-repositório)

---

## Como Contribuir

Siga os passos abaixo para submeter qualquer tipo de contribuição (correção de bugs, novas funcionalidades ou melhorias na documentação):

1. **Faça um Fork do repositório** e crie um clone local do seu fork.
2. **Crie uma branch** para a sua feature ou correção: `git checkout -b feature/minha-feature` ou `git checkout -b fix/meu-bug`.
3. Certifique-se de ter configurado o ambiente corretamente e instalado as dependências via `pip install -r requirements.txt`.
4. Implemente as suas mudanças. Caso crie novas funções, certifique-se de seguir o padrão SOLID.
5. Escreva testes para o seu novo código na pasta `tests/`.
6. Valide localmente se nada foi quebrado executando os testes (por exemplo, `pytest tests/`).
7. Faça o commit com mensagens claras (`git commit -m "feat: adicionado módulo xyz"`).
8. Faça push para a sua branch (`git push origin feature/minha-feature`) e crie um **Pull Request**.

---

## Padrões de Código e Estilo (Clean Code)

O repositório é escrito em Python e aderimos estritamente às normas da [PEP-8](https://peps.python.org/pep-0008/).

- **Type Hinting**: Sempre utilize [Type Hints](https://docs.python.org/3/library/typing.html) nas assinaturas de métodos e nas variáveis, quando possível.
- **Docstrings**: Todos os módulos, classes e funções devem ter [Docstrings](https://peps.python.org/pep-0257/) explicando seu propósito, argumentos e valor de retorno. O projeto segue o formato *Google* para docstrings.
- **Formatação Automática**: Recomendamos usar ferramentas como `black` e `isort` para formatar o código e `flake8` para verificação de estilo.

---

## Testes

Os testes são essenciais para aprovar um PR. Qualquer alteração lógica no backend deve ser acompanhada de testes unitários ou de integração na pasta `tests/`.

- Utilizamos a biblioteca padrão `unittest` ou `pytest`.
- Execute a bateria de testes localmente antes de submeter um Pull Request.

Agradecemos a sua contribuição!
