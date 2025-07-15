"""
Módulo para processamento automático de arquivos.

Este módulo contém a lógica para detectar o tipo de um arquivo carregado
e aplicar a função de processamento mais adequada, como extração de texto,
OCR, transcrição de áudio ou análise de dados.
"""
import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import io
from docx import Document

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
        }
        
        # Processa por tipo MIME
        if arquivo.type in processadores:
            return processadores[arquivo.type](arquivo)
        
        # Processa por extensão se tipo MIME não for reconhecido
        nome_arquivo = arquivo.name.lower()
        if nome_arquivo.endswith('.pdf'):
            return extrair_texto_pdf(arquivo)
        elif nome_arquivo.endswith('.txt'):
            return extrair_texto_txt(arquivo)
        elif nome_arquivo.endswith('.docx'):
            return extrair_texto_docx(arquivo)
        elif nome_arquivo.endswith('.csv'):
            return analisar_csv(arquivo)
        elif nome_arquivo.endswith(('.xls', '.xlsx')):
            return analisar_excel(arquivo)
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