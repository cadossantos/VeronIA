"""
Módulo para processamento automático de arquivos.

Este módulo contém a lógica para detectar o tipo de um arquivo carregado
e aplicar a função de processamento mais adequada, como extração de texto,
OCR, transcrição de áudio, análise de dados ou processamento de código.
"""
import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import io
from docx import Document
import json
import xml.etree.ElementTree as ET
import yaml

def extrair_texto_pdf(arquivo):
    """Extrai texto de um arquivo PDF."""
    try:
        # Lê o conteúdo do arquivo
        conteudo = arquivo.read()
        doc = fitz.open(stream=conteudo, filetype="pdf")
        texto = ""
        
        for num_pagina, pagina in enumerate(doc, 1):
            texto_pagina = pagina.get_text()
            if texto_pagina.strip():  # Só adiciona se há texto
                texto += f"--- Página {num_pagina} ---\n"
                texto += texto_pagina + "\n\n"
        
        doc.close()
        
        if not texto.strip():
            return "PDF processado, mas nenhum texto foi encontrado. Pode ser um PDF de imagens."
        
        return texto
    except Exception as e:
        st.error(f"Erro ao processar PDF '{arquivo.name}': {e}")
        return None

def extrair_texto_txt(arquivo):
    """Extrai texto de um arquivo TXT."""
    try:
        # Tenta diferentes encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        conteudo = arquivo.read()
        
        for encoding in encodings:
            try:
                return conteudo.decode(encoding)
            except UnicodeDecodeError:
                continue
        
        # Se nenhum encoding funcionar, usa utf-8 com ignore
        return conteudo.decode('utf-8', errors='ignore')
    except Exception as e:
        st.error(f"Erro ao ler arquivo de texto '{arquivo.name}': {e}")
        return None

def processar_codigo_python(arquivo):
    """Processa arquivo Python e retorna informações estruturadas."""
    try:
        conteudo = extrair_texto_txt(arquivo)
        if conteudo is None:
            return None
        
        # Análise básica do código Python
        info = f"ANÁLISE DO CÓDIGO PYTHON: {arquivo.name}\n"
        info += f"Tamanho: {len(conteudo)} caracteres\n"
        info += f"Linhas: {len(conteudo.splitlines())}\n\n"
        
        # Conta imports, funções e classes
        linhas = conteudo.splitlines()
        imports = [linha for linha in linhas if linha.strip().startswith(('import ', 'from '))]
        funcoes = [linha for linha in linhas if linha.strip().startswith('def ')]
        classes = [linha for linha in linhas if linha.strip().startswith('class ')]
        
        if imports:
            info += f"IMPORTS ({len(imports)}):\n"
            for imp in imports[:10]:  # Máximo 10 imports
                info += f"  {imp.strip()}\n"
            if len(imports) > 10:
                info += f"  ... e mais {len(imports) - 10} imports\n"
            info += "\n"
        
        if classes:
            info += f"CLASSES ({len(classes)}):\n"
            for classe in classes:
                info += f"  {classe.strip()}\n"
            info += "\n"
        
        if funcoes:
            info += f"FUNÇÕES ({len(funcoes)}):\n"
            for funcao in funcoes:
                info += f"  {funcao.strip()}\n"
            info += "\n"
        
        info += "CÓDIGO COMPLETO:\n"
        info += "=" * 50 + "\n"
        info += conteudo
        
        return info
    except Exception as e:
        st.error(f"Erro ao processar código Python '{arquivo.name}': {e}")
        return None

def processar_codigo_javascript(arquivo):
    """Processa arquivo JavaScript e retorna informações estruturadas."""
    try:
        conteudo = extrair_texto_txt(arquivo)
        if conteudo is None:
            return None
        
        info = f"ANÁLISE DO CÓDIGO JAVASCRIPT: {arquivo.name}\n"
        info += f"Tamanho: {len(conteudo)} caracteres\n"
        info += f"Linhas: {len(conteudo.splitlines())}\n\n"
        
        # Análise básica
        linhas = conteudo.splitlines()
        funcoes = [linha for linha in linhas if 'function' in linha or '=>' in linha]
        imports = [linha for linha in linhas if linha.strip().startswith(('import ', 'const ', 'require('))]
        
        if imports:
            info += f"IMPORTS/REQUIRES ({len(imports)}):\n"
            for imp in imports[:10]:
                info += f"  {imp.strip()}\n"
            if len(imports) > 10:
                info += f"  ... e mais {len(imports) - 10} imports\n"
            info += "\n"
        
        if funcoes:
            info += f"FUNÇÕES ({len(funcoes)}):\n"
            for funcao in funcoes[:10]:
                info += f"  {funcao.strip()}\n"
            if len(funcoes) > 10:
                info += f"  ... e mais {len(funcoes) - 10} funções\n"
            info += "\n"
        
        info += "CÓDIGO COMPLETO:\n"
        info += "=" * 50 + "\n"
        info += conteudo
        
        return info
    except Exception as e:
        st.error(f"Erro ao processar código JavaScript '{arquivo.name}': {e}")
        return None

