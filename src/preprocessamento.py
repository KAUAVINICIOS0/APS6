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
        
        # Redimensionar para tamanho padrão (mantém proporção se possível)
        img = cv2.resize(img, (300, 300), interpolation=cv2.INTER_AREA)
        
        # Normalização básica
        img = img.astype(np.float32)
        
        # Aplicar filtro gaussiano para reduzir ruído (ajustado para melhor preservação)
        img = cv2.GaussianBlur(img, (5, 5), 1.5)
        
        # Melhorar o contraste usando CLAHE (Contrast Limited Adaptive Histogram Equalization)
        # Parâmetros otimizados para impressões digitais
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        img = clahe.apply(img.astype(np.uint8))
        
        # Normalização final para melhorar extração de características
        # Usar equalização adaptativa adicional
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        
        # Filtro de aguçamento leve para realçar cristas
        kernel_sharpen = np.array([[-1, -1, -1],
                                   [-1,  9, -1],
                                   [-1, -1, -1]]) * 0.1
        img = cv2.filter2D(img, -1, kernel_sharpen)
        
        # Normalização final
        img = np.clip(img, 0, 255).astype(np.uint8)
        
        return img
        
    except Exception as e:
        print(f"Erro no pré-processamento: {e}")
        return None
