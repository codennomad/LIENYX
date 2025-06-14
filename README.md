# 🤖 LIENYX - Seu Assistente de Notas Inteligente para Telegram

![LIENYX Logo](https://img.shields.io/badge/LIENYX-Bot-blueviolet?style=for-the-badge&logo=telegram)
![Python Version](https://img.shields.io/badge/Python-3.13%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 🌟 Sobre o LIENYX

![Persona do Projeto LIENYX](assets/lienyx.png)

LIENYX é um assistente de inteligência artificial projetado para automatizar a criação de notas detalhadas a partir de conteúdo multimídia. Integrado com o Telegram, ele permite que você envie links de vídeos do YouTube, arquivos de vídeo ou imagens, e ele se encarrega de processar o conteúdo e gerar notas estruturadas no formato Markdown, perfeitas para serem usadas no Obsidian ou em qualquer outro editor de Markdown.

### ✨ Funcionalidades Principais:

* **Download de Vídeos do YouTube:** Baixa vídeos de links do YouTube utilizando `yt-dlp` para alta confiabilidade.
* **Extração de Áudio Inteligente:** Extrai o áudio de arquivos de vídeo MP4 usando **FFmpeg**.
* **Transcrição Avançada:** Transcreve o áudio para texto em português (Brasil) usando o modelo `medium` do `faster-whisper` (execução local e otimizada).
* **Análise Detalhada de Imagens:** Analisa o conteúdo de imagens e transcreve textos nelas contidos, utilizando modelos de IA via **OpenRouter**.
* **Geração de Notas Estruturadas:** Cria notas completas em Markdown, contendo:
    * Tags relevantes.
    * Resumo curto.
    * Resumo detalhado.
    * Listas de bullet points com as ideias principais.
* **Entrega Direta no Telegram:** Envia o arquivo Markdown da nota gerada diretamente para você no Telegram.
* **Logging Robusto:** Utiliza `loguru` para logs detalhados e organizados, com rotação diária e compressão, facilitando o monitoramento e depuração.
* **Modular e Assíncrono:** Arquitetura modular e operações assíncronas para alta performance e responsividade.

## 🚀 Como Começar

Siga estas etapas para configurar e executar seu próprio bot LIENYX.

### 📋 Pré-requisitos

Antes de começar, certifique-se de ter o seguinte instalado:

* **Python 3.13.x (Recomendado):** O projeto foi desenvolvido e testado com Python 3.13.5.
    * **Importante:** Desinstale qualquer outra versão do Python para evitar conflitos de ambiente. Se tiver várias, siga os passos de desinstalação completa antes de instalar a versão 3.13.x limpa.
* **FFmpeg:** Uma ferramenta essencial de linha de comando para manipulação de áudio/vídeo.
    * Baixe o FFmpeg em [ffmpeg.org/download.html](https://ffmpeg.org/download.html).
    * Extraia o conteúdo e adicione o caminho para a pasta `bin` do FFmpeg (`ex: C:\ffmpeg\bin`) à sua variável de ambiente `PATH` do sistema.
    * Verifique a instalação abrindo um novo terminal e digitando `ffmpeg -version`.
* **Conta no Telegram:** Para criar e configurar seu bot.

### 🔑 Configurações Essenciais

1.  **Obtenha seu Token do Bot Telegram:**
    * Converse com o @BotFather no Telegram.
    * Use o comando `/newbot` para criar um novo bot e siga as instruções.
    * O BotFather fornecerá um `token` para seu bot (ex: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123`). Guarde-o.
2.  **Obtenha sua Chave de API do OpenRouter:**
    * Crie uma conta em [openrouter.ai](https://openrouter.ai/).
    * Gere uma chave de API para acessar os modelos de linguagem. Guarde-a.

### 📦 Instalação do Projeto

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/codennomad/LIENYX.git
    ```
2.  **Crie e Ative o Ambiente Virtual:**
    É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.
    ```bash
    python -m venv venv
    .\venv\Scripts\activate 
    ```
3.  **Instale as Dependências Python:**
    Com o ambiente virtual ativado, instale as bibliotecas necessárias.
    ```bash
    pip install -r requirements.txt
    ```
    (Certifique-se de que seu `requirements.txt` está atualizado com as últimas dependências discutidas, incluindo `yt-dlp` e `loguru`).

4.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo `.env` na raiz do seu projeto (na mesma pasta onde está `main.py`) com o seguinte conteúdo:
    ```
    TELEGRAM_BOT_TOKEN=SEU_TOKEN_DO_BOT_TELEGRAM
    OPENROUTER_API_KEY=SUA_CHAVE_API_OPENROUTER
    ```
    Substitua os valores pelos tokens e chaves que você obteve.

## ⚙️ Estrutura do Projeto

```bash 

📁 ├── .env
├── requirements.txt
├── lienyx/
│   ├── init.py
│   ├── app/
│   │   ├── init.py
│   │   └── main.py
│   ├── audio.py           # Extração de áudio (FFmpeg) e transcrição (faster-whisper)
│   ├── download_youtube.py  # Download de vídeos do YouTube (yt-dlp)
│   ├── image.py           # Análise de imagens (OpenRouter/GPT-4o-mini)
│   ├── logger.py          # Configuração de logs com Loguru
│   ├── notas.py           # Geração de notas formatadas em Markdown
│   └── tools.py           # Ferramentas para o Agente LangChain
├── _downloads_telegram/   # Gerada: Vídeos baixados do Telegram/YouTube
├── _audios/               # Gerada: Áudios extraídos
├── _transcriptions/       # Gerada: Transcrições em texto
├── _notes/                # Gerada: Notas finais em Markdown
└── _logs/                 # Gerada: Arquivos de log do bot
```

## 🚀 Como Executar o Bot

Com tudo configurado, você pode iniciar o bot:

1.  **Navegue até a Raiz do Projeto:**
    ```bash
    cd "E:\Obsidian - notas" 
    ```
2.  **Ative o Ambiente Virtual:**
    ```bash
    .\venv\Scripts\activate 
    ```
3.  **Inicie o Bot:**
    ```bash
    python -m lienyx.app.main
    ```
    O bot deve iniciar e você verá mensagens de log no seu terminal.

## 💬 Como Usar o Bot no Telegram

1.  **Inicie uma Conversa:** No Telegram, encontre seu bot e envie o comando `/start`.
2.  **Envie Conteúdo:**
    * **Links do YouTube:** Envie um link de um vídeo do YouTube (ex: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`).
    * **Arquivos de Vídeo:** Anexe e envie um arquivo de vídeo (MP4 recomendado) diretamente para o bot.
    * **Imagens:** Anexe e envie uma imagem para o bot.
3.  **Aguarde:** O bot processará sua solicitação (o que pode levar alguns minutos para vídeos longos ou áudios complexos, especialmente na primeira vez que o modelo Whisper for baixado).
4.  **Receba a Nota:** O bot responderá com o resultado da análise ou, para vídeos/áudios, enviará o arquivo Markdown da nota diretamente no chat.

## 📝 Integrando com Obsidian

As notas são salvas na pasta `_notes` na raiz do seu projeto. Para usá-las no Obsidian:

1.  **Abra a Pasta do Projeto como um Cofre:**
    * No Obsidian, clique em "Open another vault" (canto inferior esquerdo).
    * Selecione "Open folder as vault".
    * Navegue e selecione a pasta **raiz do seu projeto LIENYX** (`E:\Obsidian - notas`).
    * O Obsidian carregará todo o conteúdo do seu projeto, incluindo a pasta `_notes`, e as novas notas aparecerão automaticamente.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, enviar pull requests ou sugerir melhorias.

## 🙋‍♂️ Author

Gabriel Henrique 

🔗 [LinkedIn](https://www.linkedin.com/in/gabrielhenrique-tech/)

📧 gabrielheh03@gmail.com

🧠 AI | NeuroTech | Python Developer

## 📄 Licença

Este projeto está licenciado sob a Licença MIT.

---
