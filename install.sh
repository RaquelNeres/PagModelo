#!/bin/bash

# Script de instalação automatizada - OCT Image Analysis
# Para Ubuntu/Debian e derivados

set -e  # Para na primeira falha

echo "=========================================="
echo "  OCT Image Analysis - Instalação"
echo "=========================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se está rodando no Linux
if [[ "$OSYS" == "Windows_NT" ]]; then
    echo -e "${RED}❌ Este script é para Linux. Use WSL no Windows.${NC}"
    exit 1
fi

# Verificar se Python 3.8+ está instalado
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python3 não encontrado. Instalando...${NC}"
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
else
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo -e "${GREEN}✓ Python $PYTHON_VERSION encontrado${NC}"
fi

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  pip3 não encontrado. Instalando...${NC}"
    sudo apt install -y python3-pip
fi

# Criar ambiente virtual
echo ""
echo "📦 Criando ambiente virtual..."
if [ -d "venv_oct_analysis" ]; then
    echo -e "${YELLOW}⚠️  Ambiente virtual já existe. Removendo...${NC}"
    rm -rf venv_oct_analysis
fi

python3 -m venv venv_oct_analysis
echo -e "${GREEN}✓ Ambiente virtual criado${NC}"

# Ativar ambiente virtual
echo ""
echo "🔌 Ativando ambiente virtual..."
source venv_oct_analysis/bin/activate

# Atualizar pip
echo ""
echo "⬆️  Atualizando pip..."
pip install --upgrade pip --quiet

# Instalar dependências
echo ""
echo "📚 Instalando dependências (pode levar alguns minutos)..."
echo ""

pip install flask==3.1.1 --quiet
echo -e "${GREEN}✓ Flask instalado${NC}"

echo "   Instalando TensorFlow (isso pode demorar)..."
pip install tensorflow==2.19.0 --quiet
echo -e "${GREEN}✓ TensorFlow instalado${NC}"

pip install numpy==2.1.3 --quiet
echo -e "${GREEN}✓ NumPy instalado${NC}"

pip install opencv-python==4.11.0.86 --quiet
echo -e "${GREEN}✓ OpenCV instalado${NC}"

pip install pillow==11.1.0 --quiet
echo -e "${GREEN}✓ Pillow instalado${NC}"

# Verificar se o modelo existe
echo ""
echo "🔍 Verificando modelo..."
if [ ! -f "modelos baixados/best_model_custom.keras" ]; then
    echo -e "${RED}❌ ERRO: Modelo não encontrado!${NC}"
    echo "   Coloque o arquivo 'best_model_custom.keras' na pasta 'modelos baixados/'"
    exit 1
else
    echo -e "${GREEN}✓ Modelo encontrado${NC}"
fi

# Criar script de execução
echo ""
echo "📝 Criando script de execução..."
cat > start.sh << 'EOF'
#!/bin/bash

# Script para iniciar o OCT Image Analysis

echo "🚀 Iniciando OCT Image Analysis..."
source venv_oct_analysis/bin/activate
python3 run.py
EOF

chmod +x start.sh
echo -e "${GREEN}✓ Script de execução criado${NC}"

# Finalização
echo ""
echo "=========================================="
echo -e "${GREEN}✅ Instalação concluída com sucesso!${NC}"
echo "=========================================="
echo ""
echo "Para iniciar o sistema:"
echo -e "${YELLOW}  ./start.sh${NC}"
echo ""
echo "Ou manualmente:"
echo "  source venv_oct_analysis/bin/activate"
echo "  python3 run.py"
echo ""
echo "Acesse: http://localhost:5000"
echo ""
