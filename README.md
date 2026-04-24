# 💸 Bot Financeiro Inteligente (Python)

Um bot em Python que entende linguagem natural para registrar e consultar gastos — com foco em futura integração com WhatsApp.

---

## 🚀 Funcionalidades

✔ Registro de gastos por texto
✔ Interpretação de linguagem natural
✔ Suporte a múltiplos formatos de frase
✔ Identificação automática de:

*  Valor (com ou sem centavos)
*  Data (`hoje`, `ontem`)
*  Categoria (alimentação, transporte, etc.)
*  Descrição (com limpeza automática)

✔ Normalização de texto (remoção de acentos)
✔ Filtragem de gastos:

* `ver gastos`
* `ver gastos hoje`
* `ver gastos ontem`
* `ver gastos alimentacao`

✔ Persistência de dados em arquivo JSON
✔ Execução contínua (modo chat no terminal)

---

##  Exemplos de uso

### Registrar gastos

```bash
hoje gastei 20 com netflix
ontem paguei 35 no mercado
comprei um lanche por 18
gastei 10 em uma farmacia
```

---

### Consultar gastos

```bash
ver gastos
ver gastos hoje
ver gastos ontem
ver gastos transporte
```

---

### Encerrar o bot

```bash
sair
```

---

##  Estrutura do projeto

```
 bot-financeiro
 ┣  main.py
 ┣  gastos.json
 ┗  README.md
```

---

##  Armazenamento

Os dados são salvos automaticamente no arquivo:

```bash
gastos.json
```

Exemplo:

```json
[
    {
        "descricao": "netflix",
        "valor": 20.0,
        "data": "2026-04-23",
        "categoria": "assinaturas"
    }
]
```

---
##  Tecnologias utilizadas

* Python 3
* Regex (`re`)
* Manipulação de strings
* `unicodedata` (normalização de texto)
* JSON (persistência de dados)
* Estruturas de controle (`while`, `if`, listas)

---

##  Aprendizados aplicados

* Interpretação de linguagem natural com regex
* Tratamento e limpeza de texto
* Estruturação de lógica para sistemas inteligentes
* Armazenamento de dados local
* Organização de código e fluxo contínuo

---

##  Próximos passos

* 📲 Integração com WhatsApp (API)
* ☁️ Persistência em banco de dados (Firebase)
* 📊 Relatórios automáticos
* ➕ Controle de receitas
* 🧾 Edição e exclusão de gastos
* 🤖 Uso de IA para melhorar interpretação

---

##  Objetivo

Este projeto faz parte da minha evolução como desenvolvedor, com foco em construir soluções reais que resolvem problemas do dia a dia.

---

##  Contribuição

Sinta-se à vontade para sugerir melhorias ou abrir issues.

---

## 🧑‍💻 Autor

Desenvolvido por **Magdyel Oliveira**

---

## ⭐ Se gostou do projeto

Deixe uma estrela no repositório e acompanhe a evolução 🚀
