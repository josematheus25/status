#!/usr/bin/env python3
"""
🏐 VôleiStats Pro — Sistema de Estatísticas de Vôlei
=====================================================
Como usar:
  1. Execute:  python iniciar.py
  2. Abra no navegador: http://localhost:5000
  3. Cadastre jogadores → Crie uma partida → Scout em tempo real!
"""
import os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, init_db
except ImportError:
    print("Instalando dependências...")
    os.system(f"{sys.executable} -m pip install flask")
    from app import app, init_db

init_db()
print("\n" + "="*50)
print("  🏐  VôleiStats Pro")
print("="*50)
print("  Acesse: http://localhost:5000")
print("  Para encerrar: Ctrl+C")
print("="*50 + "\n")
app.run(debug=False, port=5000, host='0.0.0.0')
