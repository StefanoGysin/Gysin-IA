# core/memoria.py

import json
from typing import Dict, List, Any

class GerenciadorMemoria:
    def __init__(self, arquivo_memoria: str = 'memoria.json'):
        self.arquivo_memoria = arquivo_memoria
        self.memoria = self.carregar_memoria()

    def carregar_memoria(self) -> Dict[str, Any]:
        try:
            with open(self.arquivo_memoria, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def salvar_memoria(self):
        with open(self.arquivo_memoria, 'w') as f:
            json.dump(self.memoria, f, indent=2)

    def adicionar_informacao(self, chave: str, valor: Any):
        self.memoria[chave] = valor
        self.salvar_memoria()

    def obter_informacao(self, chave: str) -> Any:
        return self.memoria.get(chave)

    def listar_chaves(self) -> List[str]:
        return list(self.memoria.keys())

if __name__ == "__main__":
    # Teste básico
    memoria = GerenciadorMemoria()
    memoria.adicionar_informacao("nome_usuario", "João")
    print(f"Nome do usuário: {memoria.obter_informacao('nome_usuario')}")
    print(f"Chaves na memória: {memoria.listar_chaves()}")
