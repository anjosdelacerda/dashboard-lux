# Projeto LUX Energia - Teste Técnico Full-Stack Django

Este repositório contém uma aplicação full-stack desenvolvida em Django e Django REST Framework para um teste técnico. O coração da aplicação é a área administrativa do Django, personalizada para exibir dados de interesse e permitir o gerenciamento de usuários e empresas.

## Requisitos para Rodar o Projeto

Para executar este projeto em sua máquina, você precisará ter o Python instalado em uma versão **igual ou superior a 3.12.6**.

## Como Clonar e Rodar a Aplicação

Siga os passos abaixo para configurar e iniciar o projeto:

1.  **Clone o Repositório:**
    Abra seu terminal ou prompt de comando e execute:
    ```bash
    git clone <git@github.com:anjosdelacerda/dashboard-lux.git>
    ```

2.  **Navegue até o Diretório do Projeto:**
    Após clonar, entre na pasta do projeto:
    ```bash
    cd <nome-da-pasta-do-repositorio>
    ```

3.  **Crie e Ative o Ambiente Virtual (`venv`):**
    É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.
    ```bash
    python -m venv venv
    ```
    **Ative o ambiente virtual:**
    * **No Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```
    * **No Windows (Prompt de Comando):**
        ```cmd
        venv\Scripts\activate.bat
        ```
    * **No Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```

4.  **Instale as Dependências do Projeto:**
    Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Verifique a Estrutura do Projeto:**
    Antes de rodar o servidor, é bom confirmar se você está no diretório correto. Digite `ls` (no Linux/macOS) ou `dir` (no Windows) e verifique se as seguintes pastas aparecem:
    `dashboard/`, `data/`, `empresas/`, `templates/`, `users/`

6.  **Execute as Migrações do Banco de Dados:**
    Mesmo com o banco de dados já populado, é **essencial** rodar as migrações para que o Django sincronize o esquema do banco de dados com os modelos da aplicação.
    ```bash
    python manage.py migrate
    ```

7.  **Inicie o Servidor de Desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

8.  **Acesse a Aplicação:**
    Um link será exibido no seu terminal (geralmente `http://127.0.0.1:8000/`). Segure a tecla `Ctrl` (ou `Cmd` no macOS) e clique no link para abrir a página de registro no seu navegador.

---

## Observações Importantes:

* **Banco de Dados Populado:** Subir um banco de dados junto com o repositório é uma prática de desenvolvimento geralmente evitada em projetos maiores por questões de segurança e versionamento. No entanto, para este teste técnico, o banco de dados `db.sqlite3` já está incluído com os dados da planilha populados, permitindo uma inicialização rápida.
* **Recriação do Banco de Dados:** Caso queira apagar o banco de dados existente (`db.sqlite3`) e recriar tudo do zero, o arquivo `import_excel.py` (localizado na pasta `data/`, presumindo que você tenha um) poderá ser executado **após** as migrações serem criadas e geradas (`python manage.py makemigrations` e `python manage.py migrate`).