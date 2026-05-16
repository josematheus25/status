from flask import Flask, render_template, request, jsonify, redirect
import sqlite3, os
from datetime import datetime

app = Flask(__name__)
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'volei.db')

POSICOES = {
    'Oposto': {
        'stats': ['ataque', 'erro_ataque', 'bola_passada', 'saque', 'erro_saque', 'ace', 'bloqueio'],
        'labels': {
            'ataque':       '⚡ Ponto de Ataque',
            'erro_ataque':  '✗ Erro de Ataque',
            'bola_passada': '→ Bola Passada',
            'saque':        '🎾 Saque',
            'erro_saque':   '✗ Erro de Saque',
            'ace':          '🔥 Ace',
            'bloqueio':     '🛡 Bloqueio',
        },
        'cores': {
            'ataque':       'btn-green',
            'erro_ataque':  'btn-red',
            'bola_passada': 'btn-yellow',
            'saque':        'btn-orange',
            'erro_saque':   'btn-red',
            'ace':          'btn-orange',
            'bloqueio':     'btn-blue',
        }
    },
    'Levantador': {
        'stats': ['assistencia', 'erro_levantamento', 'saque', 'erro_saque', 'ace', 'bloqueio'],
        'labels': {
            'assistencia':       '🎯 Assistência',
            'erro_levantamento': '✗ Erro Levantamento',
            'saque':             '🎾 Saque',
            'erro_saque':        '✗ Erro de Saque',
            'ace':               '🔥 Ace',
            'bloqueio':          '🛡 Bloqueio',
        },
        'cores': {
            'assistencia':       'btn-green',
            'erro_levantamento': 'btn-red',
            'saque':             'btn-orange',
            'erro_saque':        'btn-red',
            'ace':               'btn-orange',
            'bloqueio':          'btn-blue',
        }
    },
    'Líbero': {
        'stats': ['recepcao_mao', 'recepcao', 'erro_recepcao', 'passe', 'defesa'],
        'labels': {
            'recepcao_mao':  '🤚 Recepção na Mão',
            'recepcao':      '↓ Recepção',
            'erro_recepcao': '✗ Erro de Recepção',
            'passe':         '→ Passe',
            'defesa':        '🛡 Defesa',
        },
        'cores': {
            'recepcao_mao':  'btn-green',
            'recepcao':      'btn-blue',
            'erro_recepcao': 'btn-red',
            'passe':         'btn-yellow',
            'defesa':        'btn-blue',
        }
    },
    'Central': {
        'stats': ['bloqueio', 'ataque', 'erro_ataque', 'saque', 'erro_saque'],
        'labels': {
            'bloqueio':    '🛡 Bloqueio',
            'ataque':      '⚡ Ponto de Ataque',
            'erro_ataque': '✗ Erro de Ataque',
            'saque':       '🎾 Saque',
            'erro_saque':  '✗ Erro de Saque',
        },
        'cores': {
            'bloqueio':    'btn-blue',
            'ataque':      'btn-green',
            'erro_ataque': 'btn-red',
            'saque':       'btn-orange',
            'erro_saque':  'btn-red',
        }
    },
    'Ponteiro': {
        'stats': ['recepcao', 'erro_recepcao', 'ataque', 'erro_ataque', 'saque', 'erro_saque', 'ace', 'bloqueio'],
        'labels': {
            'recepcao':      '↓ Recepção',
            'erro_recepcao': '✗ Erro de Recepção',
            'ataque':        '⚡ Ponto de Ataque',
            'erro_ataque':   '✗ Erro de Ataque',
            'saque':         '🎾 Saque',
            'erro_saque':    '✗ Erro de Saque',
            'ace':           '🔥 Ace',
            'bloqueio':      '🛡 Bloqueio',
        },
        'cores': {
            'recepcao':      'btn-blue',
            'erro_recepcao': 'btn-red',
            'ataque':        'btn-green',
            'erro_ataque':   'btn-red',
            'saque':         'btn-orange',
            'erro_saque':    'btn-red',
            'ace':           'btn-orange',
            'bloqueio':      'btn-blue',
        }
    }
}

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            camisa INTEGER,
            time TEXT,
            posicao TEXT,
            criado_em TEXT
        );
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            time_a TEXT,
            time_b TEXT,
            placar_a INTEGER DEFAULT 0,
            placar_b INTEGER DEFAULT 0,
            status TEXT DEFAULT 'em_andamento',
            criado_em TEXT
        );
        CREATE TABLE IF NOT EXISTS acoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partida_id INTEGER,
            jogador_id INTEGER,
            tipo TEXT,
            timestamp TEXT,
            FOREIGN KEY(partida_id) REFERENCES partidas(id),
            FOREIGN KEY(jogador_id) REFERENCES jogadores(id)
        );
        CREATE TABLE IF NOT EXISTS partida_jogadores (
            partida_id INTEGER,
            jogador_id INTEGER,
            PRIMARY KEY(partida_id, jogador_id)
        );
    ''')
    conn.commit()
    conn.close()

# ──────────────────────────────────────────
# ROUTES
# ──────────────────────────────────────────

@app.route('/')
def index():
    conn = get_db()
    total_jogadores  = conn.execute('SELECT COUNT(*) FROM jogadores').fetchone()[0]
    total_partidas   = conn.execute('SELECT COUNT(*) FROM partidas').fetchone()[0]
    partidas_ativas  = conn.execute("SELECT COUNT(*) FROM partidas WHERE status='em_andamento'").fetchone()[0]
    partidas_recentes = conn.execute("SELECT * FROM partidas ORDER BY id DESC LIMIT 5").fetchall()
    conn.close()
    return render_template('index.html',
        total_jogadores=total_jogadores,
        total_partidas=total_partidas,
        partidas_ativas=partidas_ativas,
        partidas_recentes=partidas_recentes)

# ── JOGADORES ──
@app.route('/jogadores')
def jogadores():
    conn = get_db()
    rows = conn.execute('SELECT * FROM jogadores ORDER BY nome').fetchall()
    conn.close()
    return render_template('jogadores.html', jogadores=rows, posicoes=list(POSICOES.keys()))

@app.route('/jogadores/novo', methods=['POST'])
def novo_jogador():
    d = request.form
    conn = get_db()
    conn.execute(
        'INSERT INTO jogadores (nome, camisa, time, posicao, criado_em) VALUES (?,?,?,?,?)',
        (d['nome'], d['camisa'], d['time'], d['posicao'], datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return redirect('/jogadores')

@app.route('/jogadores/deletar/<int:jid>', methods=['POST'])
def deletar_jogador(jid):
    conn = get_db()
    # FIX: limpar referências antes de deletar o jogador
    conn.execute('DELETE FROM partida_jogadores WHERE jogador_id=?', (jid,))
    conn.execute('DELETE FROM acoes WHERE jogador_id=?', (jid,))
    conn.execute('DELETE FROM jogadores WHERE id=?', (jid,))
    conn.commit()
    conn.close()
    return redirect('/jogadores')

# ── PARTIDAS ──
@app.route('/partidas')
def partidas():
    conn = get_db()
    rows = conn.execute('SELECT * FROM partidas ORDER BY id DESC').fetchall()
    jogadores = conn.execute('SELECT * FROM jogadores ORDER BY nome').fetchall()
    conn.close()
    return render_template('partidas.html', partidas=rows, jogadores=jogadores)

@app.route('/partidas/deletar/<int:pid>', methods=['POST'])
def deletar_partida(pid):
    conn = get_db()
    conn.execute('DELETE FROM acoes WHERE partida_id=?', (pid,))
    conn.execute('DELETE FROM partida_jogadores WHERE partida_id=?', (pid,))
    conn.execute('DELETE FROM partidas WHERE id=?', (pid,))
    conn.commit()
    conn.close()
    return redirect('/partidas')

@app.route('/partidas/nova', methods=['POST'])
def nova_partida():
    d = request.form
    jogadores_ids = request.form.getlist('jogadores')
    conn = get_db()
    cur = conn.execute(
        'INSERT INTO partidas (titulo, time_a, time_b, criado_em) VALUES (?,?,?,?)',
        (d['titulo'], d['time_a'], d['time_b'], datetime.now().isoformat()))
    pid = cur.lastrowid
    for jid in jogadores_ids:
        conn.execute('INSERT INTO partida_jogadores VALUES (?,?)', (pid, jid))
    conn.commit()
    conn.close()
    return redirect(f'/partida/{pid}')

# ── PARTIDA AO VIVO ──
@app.route('/partida/<int:pid>')
def partida_ao_vivo(pid):
    conn = get_db()
    partida = conn.execute('SELECT * FROM partidas WHERE id=?', (pid,)).fetchone()
    if not partida:
        conn.close()
        return redirect('/partidas')
    jids = conn.execute(
        'SELECT jogador_id FROM partida_jogadores WHERE partida_id=?', (pid,)).fetchall()
    jogadores = []
    for row in jids:
        j = conn.execute('SELECT * FROM jogadores WHERE id=?', (row['jogador_id'],)).fetchone()
        if j:
            jogadores.append(j)
    acoes = conn.execute(
        '''SELECT a.tipo, j.nome FROM acoes a
           JOIN jogadores j ON a.jogador_id=j.id
           WHERE a.partida_id=? ORDER BY a.id DESC LIMIT 20''', (pid,)).fetchall()
    conn.close()
    return render_template('partida.html',
        partida=partida, jogadores=jogadores,
        posicoes=POSICOES, acoes=acoes)

@app.route('/api/acao', methods=['POST'])
def registrar_acao():
    d = request.json
    if not d or 'partida_id' not in d or 'jogador_id' not in d or 'tipo' not in d:
        return jsonify({'ok': False, 'erro': 'Dados inválidos'}), 400
    conn = get_db()
    conn.execute(
        'INSERT INTO acoes (partida_id, jogador_id, tipo, timestamp) VALUES (?,?,?,?)',
        (d['partida_id'], d['jogador_id'], d['tipo'], datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/api/placar', methods=['POST'])
def atualizar_placar():
    d = request.json
    if not d:
        return jsonify({'ok': False}), 400
    # FIX: garantir que placar não fique negativo
    pa = max(0, int(d.get('placar_a', 0)))
    pb = max(0, int(d.get('placar_b', 0)))
    conn = get_db()
    conn.execute(
        'UPDATE partidas SET placar_a=?, placar_b=? WHERE id=?',
        (pa, pb, d['partida_id']))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/api/encerrar_partida/<int:pid>', methods=['POST'])
def encerrar_partida(pid):
    conn = get_db()
    conn.execute("UPDATE partidas SET status='encerrada' WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

# ── RELATÓRIO ──
@app.route('/relatorio/<int:pid>')
def relatorio(pid):
    conn = get_db()
    partida = conn.execute('SELECT * FROM partidas WHERE id=?', (pid,)).fetchone()
    if not partida:
        conn.close()
        return redirect('/partidas')
    jids = conn.execute(
        'SELECT jogador_id FROM partida_jogadores WHERE partida_id=?', (pid,)).fetchall()
    dados = []
    for row in jids:
        j = conn.execute('SELECT * FROM jogadores WHERE id=?', (row['jogador_id'],)).fetchone()
        if not j:
            continue
        acoes = conn.execute(
            'SELECT tipo, COUNT(*) as qtd FROM acoes WHERE partida_id=? AND jogador_id=? GROUP BY tipo',
            (pid, j['id'])).fetchall()
        stats = {a['tipo']: a['qtd'] for a in acoes}
        pos = j['posicao']
        config = POSICOES.get(pos, {})

        # calcular eficiência
        pontos = (stats.get('ataque', 0) + stats.get('ace', 0) +
                  stats.get('bloqueio', 0) + stats.get('assistencia', 0))
        erros  = (stats.get('erro_ataque', 0) + stats.get('erro_saque', 0) +
                  stats.get('erro_recepcao', 0) + stats.get('erro_levantamento', 0))
        total  = sum(stats.values()) or 1
        # FIX: clamp eficiência entre -100 e 100
        eficiencia = round((pontos - erros) / total * 100, 1)
        eficiencia = max(-100.0, min(100.0, eficiencia))

        dados.append({
            'jogador':    dict(j),
            'stats':      stats,
            'config':     config,
            'pontos':     pontos,
            'erros':      erros,
            'total':      total,
            'eficiencia': eficiencia
        })

    # ranking MVP por eficiência (desempate: mais pontos)
    dados.sort(key=lambda x: (x['eficiencia'], x['pontos']), reverse=True)
    conn.close()
    return render_template('relatorio.html', partida=partida, dados=dados)

if __name__ == '__main__':
    init_db()
    print("\n🏐 Sistema de Estatísticas de Vôlei")
    print("   Acesse: http://localhost:5000\n")
    app.run(debug=True, port=5000)
