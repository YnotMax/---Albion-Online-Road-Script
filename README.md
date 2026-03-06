<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows">
  <img src="https://img.shields.io/badge/Automation-FF4B4B?style=for-the-badge&logo=robot&logoColor=white" alt="Automation">
  <br>
  <h1>⚔️ Albion Online Road Script - Stealth Edition</h1>
  <p><b>Ferramenta de Automação de Alta Precisão e Baixa Detecção</b></p>
</div>

<p align="center">
  <img src="Tela%20inicial.png" alt="Interface do Albion Road Script" width="800">
</p>

<p align="center">
  <video src="https://github.com/YnotMax/---Albion-Online-Road-Script/raw/main/demo.mp4" width="800" controls="controls" muted="muted" loop="loop">
    Seu navegador não suporta o player de video.
  </video>
</p>

---

> [!NOTE]  
> 🕵️‍♂️ **Camuflagem Ativa:** Para evitar detecção por sistemas Anti-Cheat (como BattlEye ou Easy Anti-Cheat), **o aplicativo foi desenhado para se disfarçar como um driver de sistema utilitário**. 
> Quando você rodar o programa ou compilar o `.exe`, ele aparecerá com o nome de **`AudioHD_Monitor`** ou **`Gerenciador de Periféricos HD`**. Não estranhe, isso é intencional para manter sua conta segura!

<p align="center">
  O <b>Albion Online Road Script</b> é uma aplicação desktop desenvolvida em Python, focada em gravar e reproduzir ações de teclado e mouse com precisão submilisegundo. Projetado para otimização de tarefas e automação de rotinas em ambientes complexos.
</p>

---

## 🎮 Para Jogadores (Foco em Albion Online & MMORPGs)

Cansado do *grind* infinito? Esta ferramenta foi desenhada para criar rotinas automatizadas (como craft, refinamento ou rotas de transporte e coleta) de forma inteligente e discreta.

### 🛡️ Por que usar este Script?
- **Identidade Falsa & Stealth Mode Ativo:** A janela do aplicativo se passa por um mero equalizador/gerenciador de hardware. Sem overlays (janelas flutuantes) e sem processos suspeitos no Gerenciador de Tarefas do Windows.
- **Precisão Cirúrgica (`time.perf_counter`):** Ferramentas normais de macro falham em longas distâncias devido ao atraso cronológico do Windows. Nós utilizamos motores de contagem da CPU para garantir que seu personagem pare **exatamente** no pixel onde a gravação terminou, mesmo em rotas longas.
- **Micro-variações Anti-Bot:** Padrões perfeitamente idênticos geram banimentos. O *I/O Controller* injeta variações microscópicas e humanizadas a cada reprodução, tornando a automação virtualmente indistinguível de um jogador real.
- **Feedback Sonoro (Bipes):** Opere sua rotina em segundo plano. Atalhos globais emitem bipes curtos e inofensivos do próprio sistema Windows para você saber quando mapeou um percurso, iniciou ou parou, sem precisar dar *Alt+Tab*.

---

## 💼 Para Recrutadores (Arquitetura e Engenharia)

Este projeto demonstra a aplicação prática de padrões de engenharia de software, UX/UI e conhecimento profundo do Sistema Operacional.

### 🧠 Destaques Técnicos:
*   **Multithreading Concorrente:** O sistema de reprodução e a interface gráfica (GUI) rodam em threads separadas, garantindo que a aplicação nunca congele (*Non-blocking UI*) durante cálculos pesados ou longos estados de espera *(sleeps)*.
*   **Loop de Alta Precisão (Busy Wait):** O comando padrão `time.sleep()` do SO Windows possui um desvio crônico de ~15ms. Para driblar esta limitação de hardware/SO, implementei uma arquitetura de loop `while` assíncrono checando o `perf_counter()` para espera ultraprecisa, essencial para automação temporal determinística.
*   **Filtros de Otimização (Anti-Jitter):** O algoritmo de captura do mouse processa e descarta movimentos sub-pixel estáticos *(Jitters)* em tempo real antes de persistir os dados no HD, reduzindo o I/O disk space e tamanho do JSON final em até 80%.
*   **Design Heurístico:** Interface UX construída do zero sob a óptica das **10 Heurísticas de Jakob Nielsen**, com fortes indicativos visuais, atalhos universais previnindo erros destrutivos do usuário.

### 🛠️ Tecnologias Utilizadas
*   **Linguagem:** Python 3.x
*   **GUI:** `customtkinter` (Dark Mode nativo, componentes complexos)
*   **Core Lógico:** `pynput` (Escuta e Injeção de eventos Kernel-Level)
*   **Persistência:** Sistemas nativos JSON com tratamentos modulares I/O.
*   **Logging:** Sistema coeso para debugar falhas, com rotação de arquivos para produção segura.

---

## 🚀 Guia de Início Rápido

### Pré-requisitos
1. Python 3.x instalado e adicionado ao caminho (PATH) do seu computador.

### Instalação
1. Clone o repositório:
```bash
git clone https://github.com/SEU_USUARIO/albion-online-road-script.git
cd albion-online-road-script
```

2. Crie e ative um ambiente virtual (Opcional, mas recomendado):
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. **Inicie o App:**
Basta dar um duplo-clique no arquivo `iniciar.bat` ou rodar no terminal:
```bash
python main.py
```

### 📖 Como Usar os Atalhos Globais:
- **`[F9]`** Inicia ou Para uma Nova Gravação. (Siga a contagem regressiva sonora).
- **`[F8]`** Inicia ou Para a Reprodução da macro selecionada na biblioteca.
- **`[F10]`** **KEY DE EMERGÊNCIA**. Aperte a qualquer instante para matar instantaneamente qualquer automação ocorrendo.

## 👤 Autor

Desenvolvido por **Tony Max da Silva Costa**.

<div align="left">
  <a href="https://www.linkedin.com/in/tony-max-da-silva-costa/" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
  <a href="https://www.instagram.com/tony_max_silva/" target="_blank">
    <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram">
  </a>
</div>

---
> **Disclaimer/Aviso:** O uso de automações pode ferir os Termos de Serviço de alguns softwares e jogos online. Use com responsabilidade e por sua própria conta e risco. O autor deste código não se responsabiliza por eventuais restrições/banimentos de contas associadas ao mau uso da ferramenta.
