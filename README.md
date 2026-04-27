# 💸 Bot Financeiro Inteligente • WhatsApp

Um bot financeiro integrado ao WhatsApp que permite registrar e consultar gastos usando linguagem natural.

> Transformando mensagens simples em controle financeiro real.

---

## ✨ Visão Geral

Este projeto evoluiu de um bot local em Python para uma aplicação real integrada ao WhatsApp, com suporte a múltiplos usuários e armazenamento em banco de dados.

O objetivo é oferecer uma forma rápida e intuitiva de controlar finanças diretamente pelo WhatsApp — sem precisar abrir aplicativos ou planilhas.

---

## 🚀 Funcionalidades

### 📲 Integração com WhatsApp
- Recebe e responde mensagens automaticamente  
- Identificação do usuário pelo número  
- Sistema pronto para uso real  

### 🧾 Registro Inteligente de Gastos
- Interpretação de linguagem natural  
- Suporte a diferentes formas de escrita  
- Extração automática de:
  - Valor  
  - Data (hoje, ontem)  
  - Categoria  
  - Descrição  

### 👤 Sistema de Usuários
- Cadastro automático  
- Login baseado no número  
- Isolamento de dados por usuário  

### 📊 Consulta de Dados
- Listagem de gastos  
- Filtros por data e categoria  
- Respostas diretas no WhatsApp  

---

## 💬 Exemplos de Uso

### ➕ Registrar gastos

hoje gastei 20 com netflix
ontem paguei 35 no mercado
comprei um lanche por 18
gastei 10 na farmácia


### 📊 Consultar gastos

ver gastos
ver gastos hoje
ver gastos ontem
ver gastos alimentação


---

## 🏗️ Arquitetura


Usuário (WhatsApp)
↓
WhatsApp API
↓
Backend (Python + Flask)
↓
Banco de Dados


---

## 🛠️ Tecnologias Utilizadas

- Python  
- Flask  
- WhatsApp API  
- Banco de dados  
- Render (deploy)  
- Regex  
- Unicodedata  

---

## 📁 Estrutura do Projeto


bot-financeiro
┣ bot.py
┣ app.py/
┣ serviceAccontKey.json/
┣ requirements.txt
┣ procfile
┗ README.md


---

## 🔄 Evolução do Projeto

1. Versão terminal (JSON)  
2. Versão web  
3. Versão atual: WhatsApp + banco de dados  

---

## 🎯 Objetivo

Construir uma solução prática de controle financeiro usando linguagem natural, integrada ao WhatsApp, focada no uso real do dia a dia.

---

## 🔮 Próximos Passos

- Relatórios automáticos  
- Controle de receitas  
- Edição e exclusão de gastos  
- Dashboard web  
- Melhorias com IA  
- Alertas financeiros  

---

## 🤝 Contribuição

Sinta-se à vontade para abrir issues ou sugerir melhorias.

---

## 🧑‍💻 Autor

**Magdyel Oliveira**

---

## ⭐ Apoie o Projeto

Se achou interessante:

⭐ Deixe uma estrela  
🚀 Acompanhe a evolução  
