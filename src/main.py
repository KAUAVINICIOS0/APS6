import sys
import os
import random

# Adicionar o diretório pai ao path para importar carregar_dataset
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from carregar_dataset import baixar_e_listar_imagens
from src.autenticacao import autenticar
from src.db import init_db, criar_usuario, listar_usuarios, consultar_propriedades_por_nivel, registrar_log

def main():
    """
    Função principal do sistema de autenticação por impressão digital.
    """
    print(" SISTEMA DE AUTENTICAÇÃO POR IMPRESSÃO DIGITAL")
    print("=" * 50)
    
    try:
        print(" Inicializando banco de dados...")
        init_db(seed=True)

        print(" Baixando dataset do Kaggle...")
        imagens = baixar_e_listar_imagens()
        if len(imagens) < 2:
            print(" Dataset insuficiente para operação.")
            return

        print(f"\n Dataset carregado com {len(imagens)} imagens")

        sessao = {"usuario": None}

        while True:
            print("\n" + "=" * 60)
            print(" MENU PRINCIPAL:")
            print("1. Cadastrar usuário (matrícula biométrica)")
            print("2. Login biométrico")
            print("3. Consultar dados (acesso por nível)")
            print("4. Listar usuários cadastrados")
            print("5. Sair")

            opcao = input("\nEscolha uma opção (1-5): ").strip()

            if opcao == "1":
                cadastrar_usuario(imagens)
            elif opcao == "2":
                sessao["usuario"] = login_biometrico(imagens)
            elif opcao == "3":
                consultar_dados(sessao)
            elif opcao == "4":
                mostrar_usuarios()
            elif opcao == "5":
                print(" Encerrando sistema...")
                break
            else:
                print(" Opção inválida. Tente novamente.")

    except Exception as e:
        print(f"Erro no sistema: {e}")

def teste_automatico(imagens):
    """Teste automático com duas imagens aleatórias."""
    print("\n TESTE AUTOMÁTICO")
    print("-" * 30)
    
    # Escolher duas imagens aleatórias
    img1, img2 = random.sample(imagens, 2)
    
    print(f" Imagem 1: {img1.split('/')[-1]}")
    print(f" Imagem 2: {img2.split('/')[-1]}")
    
    # Testar com diferentes limiares
    limiares = [50, 60, 70, 80]
    for limiar in limiares:
        print(f"\n Testando com limiar {limiar}%:")
        resultado = autenticar(img1, img2, limiar=limiar)
        print(f"   Resultado: {' Autenticado' if resultado else ' Negado'}")

def teste_manual(imagens):
    """Teste manual onde o usuário escolhe as imagens."""
    print("\n👤 TESTE MANUAL")
    print("-" * 30)
    
    # Mostrar algumas imagens disponíveis
    print("Imagens disponíveis (primeiras 10):")
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
            print("Índices inválidos.")
            
    except ValueError:
        print("Entrada inválida.")

