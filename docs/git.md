# Guia Prático de Git e GitHub para Iniciantes

Este guia foi criado para ajudar você a entender e utilizar o **Git** (controle de versão local) e o **GitHub** (plataforma de hospedagem remota) de forma simples, objetiva e prática.

---

## 1. Conceitos Básicos

- **Git:** Sistema de controle de versão que roda no seu computador. Ele salva o histórico de alterações do seu código ("fotos" do projeto ao longo do tempo).
- **GitHub:** Serviço na nuvem que armazena seus repositórios Git, permitindo compartilhamento, backup e colaboração.
- **Repositório Local:** A pasta do projeto no seu computador gerenciada pelo Git.
- **Repositório Remoto:** O projeto hospedado no GitHub.

---

## 2. Configuração Inicial do Git (Feita apenas uma vez)

Se você ainda não configurou seu nome e e-mail no Git do seu computador, abra o terminal e execute:

```bash
git config --global user.name "phmcasimiro"
git config --global user.email "phmcasimiro@gmail.com"
```

---

## 3. Conectando este Repositório Local ao GitHub

Considerando o repositório remoto que você criou:  
`https://github.com/phmcasimiro/geo-data_portfolio.git`

Siga os passos abaixo no terminal dentro da pasta raiz do projeto:

### Passo 1: Inicializar o Git no projeto local
*(Execute este comando se a pasta ainda não for um repositório Git)*
```bash
git init
```

### Passo 2: Renomear o branch principal para `main` (Padrão atual)
```bash
git branch -M main
```

### Passo 3: Conectar o repositório local ao repositório do GitHub
```bash
git remote add origin https://github.com/phmcasimiro/geo-data_portfolio.git
```

> **Dica:** Para verificar se a conexão foi feita corretamente, rode:
> `git remote -v`

---

## 4. Fluxo de Trabalho Diário (Os 4 Passos Fundamentais)

Sempre que você criar, editar ou deletar arquivos no seu projeto, siga este fluxo:

### 1. Verificar o status dos arquivos
Veja quais arquivos foram modificados ou ainda não estão sendo rastreados pelo Git:
```bash
git status
```

### 2. Adicionar os arquivos para a "Staging Area" (Preparar para o commit)
- Para adicionar todos os arquivos modificados de uma vez:
  ```bash
  git add .
  ```
- Ou para adicionar um arquivo específico:
  ```bash
  git add nome_do_arquivo.extensao
  ```

### 3. Fazer o Commit (Salvar a versão localmente)
Grave as alterações no histórico local acompanhadas de uma mensagem clara que descreva o que foi feito:
```bash
git commit -m "feat: adiciona guia pratico de git e github"
```

### 4. Enviar para o GitHub (Push)
- **Primeiro push:** Envia o código e vincula o branch local ao remoto:
  ```bash
  git push -u origin main
  ```
- **Próximos pushes:** Nas próximas vezes, basta usar apenas:
  ```bash
  git push
  ```

---

## 5. Baixando Alterações do GitHub (Pull)

Se você fizer alterações diretamente pelo site do GitHub ou trabalhar de outro computador, atualize seu projeto local rodando:

```bash
git pull origin main
```

---

## 6. O Arquivo `.gitignore` (Muito Importante!)

Nem tudo deve ser enviado para o GitHub (por exemplo: ambientes virtuais como a pasta `venv/`, arquivos de configuração com senhas ou arquivos temporários).

Para evitar o envio desses arquivos, crie um arquivo chamado `.gitignore` na raiz do projeto e insira os arquivos/pastas a serem ignorados. Exemplo:

```text
# Ambiente virtual Python
venv/
.venv/

# Cache do Python
__pycache__/
*.pyc

# Checkpoints do Jupyter Notebook
.ipynb_checkpoints/
```

---

## 7. Resumo Rápido de Comandos

| Comando | Descrição |
| :--- | :--- |
| `git status` | Exibe o estado atual das suas alterações. |
| `git add .` | Prepara todos os arquivos modificados para o commit. |
| `git commit -m "mensagem"` | Salva as alterações na linha do tempo do projeto. |
| `git push` | Envia as alterações salvas para o GitHub. |
| `git pull` | Baixa as novidades do GitHub para a sua máquina. |
| `git log` | Mostra o histórico de commits do projeto. |
