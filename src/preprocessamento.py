import cv2
import numpy as np

def preprocessar_imagem(caminho_imagem):
    """
    Pré-processa uma imagem de impressão digital para melhorar a extração de características.
    """
    try:
        # Carregar imagem em escala de cinza
        img = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Não foi possível carregar a imagem: {caminho_imagem}")
        
        # Redimensionar para tamanho padrão
        img = cv2.resize(img, (300, 300))
        
        # Aplicar filtro gaussiano para reduzir ruído
        img = cv2.GaussianBlur(img, (3, 3), 0)
        
        # Melhorar o contraste usando CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img = clahe.apply(img)
        
        # Binarização usando Otsu
        _, binaria = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Operações morfológicas para limpar a imagem
        kernel = np.ones((2,2), np.uint8)
        binaria = cv2.morphologyEx(binaria, cv2.MORPH_CLOSE, kernel)
        binaria = cv2.morphologyEx(binaria, cv2.MORPH_OPEN, kernel)
        
        return binaria
        
    except Exception as e:
        print(f"Erro no pré-processamento: {e}")
        return None
