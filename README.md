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

## IMPORTANTE - Requisitos de Sistema

**O TensorFlow 2.19.0 NÃO tem suporte nativo para Windows.** Para executar este projeto no Windows, você **DEVE** usar o WSL (Windows Subsystem for Linux).


## Getting Started

### 1. Pré-requisitos

#### Para Usuários Windows: Configurar WSL2

**IMPORTANTE:** Se você está no Windows, siga estas etapas primeiro antes de continuar:

1. **Instalar WSL2:**
   ```powershell
   wsl --install
   ```
   Reinicie o computador quando solicitado.

2. **Instalar Ubuntu no WSL:**
   ```powershell
   wsl --install -d Ubuntu
   ```

3. **Configurar usuário e senha** quando o Ubuntu iniciar pela primeira vez.

4. **Atualizar pacotes do Ubuntu:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

5. **Instalar Python 3.8+ no WSL:**
   ```bash
   sudo apt install python3 python3-pip python3-venv -y
   ```

6. **Verificar instalação:**
   ```bash
   python3 --version
   ```

**Documentação oficial:**
- **Instalação do WSL:** https://learn.microsoft.com/pt-br/windows/wsl/install
- **Instalação do TensorFlow:** https://www.tensorflow.org/install/pip

#### Para Usuários Linux/macOS:

Certifique-se de ter o **Python 3.8+** instalado:

```bash
python3 --version
```

### 2. Configuração do Ambiente

1. **Abra o terminal** (WSL no Windows, terminal normal no Linux/macOS)

2. **Clone ou baixe o projeto** para sua máquina local

3. **Navegue até a pasta do projeto:**
   ```bash
   cd /caminho/para/PagModelo
   ```

4. **Crie um ambiente virtual:**
   ```bash
   python3 -m venv venv_oct_analysis
   ```

5. **Ative o ambiente virtual:**

   **No WSL/Linux:**
   ```bash
   source venv_oct_analysis/bin/activate
   ```

   **No macOS:**
   ```bash
   source venv_oct_analysis/bin/activate
   ```

### 3. Instalação das Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Ou instale individualmente:**
```bash
pip install flask==3.1.1
pip install tensorflow==2.19.0
pip install numpy==2.1.3
pip install opencv-python==4.11.0.86
pip install pillow==11.1.0
```

### 4. Estrutura do Projeto

Certifique-se de que seu projeto tenha a seguinte estrutura:

```
projeto/
│
├── app.py                 # Aplicação Flask principal
├── run.py                 # Script para executar o servidor
├── requirements.txt       # Dependências do projeto
├── modelos baixados/      # Pasta com o modelo treinado
│   └── best_model_custom.keras
├── templates/             # Templates HTML
│   ├── index.html
│   └── result.html
└── static/               # Arquivos CSS/JS
    └── style.css
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

**Nota para usuários WSL:** Você pode acessar a aplicação no seu navegador Windows normalmente usando esses endereços.

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
- **TensorFlow 2.19.0** - Deep learning (requer WSL no Windows)
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

### Erro: TensorFlow não instala no Windows nativo

**Problema:** Tentou instalar o TensorFlow 2.19.0 diretamente no Windows (PowerShell/CMD).

**Solução:** Use WSL2 conforme instruções acima. O TensorFlow 2.19.0 requer ambiente Linux.

### Erro no WSL: "python: command not found"

Use `python3` ao invés de `python`:
```bash
python3 run.py
```

### Aviso sobre variáveis do otimizador

Se aparecer o aviso:
```
UserWarning: Skipping variable loading for optimizer 'adam', because it has 96 variables whereas the saved optimizer has 100 variables.
```

Este é um aviso normal devido a diferenças entre versões do TensorFlow. O modelo funcionará corretamente.

### Problemas de GPU 

Para usar GPU com TensorFlow, instale as dependências CUDA apropriadas conforme a documentação oficial do TensorFlow.

### Erro: TypeError: list indices must be integers or slices, not tuple

Se você encontrar este erro na função `make_gradcam_heatmap`, é devido a uma incompatibilidade no formato de saída do modelo no TensorFlow 2.19.0.

**Solução:** Na função `make_gradcam_heatmap` (arquivo `app.py`), adicione esta verificação logo após desempacotar os outputs:

```python
last_conv_layer_output, preds = grad_model(img_array, training=False)
# Corrige formato do preds
if isinstance(preds, (list, tuple)):
    preds = tf.convert_to_tensor(preds[0])  # Converte lista -> tensor
preds = tf.reshape(preds, [-1])  # Garante formato correto
```

Esta correção garante compatibilidade com TensorFlow 2.19.0 e versões futuras.

## Contribuição

Para contribuir com o projeto:

1. Faça fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Suporte

Em caso de dúvidas ou problemas:
- **Primeiro:** Verifique se está usando WSL no Windows
- Confirme que todas as dependências estão instaladas corretamente
- Verifique se o modelo está no local correto
- Teste com imagens de diferentes formatos
- Consulte os logs de erro no terminal para diagnóstico
- Consulte a documentação oficial do TensorFlow: https://www.tensorflow.org/install/pip

---

**Nota:** Este sistema é desenvolvido para fins de pesquisa e apoio ao diagnóstico médico. Sempre consulte um profissional de saúde qualificado para diagnósticos definitivos.