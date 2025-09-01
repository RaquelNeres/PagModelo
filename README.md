# OCT Image Analysis - Diagnóstico de Doenças Retinianas

## Introdução

Este projeto implementa um sistema de análise automatizada de imagens de Tomografia de Coerência Óptica (OCT) para diagnóstico de doenças retinianas. Utilizando redes neurais convolucionais e técnicas de explainabilidade (Grad-CAM), o sistema é capaz de classificar imagens OCT em quatro categorias principais:

- **CNV** - Neovascularização Coroidal
- **DME** - Edema Macular Diabético  
- **DRUSEN** - Drusas
- **NORMAL** - Retina Normal

As tecnologias utilizadas incluem: **Flask** (backend), **TensorFlow/Keras** (machine learning), **OpenCV** (processamento de imagens) e **Grad-CAM** (visualização de ativações).

## Funcionalidades

- Upload e análise de imagens OCT
- Classificação automática com percentual de confiança
- Visualização das regiões de interesse através do Grad-CAM
- Pré-processamento automático das imagens (remoção de bordas e equalização)
- Interface web intuitiva para uso médico

## Getting Started

### 1. Pré-requisitos

Certifique-se de ter o **Python 3.8+** instalado em sua máquina. Você pode verificar executando:

```bash
python --version
```

### 2. Configuração do Ambiente

1. Clone ou baixe o projeto para sua máquina local
2. Navegue até a pasta do projeto no terminal
3. Crie um ambiente virtual para isolamento das dependências:

```bash
python -m venv venv_oct_analysis
```

4. Ative o ambiente virtual:

**No Windows (PowerShell):**
```bash
./venv_oct_analysis/Scripts/Activate.ps1
```

**No Windows (CMD):**
```bash
venv_oct_analysis\Scripts\activate
```

**No Linux/MacOS:**
```bash
source venv_oct_analysis/bin/activate
```

### 3. Instalação das Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:

```bash
pip install flask==3.1.1
pip install tensorflow==2.19.0
pip install numpy==2.1.3
pip install opencv-python==4.11.0.86
pip install pillow==11.1.0
```

**Ou use o arquivo requirements.txt:**
```bash
pip install -r requirements.txt
```

### 4. Estrutura do Projeto

Certifique-se de que seu projeto tenha a seguinte estrutura:

```
projeto/
│
├── app.py                 # Aplicação Flask principal
├── run.py                 # Script para executar o servidor
├── modelos baixados/      # Pasta com o modelo treinado
│   └── best_model_custom.keras
├── templates/             # Templates HTML
│   ├── index.html
│   └── result.html
└── static/               # Arquivos CSS/JS 
```

### 5. Modelo de Machine Learning

O projeto requer um modelo Keras treinado localizado em:
```
modelos baixados/best_model_custom.keras
```

**Importante:** Certifique-se de que o modelo esteja na pasta correta antes de executar a aplicação.

### 6. Executando a Aplicação

Com todas as dependências instaladas e o modelo no lugar correto:

```bash
python run.py
```

Ou diretamente:
```bash
python app.py
```

A aplicação estará disponível em: **http://localhost:5000** ou **http://127.0.0.1:5000**

### 7. Utilizando o Sistema

1. Acesse a URL no seu navegador
2. Faça upload de uma imagem OCT (formatos suportados: JPG, PNG, etc.)
3. Aguarde o processamento (alguns segundos)
4. Visualize os resultados:
   - Classificação prevista
   - Percentual de confiança
   - Probabilidades para todas as classes
   - Imagem original processada
   - Mapa de calor Grad-CAM

## Especificações Técnicas

### Bibliotecas Principais
- **Flask 3.1.1** - Framework web
- **TensorFlow 2.19.0** - Deep learning
- **OpenCV 4.11.0** - Processamento de imagens
- **NumPy 2.1.3** - Computação numérica
- **Pillow 11.1.0** - Manipulação de imagens

### Processamento de Imagens
- Remoção automática de bordas e legendas (8% superior/inferior, 4% laterais)
- Equalização adaptativa de contraste (CLAHE)
- Redimensionamento para 224x224 pixels
- Normalização para entrada do modelo

### Limitações
- Tamanho máximo de arquivo: **5MB**
- Formatos suportados: JPG, PNG, BMP, TIFF
- Formatos não suportados: AVIF, WEBP (alguns casos)

## Troubleshooting

### Erro de Import do TensorFlow
Se encontrar erros relacionados ao TensorFlow, tente:
```bash
pip install tensorflow==2.19.0 --upgrade
```

### Erro no OpenCV
Para problemas com o OpenCV:
```bash
pip uninstall opencv-python
pip install opencv-python==4.11.0.86
```

### Modelo não encontrado
Verifique se o arquivo `best_model_custom.keras` está na pasta `modelos baixados/` e se o caminho no código está correto.

### Problemas de GPU (Opcional)
Para usar GPU com TensorFlow, instale as dependências CUDA apropriadas conforme a documentação oficial do TensorFlow.

## Contribuição

Para contribuir com o projeto:

1. Faça fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Suporte

Em caso de dúvidas ou problemas:
- Verifique se todas as dependências estão instaladas corretamente
- Confirme que o modelo está no local correto
- Teste com imagens de diferentes formatos
- Consulte os logs de erro no terminal para diagnóstico

---

**Nota:** Este sistema é desenvolvido para fins de pesquisa e apoio ao diagnóstico médico. Sempre consulte um profissional de saúde qualificado para diagnósticos definitivos.