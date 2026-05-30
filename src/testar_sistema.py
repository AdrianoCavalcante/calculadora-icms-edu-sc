"""
Script de Teste - Sistema IQESC Automático
Testa a funcionalidade de download automático para diferentes anos
"""
import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from calculadora.calculadora_iqesc import CalculadoraIQESC

def testar_ano(ano, auto_download=True):
    """
    Testa carregamento de dados para um ano específico
    
    Args:
        ano: Ano a testar
        auto_download: Se True, tenta download automático
    """
    print("\n" + "="*80)
    print(f"🧪 TESTANDO ANO: {ano}")
    print("="*80)
    
    try:
        print(f"\n📋 Configuração:")
        print(f"   - Ano: {ano}")
        print(f"   - Download automático: {'✅ SIM' if auto_download else '❌ NÃO'}")
        
        # Tenta carregar
        print(f"\n🔍 Tentando carregar dados...")
        calc = CalculadoraIQESC(ano=ano, auto_download=auto_download)
        
        # Estatísticas
        stats = calc.calcular_estatisticas_gerais()
        
        print(f"\n✅ SUCESSO!")
        print(f"\n📊 Estatísticas:")
        print(f"   - Total de municípios: {stats['total_municipios']}")
        print(f"   - IQESC médio: {stats['iqesc']['media']:.4f}")
        print(f"   - IQESC máximo: {stats['iqesc']['maximo']:.4f}")
        print(f"   - IQESC mínimo: {stats['iqesc']['minimo']:.4f}")
        
        # Top 3
        print(f"\n🏆 Top 3 Municípios:")
        ranking = calc.ranking_municipios(top_n=3)
        for i, m in enumerate(ranking, 1):
            print(f"   {i}º - {m['nome']}: {m['iqesc']:.4f}")
        
        return True
        
    except FileNotFoundError as e:
        print(f"\n❌ DADOS NÃO ENCONTRADOS")
        print(f"   {e}")
        return False
        
    except Exception as e:
        print(f"\n❌ ERRO")
        print(f"   {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Menu principal de testes"""
    print("\n" + "="*80)
    print("🧪 TESTE DO SISTEMA IQESC AUTOMÁTICO")
    print("="*80)
    
    print("""
Este script testa a funcionalidade de download automático do sistema.

Opções:
1. Testar ano 2024 (deve ter cache)
2. Testar ano 2023 (pode precisar download)
3. Testar ano 2022 (pode precisar download)
4. Testar ano customizado
5. Testar múltiplos anos
0. Sair
    """)
    
    while True:
        try:
            opcao = input("\n👉 Escolha uma opção (0-5): ").strip()
            
            if opcao == "0":
                print("\n👋 Saindo...")
                break
                
            elif opcao == "1":
                testar_ano(2024, auto_download=True)
                
            elif opcao == "2":
                testar_ano(2023, auto_download=True)
                
            elif opcao == "3":
                testar_ano(2022, auto_download=True)
                
            elif opcao == "4":
                ano = int(input("Digite o ano: "))
                testar_ano(ano, auto_download=True)
                
            elif opcao == "5":
                anos_input = input("Digite os anos separados por vírgula (ex: 2022,2023,2024): ")
                anos = [int(a.strip()) for a in anos_input.split(",")]
                
                resultados = {}
                for ano in anos:
                    sucesso = testar_ano(ano, auto_download=True)
                    resultados[ano] = sucesso
                
                # Resumo
                print("\n" + "="*80)
                print("📋 RESUMO DOS TESTES")
                print("="*80)
                for ano, sucesso in resultados.items():
                    status = "✅ SUCESSO" if sucesso else "❌ FALHOU"
                    print(f"   {ano}: {status}")
                
            else:
                print("⚠️  Opção inválida!")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário")
            break
        except ValueError as e:
            print(f"⚠️  Erro: Digite um número válido")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print("\n" + "="*80)
    print("🏁 TESTE CONCLUÍDO")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
