# core/memoria.py

import json
from typing import Dict, List, Any
import os

class GerenciadorMemoria:
    def __init__(self, arquivo_memoria: str = 'memoria.json'):
        self.arquivo_memoria = arquivo_memoria
        self.memoria = self.carregar_memoria()
        self.tamanho_maximo = 1000  # Limite máximo de itens na memória

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
        if len(self.memoria) >= self.tamanho_maximo:
            # Remove o item mais antigo
            chave_antiga = next(iter(self.memoria))
            del self.memoria[chave_antiga]
        
        self.memoria[chave] = valor
        self.salvar_memoria()

    def obter_informacao(self, chave: str) -> Any:
        return self.memoria.get(chave)

    def listar_chaves(self) -> List[str]:
        return list(self.memoria.keys())

    def limpar_memoria(self):
        self.memoria.clear()
        self.salvar_memoria()

    def tamanho_memoria(self) -> int:
        return len(self.memoria)

    def backup_memoria(self, arquivo_backup: str):
        with open(arquivo_backup, 'w') as f:
            json.dump(self.memoria, f, indent=2)

if __name__ == "__main__":
    # Teste básico
    memoria = GerenciadorMemoria()
    memoria.adicionar_informacao("nome_usuario", "João")
    print(f"Nome do usuário: {memoria.obter_informacao('nome_usuario')}")
    print(f"Chaves na memória: {memoria.listar_chaves()}")
    print(f"Tamanho da memória: {memoria.tamanho_memoria()}")
    memoria.backup_memoria("backup_memoria.json")
    memoria.limpar_memoria()
    print(f"Tamanho da memória após limpeza: {memoria.tamanho_memoria()}")