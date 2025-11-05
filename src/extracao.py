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
            nfeatures=1500,
            scaleFactor=1.2,
            nlevels=8,
            edgeThreshold=15,
            firstLevel=0,
            WTA_K=2,
            scoreType=cv2.ORB_HARRIS_SCORE,
            patchSize=31
        )
        
        keypoints, descritores = orb.detectAndCompute(imagem, None)
        
        # Validação mínima de qualidade
        if descritores is None or keypoints is None or len(keypoints) < 10:
            print(f"Aviso: poucas características extraídas ({len(keypoints) if keypoints else 0})")
            return None, None
        
        print(f"Extraídas {len(keypoints)} características")
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
        
        if len(desc1) < 10 or len(desc2) < 10:
            print("Aviso: poucos descritores para comparar")
            return 0
        
        # BFMatcher sem crossCheck para permitir ratio test (Lowe)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        knn_matches = bf.knnMatch(desc1, desc2, k=2)
        
        # Ratio test para filtrar matches ambíguos
        ratio_threshold = 0.75
        good_matches = []
        for pair in knn_matches:
            if len(pair) == 2:
                m, n = pair
                if m.distance < ratio_threshold * n.distance:
                    good_matches.append(m)
        
        # Fallback: se nada passar no ratio test, usa matching simples
        if len(good_matches) == 0:
            fallback = bf.match(desc1, desc2)
            fallback = sorted(fallback, key=lambda x: x.distance)
            good_matches = fallback[:min(len(fallback), 100)]
        
        if len(good_matches) == 0:
            return 0
        
        # Ordenar por distância
        good_matches = sorted(good_matches, key=lambda x: x.distance)
        distances = [m.distance for m in good_matches]
        num_matches = len(good_matches)
        avg_distance = float(np.mean(distances))
        median_distance = float(np.median(distances))
        min_distance = float(np.min(distances))
        
        # Distância Hamming típica de ORB está em 0-64 (para 256 bits)
        max_expected_distance = 64.0
        distance_score = max(0.0, 100.0 - (avg_distance / max_expected_distance) * 100.0)
        
        # Score pela quantidade de matches (limitado)
        min_matches = 10.0
        max_matches = 200.0
        quantity_score = ((min(num_matches, max_matches) - min_matches) / (max_matches - min_matches)) * 30.0
        quantity_score = max(0.0, min(30.0, quantity_score))
        
        # Consistência: mediana próxima da média indica distribuição estável
        consistency = 1.0 - abs(median_distance - avg_distance) / (avg_distance + 1e-6)
        consistency_score = max(0.0, min(20.0, consistency * 20.0))
        
        score = distance_score * 0.5 + quantity_score * 0.3 + consistency_score * 0.2
        score = max(0.0, min(100.0, score))
        
        print(f"{num_matches} matches válidos (ratio test aplicado)")
        print(f"Dist. média: {avg_distance:.2f}, mediana: {median_distance:.2f}, mín: {min_distance:.2f}")
        print(f"Score: {score:.2f}% (dist: {distance_score:.1f}%, qtd: {quantity_score:.1f}%, consist: {consistency_score:.1f}%)")
        
        return score
        
    except Exception as e:
        print(f"Erro na comparação: {e}")
        return 0
