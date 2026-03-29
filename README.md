# 🚀 Rica-Monitor

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![UI](https://img.shields.io/badge/UI-Rich--TUI-cyan.svg)
![OS](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg)

**Rica-Monitor** é um monitor de recursos do sistema moderno, leve e elegante para o terminal. Desenvolvido em Python e inspirado na estética do `btop`, ele oferece uma experiência fluida com zero latência na interface, permitindo acompanhar a saúde do seu hardware em tempo real.

---

## ✨ Funcionalidades

* 📊 **Resumo Geral**: Visão consolidada de CPU e RAM com barras de progresso dinâmicas.
* ⚡ **Monitor de CPU**: Detalhamento individual por núcleo, frequência atual (MHz) e cores semânticas (Verde/Amarelo/Vermelho).
* 🧠 **Gerenciamento de Memória**: Visualização clara de uso percentual, capacidade total e memória disponível.
* 💾 **Armazenamento**: Monitoramento de partições com cálculos de espaço livre/usado e alertas visuais.
* 🌐 **Tráfego de Rede**: Estatísticas em tempo real de Download e Upload (MB).
* 🕒 **Interface Profissional**: Layout dividido com Header (Relógio), Menu Lateral, Conteúdo Dinâmico e Footer com atalhos.

---

## 🛠️ Arquitetura Técnica

Diferente de monitores simples que travam a interface ao ler o disco ou rede, o **Rica-Monitor** utiliza uma arquitetura de **Separação de Preocupações (SoC)** com Multi-threading:

1.  **Thread de Coleta (Background)**: Atualiza um cache de dados do sistema via `psutil` a cada 1 segundo.
2.  **Thread de Input**: Captura as teclas do usuário de forma assíncrona com `readchar`, garantindo que o menu responda instantaneamente.
3.  **Thread de Renderização (Rich Live)**: Atualiza a interface visual a 10 FPS, permitindo um relógio fluido e transições suaves sem impacto na performance.

---

## 📦 Instalação

### Pré-requisitos
* Python 3.10 ou superior.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/ricaprof/rica-tools.git
    cd rica-tools
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # .venv\Scripts\activate   # Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Como Executar

Para iniciar o monitor, execute o arquivo principal:
```bash
python main.py
```

## Estrutura do Arquivo
```
/rica-tools
│
├── main.py              # Ponto de entrada (Executável)
├── monitor_app.py       # Classe MonitorApp (Lógica e Threads)
├── views.py             # Funções de renderização (UI)
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação completa
```

