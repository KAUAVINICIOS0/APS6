from .preprocessamento import preprocessar_imagem
from .extracao import extrair_caracteristicas, comparar_digitais
import os

def autenticar(imagem_registrada, imagem_teste, limiar=60):
    """
    Autentica uma impressão digital comparando com uma imagem registrada.
    
    Args:
        imagem_registrada (str): Caminho para a imagem registrada
        imagem_teste (str): Caminho para a imagem de teste
        limiar (int): Limiar de similaridade para autenticação (0-100)
    
    Returns:
        bool: True se autenticado, False caso contrário
    """
    try:
        print(f"\n Iniciando autenticação...")
        print(f" Imagem registrada: {os.path.basename(imagem_registrada)}")
        print(f" Imagem de teste: {os.path.basename(imagem_teste)}")
        
        # Verificar se os arquivos existem
        if not os.path.exists(imagem_registrada):
            print(f" Erro: Imagem registrada não encontrada: {imagem_registrada}")
            return False
            
        if not os.path.exists(imagem_teste):
            print(f" Erro: Imagem de teste não encontrada: {imagem_teste}")
            return False
        
        # Pré-processar ambas as imagens
        print("\n Pré-processando imagens...")
        img1 = preprocessar_imagem(imagem_registrada)
        img2 = preprocessar_imagem(imagem_teste)
        
        if img1 is None or img2 is None:
            print(" Erro no pré-processamento das imagens")
            return False
        
        # Extrair características
        print("\n Extraindo características...")
        _, desc1 = extrair_caracteristicas(img1)
        _, desc2 = extrair_caracteristicas(img2)
        
        if desc1 is None or desc2 is None:
            print(" Erro na extração de características")
            return False
        
        # Comparar as impressões digitais
        print("\n Comparando impressões digitais...")
        similaridade = comparar_digitais(desc1, desc2)
        
        print(f"\n RESULTADO DA AUTENTICAÇÃO:")
        print(f"   similaridade: {similaridade:.2f}%")
        print(f"   Limiar: {limiar}%")
        
        # Decisão de autenticação
        if similaridade >= limiar:
            print(" ACESSO PERMITIDO - Impressões digitais correspondem!")
            return True
        else:
            print(" ACESSO NEGADO - Impressões digitais não correspondem")
            return False
            
    except Exception as e:
        print(f" Erro durante a autenticação: {e}")
        return False
