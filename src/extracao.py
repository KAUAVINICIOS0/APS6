import cv2
import numpy as np

def extrair_caracteristicas(imagem):
    """
    Extrai características de uma imagem de impressão digital usando ORB.
    """
    try:
        if imagem is None:
            return None, None
            
        # Criar detector ORB com parâmetros otimizados para impressões digitais
        orb = cv2.ORB_create(
            nfeatures=1000,  # Número de características
            scaleFactor=1.2,  # Fator de escala
            nlevels=8,        # Níveis da pirâmide
            edgeThreshold=15, # Limiar de borda
            firstLevel=0,     # Primeiro nível
            WTA_K=2,          # Número de pontos para WTA
            scoreType=cv2.ORB_HARRIS_SCORE,  # Tipo de pontuação
            patchSize=31      # Tamanho do patch
        )
        
        keypoints, descritores = orb.detectAndCompute(imagem, None)
        
        if descritores is not None:
            print(f"✅ Extraídas {len(keypoints)} características")
        else:
            print("⚠️ Nenhuma característica extraída")
            
        return keypoints, descritores
        
    except Exception as e:
        print(f"Erro na extração de características: {e}")
        return None, None

def comparar_digitais(desc1, desc2):
    """
    Compara duas impressões digitais usando matching de características.
    Retorna um score de similaridade (0-100).
    """
    try:
        if desc1 is None or desc2 is None:
            return 0
            
        # Criar matcher BF (Brute Force)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
        # Encontrar matches
        matches = bf.match(desc1, desc2)
        
        if len(matches) == 0:
            return 0
            
        # Ordenar matches por distância
        matches = sorted(matches, key=lambda x: x.distance)
        
        # Calcular score baseado na qualidade dos matches
        # Considerar apenas os melhores matches (menor distância)
        num_good_matches = min(len(matches), 50)  # Top 50 matches
        good_matches = matches[:num_good_matches]
        
        # Calcular distância média dos melhores matches
        avg_distance = np.mean([m.distance for m in good_matches])
        
        # Converter distância em score (0-100)
        # Distâncias menores = maior similaridade
        max_distance = 100  # Distância máxima esperada
        score = max(0, 100 - (avg_distance / max_distance) * 100)
        
        print(f"🔍 {len(matches)} matches encontrados, {num_good_matches} melhores")
        print(f"📊 Distância média: {avg_distance:.2f}, Score: {score:.2f}")
        
        return score
        
    except Exception as e:
        print(f"Erro na comparação: {e}")
        return 0
