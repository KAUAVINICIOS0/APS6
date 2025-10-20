import kagglehub
import os
import time

def baixar_e_listar_imagens():
    """
    Baixa o dataset de impressões digitais do Kaggle e retorna lista de imagens.
    """
    try:
        print("🔄 Baixando dataset do Kaggle...")
        print("📦 Dataset: kundurunonieshreddy/finger-print-dataset")
        
        # Baixar o dataset do Kaggle
        start_time = time.time()
        path = kagglehub.dataset_download("kundurunonieshreddy/finger-print-dataset")
        download_time = time.time() - start_time
        
        print(f"✅ Dataset baixado com sucesso!")
        print(f"📁 Localização: {path}")
        print(f"⏱️ Tempo de download: {download_time:.2f} segundos")

        # Listar as imagens encontradas
        print("\n🔍 Procurando imagens no dataset...")
        imagens = []
        
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
                    full_path = os.path.join(root, file)
                    imagens.append(full_path)

        print(f"📊 Total de imagens encontradas: {len(imagens)}")
        
        if len(imagens) > 0:
            print("📁 Primeiras 5 imagens:")
            for i, img in enumerate(imagens[:5]):
                print(f"   {i+1}. {os.path.basename(img)}")
            
            if len(imagens) > 5:
                print(f"   ... e mais {len(imagens) - 5} imagens")
        else:
            print("⚠️ Nenhuma imagem encontrada no dataset!")
            
        return imagens
        
    except Exception as e:
        print(f"❌ Erro ao baixar o dataset: {e}")
        print("💡 Verifique sua conexão com a internet e suas credenciais do Kaggle")
        return []