def processar_html(arquivo):
    """Processa arquivo HTML e retorna informações estruturadas."""
    try:
        conteudo = extrair_texto_txt(arquivo)
        if conteudo is None:
            return None
        
        info = f"ANÁLISE DO HTML: {arquivo.name}\n"
        info += f"Tamanho: {len(conteudo)} caracteres\n"
        info += f"Linhas: {len(conteudo.splitlines())}\n\n"
        
        # Análise básica de tags
        import re
        tags = re.findall(r'<(\w+)', conteudo.lower())
        tags_unicas = list(set(tags))
        
        if tags_unicas:
            info += f"TAGS HTML ENCONTRADAS ({len(tags_unicas)}):\n"
            for tag in sorted(tags_unicas):
                count = tags.count(tag)
                info += f"  <{tag}> ({count}x)\n"
            info += "\n"
        
        # Procura por scripts e estilos
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', conteudo, re.DOTALL | re.IGNORECASE)
        styles = re.findall(r'<style[^>]*>(.*?)</style>', conteudo, re.DOTALL | re.IGNORECASE)
        
        if scripts:
            info += f"SCRIPTS ENCONTRADOS ({len(scripts)}):\n"
            for i, script in enumerate(scripts[:3], 1):
                info += f"  Script {i}: {len(script)} caracteres\n"
            info += "\n"
        
        if styles:
            info += f"ESTILOS ENCONTRADOS ({len(styles)}):\n"
            for i, style in enumerate(styles[:3], 1):
                info += f"  Style {i}: {len(style)} caracteres\n"
            info += "\n"
        
        info += "CÓDIGO COMPLETO:\n"
        info += "=" * 50 + "\n"
        info += conteudo
        
        return info
    except Exception as e:
        st.error(f"Erro ao processar HTML '{arquivo.name}': {e}")
        return None

def processar_css(arquivo):
    """Processa arquivo CSS e retorna informações estruturadas."""
    try:
        conteudo = extrair_texto_txt(arquivo)
        if conteudo is None:
            return None
        
        info = f"ANÁLISE DO CSS: {arquivo.name}\n"
        info += f"Tamanho: {len(conteudo)} caracteres\n"
        info += f"Linhas: {len(conteudo.splitlines())}\n\n"
        
        # Análise básica de seletores
        import re
        seletores = re.findall(r'([^{]+){', conteudo)
        seletores_limpos = [s.strip() for s in seletores if s.strip()]
        
        if seletores_limpos:
            info += f"SELETORES CSS ({len(seletores_limpos)}):\n"
            for seletor in seletores_limpos[:20]:  # Máximo 20 seletores
                info += f"  {seletor}\n"
            if len(seletores_limpos) > 20:
                info += f"  ... e mais {len(seletores_limpos) - 20} seletores\n"
            info += "\n"
        
        # Procura por media queries
        media_queries = re.findall(r'@media[^{]+', conteudo)
        if media_queries:
            info += f"MEDIA QUERIES ({len(media_queries)}):\n"
            for mq in media_queries:
                info += f"  {mq.strip()}\n"
            info += "\n"
        
        info += "CÓDIGO COMPLETO:\n"
        info += "=" * 50 + "\n"
        info += conteudo
        
        return info
    except Exception as e:
        st.error(f"Erro ao processar CSS '{arquivo.name}': {e}")
        return None

def processar_json(arquivo):
    """Processa arquivo JSON e retorna informações estruturadas."""
    try:
        conteudo = extrair_texto_txt(arquivo)
        if conteudo is None:
            return None
        
        # Tenta parsear o JSON
        try:
            dados = json.loads(conteudo)
            info = f"ANÁLISE DO JSON: {arquivo.name}\n"
            info += f"Tamanho: {len(conteudo)} caracteres\n"
            info += f"Válido: SIM\n"
            info += f"Tipo raiz: {type(dados).__name__}\n"
            
            if isinstance(dados, dict):
                info += f"Chaves principais: {list(dados.keys())}\n"
            elif isinstance(dados, list):
                info += f"Elementos na lista: {len(dados)}\n"
            
            info += "\nCONTEÚDO JSON:\n"
            info += "=" * 50 + "\n"
            info += json.dumps(dados, indent=2, ensure_ascii=False)
            
            return info
        except json.JSONDecodeError as e:
            info = f"ANÁLISE DO JSON: {arquivo.name}\n"
            info += f"Tamanho: {len(conteudo)} caracteres\n"
            info += f"Válido: NÃO - Erro: {e}\n\n"
            info += "CONTEÚDO BRUTO:\n"
            info += "=" * 50 + "\n"
            info += conteudo
            return info
    except Exception as e:
        st.error(f"Erro ao processar JSON '{arquivo.name}': {e}")
        return None

