# 🏳️‍🌈 PrismaDeGênero / GenderPrism

[![Read in English](https://img.shields.io/badge/README-English-blue)](README_EN.md)

Bem-vindo ao repositório do **PrismaDeGênero** (internacionalmente conhecido como **GenderPrism**). Esta é uma plataforma educacional open-source dedicada ao letramento de gênero, diversidade e inclusão.

Nosso objetivo é desconstruir preconceitos e construir uma sociedade mais igualitária através da educação acessível.

## 🚀 Sobre o Projeto

O **PrismaDeGênero** é uma aplicação web full-stack que oferece cursos, materiais educativos e uma comunidade segura para aprendizado sobre identidade de gênero, sexualidade e direitos humanos.

### ✨ Funcionalidades Principais

*   **Multilíngue**: Suporte completo para Português Brasileiro (pt-BR) e Inglês (en-US).
*   **Identidade Visual "Prisma"**: Design moderno baseado em espectro de cores e glassmorphism.
*   **Gestão de Cursos**: Listagem de cursos com preços e descrições.
*   **Sistema de Matrícula**: Usuários podem se matricular e acompanhar o progresso (Dashboard).
*   **Autenticação Segura**: Login (Usuário/Email) e Registro com permissões diferenciadas (Admin vs Aluno).
*   **Painel do Aluno**: Acompanhamento visual de progresso e histórico de cursos.

## 🛠️ Tecnologias Utilizadas

### Backend (API)
*   **Python 3**
*   **Django REST Framework**: Para construção da API robusta.
*   **SQLite**: Banco de dados padrão (pode ser migrado para PostgreSQL).

### Frontend (Interface)
*   **Vue.js 3**: Framework JavaScript reativo (Composition API).
*   **Vite**: Build tool ultra-rápido.
*   **Tailwind CSS**: Framework de estilização utilitário.
*   **Vue Router & Pinia**: Roteamento e gerenciamento de estado.
*   **Vue I18n**: Internacionalização.

---

## ⚙️ Como Executar o Projeto

Siga os passos abaixo para rodar o projeto localmente em sua máquina.

### Pré-requisitos
*   Node.js (v16+) e npm
*   Python (v3.8+) e pip

### 1. Configurando o Backend (Django)

```bash
# Entre na pasta do backend
cd backend

# Crie um ambiente virtual (opcional, mas recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações do banco de dados
python3 manage.py migrate

# Crie um superusuário (para acessar o admin e criar cursos)
python3 manage.py createsuperuser

# Inicie o servidor
python3 manage.py runserver
```

O backend estará rodando em: `http://localhost:8000`

### 2. Configurando o Frontend (Vue.js)

```bash
# Abra um novo terminal e entre na pasta do frontend
cd frontend

# Instale as dependências do Node
npm install

# Inicie o servidor de desenvolvimento
npm run dev
```

O frontend estará rodando em: `http://localhost:5173` (ou porta similar indicada no terminal).

---

## 🤝 Como Contribuir

Este é um projeto público e colaborativo! Queremos muito a sua ajuda para torná-lo ainda melhor. Seja corrigindo bugs, adicionando novas funcionalidades, melhorando a documentação ou traduzindo conteúdo.

### Guia de Contribuição

1.  **Faça um Fork** deste repositório.
2.  **Clone o seu Fork** para sua máquina local.
    ```bash
    git clone https://github.com/SEU_USUARIO/GenderSchool.git
    ```
3.  **Crie uma Branch** para sua funcionalidade ou correção.
    ```bash
    git checkout -b feature/minha-nova-funcionalidade
    ```
4.  **Faça as alterações** necessárias e commite.
    ```bash
    git commit -m "feat: Adiciona nova funcionalidade X"
    ```
5.  **Envie para o seu repositório** (Push).
    ```bash
    git push origin feature/minha-nova-funcionalidade
    ```
6.  **Abra um Pull Request (PR)** no repositório original.
    *   Descreva detalhadamente o que foi feito.
    *   Se possível, anexe screenshots ou vídeos.

### O que você pode fazer?
*   🐛 **Reportar Bugs**: Abra uma Issue descrevendo o problema.
*   💡 **Sugerir Melhorias**: Tem uma ideia legal? Abra uma Issue para discutirmos.
*   📝 **Melhorar a Documentação**: Ajude a tornar este README ou o código mais claro.
*   🌍 **Tradução**: Ajude a adicionar novos idiomas.

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, modificar e distribuir.

---

<p align="center">
  Feito com 🏳️‍🌈 e ❤️ pela comunidade <strong>PrismaDeGênero</strong>.
</p>
