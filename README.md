# 📦 Estrala Aviamentos – Automação de Ordens de Serviço

## 📌 Contexto do Problema
Atualmente, a **Estrala Aviamentos** possui apenas **uma licença do módulo de Manutenção de Ativos da TOTVS (Protheus)**.  
Isso faz com que **somente uma pessoa** seja responsável por cadastrar todas as **Ordens de Serviço (OS)** no sistema, ocasionando:

- Gargalo operacional
- Risco de atraso no registro das OS
- Dependência excessiva de um único usuário

---

## 🎯 Objetivo
Desenvolver um **protótipo em Python** para validar uma solução que permita:

- Cadastro descentralizado de Ordens de Serviço
- Registro de serviços vinculados à OS
- Armazenamento das informações em banco de dados próprio
- Redução da dependência direta da licença da TOTVS

---

## 🧩 Escopo do Protótipo
Este projeto consiste em um **protótipo funcional**, com foco em validação técnica e de processo, não sendo ainda um sistema final.

Funcionalidades implementadas:

- Aplicação em Python
- Banco de dados local (SQLite)
- Cadastro de Ordens de Serviço
- Cadastro de serviços vinculados às OS
- Preparação dos dados para automação

---

## 🗄️ Estrutura do Banco de Dados
O banco de dados do protótipo é composto por três tabelas:

- **ordem_servico**  
  Armazena as informações principais da Ordem de Serviço.

- **servico_os**  
  Armazena os serviços vinculados a cada OS, relacionados pelo campo `id_os`.

- **reg_automacao**  
  Tabela intermediária utilizada pela automação para registrar as OS processadas.

---

## ⚙️ Automação
Foi desenvolvido um script em Python responsável por:

1. Ler os registros da tabela `ordem_servico`
2. Buscar os serviços vinculados na tabela `servico_os`
3. Consolidar as informações em um conteúdo textual
4. Registrar os dados na tabela `reg_automacao`
5. Excluir os registros processados das tabelas `ordem_servico` e `servico_os`

Esses dados são utilizados para geração de um **bloco de texto**, que futuramente será consumido por uma automação no sistema TOTVS.

---

## 🔄 Próximas Etapas
Após a validação do protótipo, estão previstas as seguintes evoluções:

- Migração do banco de dados para **MySQL**
- Melhoria do modelo relacional
- Implementação de automação com **PyAutoGUI**
- Preenchimento automático de Ordens de Serviço no **TOTVS Protheus**

---

## 🛠️ Tecnologias Utilizadas
- Python
- SQLite (protótipo)
- PyAutoGUI (planejado)
- Git & GitHub

---

## 🚀 Benefícios Esperados
- Redução de gargalos operacionais
- Agilidade no registro de Ordens de Serviço
- Melhor rastreabilidade das informações
- Base sólida para automações futuras

---

## 📌 Status do Projeto
🟢 Protótipo concluído  
🟡 Em fase de validação para evolução

---

## 👤 Autor
**Renan Garcia Araujo Gadelha**  
Engenheiro de Dados