def processar_xml(arquivo):
    """Processa arquivo XML e retorna informações estruturadas."""
    try:
        conteudo = extrair_texto_txt(arquivo)
        if conteudo is None:
            return None
        
        info = f"ANÁLISE DO XML: {arquivo.name}\n"
        info += f"Tamanho: {len(conteudo)} caracteres\n"
        
        try:
            root = ET.fromstring(conteudo)
            info += f"Válido: SIM\n"
            info += f"Elemento raiz: {root.tag}\n"
            
            # Lista elementos filhos
            children = list(root)
            if children:
                info += f"Elementos filhos: {[child.tag for child in children]}\n"
            
            info += "\nCONTEÚDO XML:\n"
            info += "=" * 50 + "\n"
            info += conteudo
            
            return info
        except ET.ParseError as e:
            info += f"Válido: NÃO - Erro: {e}\n\n"
            info += "CONTEÚDO BRUTO:\n"
            info += "=" * 50 + "\n"
            info += conteudo
            return info
    except Exception as e:
        st.error(f"Erro ao processar XML '{arquivo.name}': {e}")
        return None

def processar_codigo_generico(arquivo):
    """Processa arquivos de código genéricos (extensões não específicas)."""
    try:
        conteudo = extrair_texto_txt(arquivo)
        if conteudo is None:
            return None
        
        extensao = arquivo.name.split('.')[-1].upper()
        
        info = f"ANÁLISE DE CÓDIGO ({extensao}): {arquivo.name}\n"
        info += f"Tamanho: {len(conteudo)} caracteres\n"
        info += f"Linhas: {len(conteudo.splitlines())}\n\n"
        
        # Análise básica
        linhas = conteudo.splitlines()
        linhas_codigo = [linha for linha in linhas if linha.strip() and not linha.strip().startswith('#')]
        comentarios = [linha for linha in linhas if linha.strip().startswith('#')]
        
        info += f"Linhas de código (não comentário): {len(linhas_codigo)}\n"
        info += f"Linhas de comentário: {len(comentarios)}\n\n"
        
        info += "CÓDIGO COMPLETO:\n"
        info += "=" * 50 + "\n"
        info += conteudo
        
        return info
    except Exception as e:
        st.error(f"Erro ao processar código '{arquivo.name}': {e}")
        return None

def extrair_texto_docx(arquivo):
    """Extrai texto de um arquivo DOCX."""
    try:
        doc = Document(arquivo)
        texto = ""
        
        for num_paragrafo, paragrafo in enumerate(doc.paragraphs, 1):
            if paragrafo.text.strip():
                texto += f"{paragrafo.text}\n"
        
        if not texto.strip():
            return "Documento DOCX processado, mas nenhum texto foi encontrado."
        
        return texto
    except Exception as e:
        st.error(f"Erro ao processar DOCX '{arquivo.name}': {e}")
        return None

def analisar_csv(arquivo):
    """Analisa um arquivo CSV e retorna informações estruturadas."""
    try:
        # Lê o CSV
        df = pd.read_csv(arquivo)
        
        # Informações básicas
        info = f"ANÁLISE DO CSV: {arquivo.name}\n"
        info += f"Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas\n\n"
        
        # Colunas
        info += "COLUNAS:\n"
        for col in df.columns:
            info += f"- {col}\n"
        
        # Primeiras linhas
        info += f"\nPRIMEIRAS 5 LINHAS:\n"
        info += df.head().to_string()
        
        # Informações estatísticas básicas para colunas numéricas
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            info += f"\n\nESTATÍSTICAS (colunas numéricas):\n"
            info += df[numeric_cols].describe().to_string()
        
        return info
    except Exception as e:
        st.error(f"Erro ao analisar CSV '{arquivo.name}': {e}")
        return None

def analisar_excel(arquivo):
    """Analisa um arquivo Excel e retorna informações estruturadas."""
    try:
        # Lê o Excel
        df = pd.read_excel(arquivo)
        
        # Informações básicas
        info = f"ANÁLISE DO EXCEL: {arquivo.name}\n"
        info += f"Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas\n\n"
        
        # Colunas
        info += "COLUNAS:\n"
        for col in df.columns:
            info += f"- {col}\n"
        
        # Primeiras linhas
        info += f"\nPRIMEIRAS 5 LINHAS:\n"
        info += df.head().to_string()
        
        # Informações estatísticas básicas para colunas numéricas
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            info += f"\n\nESTATÍSTICAS (colunas numéricas):\n"
            info += df[numeric_cols].describe().to_string()
        
        return info
    except Exception as e:
        st.error(f"Erro ao analisar Excel '{arquivo.name}': {e}")
        return None

