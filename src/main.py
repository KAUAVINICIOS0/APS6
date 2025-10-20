import sys
import os
import random

# Adicionar o diretório pai ao path para importar carregar_dataset
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from carregar_dataset import baixar_e_listar_imagens
from src.autenticacao import autenticar

def main():
    """
    Função principal do sistema de autenticação por impressão digital.
    """
    print("🔐 SISTEMA DE AUTENTICAÇÃO POR IMPRESSÃO DIGITAL")
    print("=" * 50)
    
    try:
        # Baixar dataset e obter imagens
        print("📥 Baixando dataset do Kaggle...")
        imagens = baixar_e_listar_imagens()
        
        if len(imagens) < 2:
            print("❌ Dataset insuficiente para comparação.")
            return
        
        print(f"\n✅ Dataset carregado com {len(imagens)} imagens")
        
        # Menu de opções
        while True:
            print("\n" + "=" * 50)
            print("📋 MENU DE OPÇÕES:")
            print("1. Teste automático (comparar duas imagens aleatórias)")
            print("2. Teste manual (escolher imagens específicas)")
            print("3. Teste de múltiplas comparações")
            print("4. Sair")
            
            opcao = input("\nEscolha uma opção (1-4): ").strip()
            
            if opcao == "1":
                teste_automatico(imagens)
            elif opcao == "2":
                teste_manual(imagens)
            elif opcao == "3":
                teste_multiplas_comparacoes(imagens)
            elif opcao == "4":
                print("👋 Encerrando sistema...")
                break
            else:
                print("❌ Opção inválida. Tente novamente.")
                
    except Exception as e:
        print(f"❌ Erro no sistema: {e}")

def teste_automatico(imagens):
    """Teste automático com duas imagens aleatórias."""
    print("\n🎲 TESTE AUTOMÁTICO")
    print("-" * 30)
    
    # Escolher duas imagens aleatórias
    img1, img2 = random.sample(imagens, 2)
    
    print(f"📁 Imagem 1: {img1.split('/')[-1]}")
    print(f"📁 Imagem 2: {img2.split('/')[-1]}")
    
    # Testar com diferentes limiares
    limiares = [50, 60, 70, 80]
    for limiar in limiares:
        print(f"\n🔍 Testando com limiar {limiar}%:")
        resultado = autenticar(img1, img2, limiar=limiar)
        print(f"   Resultado: {'✅ Autenticado' if resultado else '❌ Negado'}")

def teste_manual(imagens):
    """Teste manual onde o usuário escolhe as imagens."""
    print("\n👤 TESTE MANUAL")
    print("-" * 30)
    
    # Mostrar algumas imagens disponíveis
    print("📁 Imagens disponíveis (primeiras 10):")
    for i, img in enumerate(imagens[:10]):
        print(f"   {i+1}. {img.split('/')[-1]}")
    
    try:
        idx1 = int(input("\nEscolha o índice da primeira imagem (1-10): ")) - 1
        idx2 = int(input("Escolha o índice da segunda imagem (1-10): ")) - 1
        
        if 0 <= idx1 < len(imagens) and 0 <= idx2 < len(imagens):
            img1 = imagens[idx1]
            img2 = imagens[idx2]
            
            limiar = int(input("Digite o limiar de similaridade (0-100): ") or "60")
            
            autenticar(img1, img2, limiar=limiar)
        else:
            print("❌ Índices inválidos.")
            
    except ValueError:
        print("❌ Entrada inválida.")

def teste_multiplas_comparacoes(imagens):
    """Teste com múltiplas comparações para análise estatística."""
    print("\n📊 TESTE DE MÚLTIPLAS COMPARAÇÕES")
    print("-" * 40)
    
    num_testes = min(10, len(imagens) // 2)
    limiar = 60
    
    print(f"Executando {num_testes} comparações com limiar {limiar}%...")
    
    resultados = []
    for i in range(num_testes):
        img1, img2 = random.sample(imagens, 2)
        resultado = autenticar(img1, img2, limiar=limiar)
        resultados.append(resultado)
        print(f"Teste {i+1}: {'✅' if resultado else '❌'}")
    
    # Estatísticas
    autenticados = sum(resultados)
    taxa_autenticacao = (autenticados / num_testes) * 100
    
    print(f"\n📈 ESTATÍSTICAS:")
    print(f"   Total de testes: {num_testes}")
    print(f"   Autenticações bem-sucedidas: {autenticados}")
    print(f"   Taxa de autenticação: {taxa_autenticacao:.1f}%")

if __name__ == "__main__":
    main()
