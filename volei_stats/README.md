# 🏐 VôleiStats Pro

Sistema profissional de estatísticas para vôlei com scout em tempo real.

---

## ✅ Como instalar e rodar

### Requisitos
- Python 3.8 ou superior
- Flask (instalado automaticamente)

### Passo a passo

```bash
# 1. Instale o Flask (somente na primeira vez)
pip install flask

# 2. Entre na pasta do projeto
cd volei_stats

# 3. Inicie o sistema
python iniciar.py

# 4. Abra o navegador em:
#    http://localhost:5000
```

---

## 🎮 Como usar

### 1. Cadastrar Jogadores
- Vá em **Jogadores**
- Preencha: Nome, Camisa, Time, Posição
- Clique em **Cadastrar Jogador**

### 2. Criar Partida
- Vá em **Partidas**
- Preencha: Título, Times A e B
- Selecione os jogadores que vão jogar
- Clique em **Iniciar Partida**

### 3. Scout em Tempo Real
- A tela da partida mostra cada jogador com seus botões específicos
- Clique nos botões para registrar ações
- O log ao vivo mostra tudo em tempo real
- Ajuste o placar com os botões + e −

### 4. Encerrar e Ver Relatório
- Clique em **Encerrar** para finalizar a partida
- O relatório automático mostra:
  - Placar final
  - MVP + ranking
  - Eficiência de cada jogador
  - Estatísticas detalhadas por posição

---

## 📊 Posições e Estatísticas

| Posição     | Estatísticas                                      |
|-------------|---------------------------------------------------|
| Oposto      | Ataque, Erro de Ataque, Bola Recebida, Bola Passada |
| Levantador  | Assistência, Erro de Levantamento, Ace, Bloqueio  |
| Líbero      | Recepção Perfeita, Defesa, Erro de Recepção, Passe |
| Central     | Bloqueio, Ponto Rápido, Erro, Saque               |
| Ponteiro    | Recepção, Ataque, Defesa, Erro                    |

---

## 🧮 Fórmula de Eficiência

```
Eficiência = (Pontos - Erros) / Total de Ações × 100
```

---

## 📁 Arquivos do projeto

```
volei_stats/
├── app.py          → Backend principal (Flask + SQLite)
├── iniciar.py      → Script de inicialização
├── volei.db        → Banco de dados (criado automaticamente)
├── templates/
│   ├── base.html   → Layout base
│   ├── index.html  → Tela inicial
│   ├── jogadores.html → Cadastro de jogadores
│   ├── partidas.html  → Lista e criação de partidas
│   ├── partida.html   → Scout ao vivo
│   └── relatorio.html → Relatório pós-jogo
└── README.md
```