def aplicar_ocr(arquivo):
    """Placeholder para aplicação de OCR em imagem."""
    st.info(f"OCR seria aplicado na imagem '{arquivo.name}' aqui.")
    return f"[OCR] Imagem {arquivo.name} foi carregada. Funcionalidade de OCR não implementada ainda."

def transcrever_audio(arquivo):
    """Placeholder para transcrição de áudio."""
    st.info(f"Áudio '{arquivo.name}' seria transcrito aqui.")
    return f"[ÁUDIO] Arquivo {arquivo.name} foi carregado. Funcionalidade de transcrição não implementada ainda."

def processar_automatico(arquivo):
    """
    Detecta o tipo do arquivo e aplica o processamento adequado.
    Retorna o resultado do processamento.
    """
    try:
        # Mapeia tipos de arquivo para funções de processamento
        processadores = {
            "application/pdf": extrair_texto_pdf,
            "text/plain": extrair_texto_txt,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": extrair_texto_docx,
            "text/csv": analisar_csv,
            "application/vnd.ms-excel": analisar_excel,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": analisar_excel,
            "application/json": processar_json,
            "text/html": processar_html,
            "text/css": processar_css,
            "application/javascript": processar_codigo_javascript,
            "text/javascript": processar_codigo_javascript,
            "application/xml": processar_xml,
            "text/xml": processar_xml,
        }
        
        # Processa por tipo MIME
        if arquivo.type in processadores:
            return processadores[arquivo.type](arquivo)
        
        # Processa por extensão se tipo MIME não for reconhecido
        nome_arquivo = arquivo.name.lower()
        
        # Arquivos de código
        if nome_arquivo.endswith('.py'):
            return processar_codigo_python(arquivo)
        elif nome_arquivo.endswith(('.js', '.jsx')):
            return processar_codigo_javascript(arquivo)
        elif nome_arquivo.endswith('.html'):
            return processar_html(arquivo)
        elif nome_arquivo.endswith('.css'):
            return processar_css(arquivo)
        elif nome_arquivo.endswith('.json'):
            return processar_json(arquivo)
        elif nome_arquivo.endswith(('.xml', '.svg')):
            return processar_xml(arquivo)
        elif nome_arquivo.endswith(('.yaml', '.yml')):
            return processar_codigo_generico(arquivo)
        elif nome_arquivo.endswith(('.php', '.rb', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.go', '.rs', '.swift', '.kt', '.scala', '.r', '.m', '.sh', '.bat', '.ps1')):
            return processar_codigo_generico(arquivo)
        # Arquivos de configuração
        elif nome_arquivo.endswith(('.conf', '.config', '.ini', '.cfg', '.properties', '.env')):
            return processar_codigo_generico(arquivo)
        # Arquivos de documentação
        elif nome_arquivo.endswith(('.md', '.markdown', '.rst', '.txt')):
            return extrair_texto_txt(arquivo)
        # Arquivos de dados
        elif nome_arquivo.endswith('.pdf'):
            return extrair_texto_pdf(arquivo)
        elif nome_arquivo.endswith('.docx'):
            return extrair_texto_docx(arquivo)
        elif nome_arquivo.endswith('.csv'):
            return analisar_csv(arquivo)
        elif nome_arquivo.endswith(('.xls', '.xlsx')):
            return analisar_excel(arquivo)
        # Arquivos de mídia
        elif nome_arquivo.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            return aplicar_ocr(arquivo)
        elif nome_arquivo.endswith(('.mp3', '.wav', '.m4a', '.flac')):
            return transcrever_audio(arquivo)
        else:
            st.warning(f"Tipo de arquivo '{arquivo.type}' ({arquivo.name}) não suportado para processamento automático.")
            return f"[ARQUIVO NÃO SUPORTADO] {arquivo.name} - Tipo: {arquivo.type}"
    
    except Exception as e:
        st.error(f"Erro geral ao processar arquivo '{arquivo.name}': {e}")
        return None

def obter_tipos_suportados():
    """Retorna lista dos tipos de arquivo suportados."""
    return {
        'Documentos': ['.pdf', '.docx', '.txt', '.md', '.rst'],
        'Planilhas': ['.csv', '.xls', '.xlsx'],
        'Código': ['.py', '.js', '.jsx', '.html', '.css', '.php', '.rb', '.java', '.c', '.cpp', '.cs', '.go', '.rs', '.swift', '.kt', '.scala'],
        'Dados': ['.json', '.xml', '.yaml', '.yml'],
        'Configuração': ['.conf', '.config', '.ini', '.cfg', '.properties', '.env'],
        'Imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'Áudio': ['.mp3', '.wav', '.m4a', '.flac']
    }