def teste_multiplas_comparacoes(imagens):
    """Teste com múltiplas comparações para análise estatística."""
    print("\n TESTE DE MÚLTIPLAS COMPARAÇÕES")
    print("-" * 40)
    
    num_testes = min(10, len(imagens) // 2)
    limiar = 60
    
    print(f"Executando {num_testes} comparações com limiar {limiar}%...")
    
    resultados = []
    for i in range(num_testes):
        img1, img2 = random.sample(imagens, 2)
        resultado = autenticar(img1, img2, limiar=limiar)
        resultados.append(resultado)
        print(f"Teste {i+1}: {'' if resultado else ''}")
    
    # Estatísticas
    autenticados = sum(resultados)
    taxa_autenticacao = (autenticados / num_testes) * 100
    
    print(f"\n ESTATÍSTICAS:")
    print(f"   Total de testes: {num_testes}")
    print(f"   Autenticações bem-sucedidas: {autenticados}")
    print(f"   Taxa de autenticação: {taxa_autenticacao:.1f}%")


def mostrar_imagens_disponiveis(imagens, limite=10):
    print("Imagens disponíveis (primeiras {}):".format(limite))
    for i, img in enumerate(imagens[:limite]):
        print(f"   {i+1}. {img.split('/')[-1]}")


def cadastrar_usuario(imagens):
    print("\n CADASTRAR USUÁRIO")
    print("-" * 30)

    nome = input("Nome do usuário: ").strip()
    try:
        nivel = int(input("Nível de acesso (1=Todos, 2=Diretores, 3=Ministro): ").strip())
    except ValueError:
        print(" Nível inválido.")
        return

    if nivel not in (1, 2, 3):
        print(" Nível deve ser 1, 2 ou 3.")
        return

    print("")
    mostrar_imagens_disponiveis(imagens)
    try:
        idx = int(input("Escolha a imagem para registrar (1-10) ou 0 para caminho manual: ").strip())
    except ValueError:
        print(" Entrada inválida.")
        return

    if idx == 0:
        caminho = input("Caminho completo da imagem: ").strip()
    else:
        if 1 <= idx <= min(10, len(imagens)):
            caminho = imagens[idx - 1]
        else:
            print(" Índice inválido.")
            return

    if not os.path.exists(caminho):
        print(" Arquivo não encontrado.")
        return

    user_id = criar_usuario(nome, nivel, caminho)
    registrar_log(user_id, "cadastro_usuario", True)
    print(f" Usuário cadastrado com ID {user_id} e nível {nivel}.")


def login_biometrico(imagens):
    print("\n LOGIN BIOMÉTRICO")
    print("-" * 30)

    usuarios = listar_usuarios()
    if len(usuarios) == 0:
        print(" Nenhum usuário cadastrado. Cadastre primeiro.")
        return None

    print("Usuários:")
    for u in usuarios:
        print(f"   {u['id']}. {u['nome']} (nível {u['nivel']})")

    try:
        uid = int(input("Escolha o ID do usuário para autenticar: ").strip())
    except ValueError:
        print(" Entrada inválida.")
        return None

    selecionado = None
    for u in usuarios:
        if u["id"] == uid:
            selecionado = u
            break

    if selecionado is None:
        print(" Usuário não encontrado.")
        return None

    print("")
    mostrar_imagens_disponiveis(imagens)
    try:
        idx = int(input("Escolha a imagem de teste (1-10) ou 0 para caminho manual: ").strip())
    except ValueError:
        print(" Entrada inválida.")
        return None

    if idx == 0:
        img_teste = input("Caminho completo da imagem de teste: ").strip()
    else:
        if 1 <= idx <= min(10, len(imagens)):
            img_teste = imagens[idx - 1]
        else:
            print(" Índice inválido.")
            return None

    if not os.path.exists(img_teste):
        print(" Arquivo de teste não encontrado.")
        return None

    ok = autenticar(selecionado["imagem_registrada"], img_teste, limiar=60)
    registrar_log(selecionado["id"], "login", ok)
    if ok:
        print(f" Login bem-sucedido. Bem-vindo, {selecionado['nome']} (nível {selecionado['nivel']}).")
        return selecionado
    else:
        print(" Falha na autenticação biométrica.")
        return None


def consultar_dados(sessao):
    print("\n CONSULTAR DADOS")
    print("-" * 30)
    if not sessao.get("usuario"):
        print(" É necessário estar logado para consultar dados.")
        return

    nivel = sessao["usuario"]["nivel"]
    linhas = consultar_propriedades_por_nivel(nivel)
    if len(linhas) == 0:
        print(" Nenhum dado disponível para seu nível de acesso.")
        return

    print(f" Dados disponíveis para nível {nivel}:")
    for r in linhas:
        print(
            f" - [{r['nivel_minimo']}] {r['nome']} | {r['localizacao']} | Agrotóxicos: {r['agrotoxicos_proibidos']} | Impacto: {r['impacto']}"
        )


def mostrar_usuarios():
    print("\n USUÁRIOS CADASTRADOS")
    print("-" * 30)
    usuarios = listar_usuarios()
    if len(usuarios) == 0:
        print(" Nenhum usuário cadastrado.")
        return
    for u in usuarios:
        print(f" - ID {u['id']}: {u['nome']} (nível {u['nivel']}) [img: {os.path.basename(u['imagem_registrada'])}]")

if __name__ == "__main__":
    main()
