import re
import uuid
import os
import logging
from typing import List, Dict, Any, Union, Optional
from pdfminer.high_level import extract_text
from docx import Document
from smart_rh.models.analysis import Analysis

logger = logging.getLogger(__name__)

def read_file(file_path: str) -> str:
    """Extrai texto de arquivos PDF ou DOCX baseado na extensão do arquivo"""
    try:
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return extract_text(file_path)
        elif file_ext == '.docx':
            return read_docx(file_path)
        else:
            raise ValueError(f"Formato de arquivo não suportado: {file_ext}")
    except Exception as e:
        logger.error(f"Erro ao ler arquivo {file_path}: {str(e)}")
        raise RuntimeError(f"Não foi possível ler o arquivo: {str(e)}")

def read_docx(file_path: str) -> str:
    """Extrai texto de arquivos DOCX"""
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        logger.error(f"Erro ao ler DOCX: {str(e)}")
        raise RuntimeError(f"Falha ao ler arquivo DOCX: {str(e)}")

def clean_item(item: str) -> str:
    """Limpeza de itens com tratamento de caracteres especiais"""
    if not item:
        return "Não especificado"
        
    # Remove marcadores comuns e espaços extras
    cleaned = re.sub(r"[*\-•→⇒►◆◇○●■□]", "", item).strip()
    # Remove quebras de linha internas
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned if cleaned else "Não especificado"

def extract_sections_from_text(text: str) -> Dict[str, Any]:
    """Tenta extrair seções do currículo usando vários métodos"""
    # Primeiro tentamos o formato estruturado em markdown
    sections = extract_markdown_sections(text)
    
    # Se não encontrarmos seções no formato markdown, tentamos outras abordagens
    if not any(sections.values()):
        sections = extract_common_sections(text)
    
    return sections

def extract_markdown_sections(text: str) -> Dict[str, Any]:
    """Extrai seções de um texto formatado em markdown"""
    patterns = {
        "name": r"(?i)^##\s*Nome\s*(Completo|do\s*Candidato)?\s*$\n(.+?)(?=\n##|\Z)",
        "skills": r"(?i)^##\s*(Habilidades|Competências|Skills)(\s*Técnicas)?\s*$\n((?:.*\n)+?)(?=\n##|\Z)",
        "education": r"(?i)^##\s*(Formação|Educação|Formação\s*Acadêmica)\s*$\n((?:.*\n)+?)(?=\n##|\Z)",
        "languages": r"(?i)^##\s*(Idiomas|Línguas)\s*$\n((?:.*\n)+?)(?=\n##|\Z)",
        "experience": r"(?i)^##\s*(Experiência|Experiências)(\s*Profissional|Profissionais)?\s*$\n((?:.*\n)+?)(?=\n##|\Z)",
    }
    
    sections = {
        "name": None,
        "skills": [],
        "education": [],
        "languages": [],
        "experience": []
    }
    
    for section, pattern in patterns.items():
        try:
            match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
            if match:
                if section == "name":
                    sections[section] = clean_item(match.group(2))
                else:
                    content = match.group(match.lastindex).strip()
                    sections[section] = parse_list_items(content)
        except Exception as e:
            logger.error(f"Erro ao extrair seção {section}: {str(e)}")
    
    return sections

def extract_common_sections(text: str) -> Dict[str, Any]:
    """Tenta extrair seções de um texto não estruturado usando palavras-chave"""
    sections = {
        "name": None,
        "skills": [],
        "education": [],
        "languages": [],
        "experience": []
    }
    
    # Tentativa de extrair o nome (geralmente está no início)
    name_match = re.search(r"^(.{2,60})$", text.split('\n')[0], re.MULTILINE)
    if name_match:
        sections["name"] = clean_item(name_match.group(1))
    
    # Keywords para identificar seções
    keywords = {
        "skills": [r"(?i)(habilidades|competências|skills|conhecimentos)(\s*técnicas)?:?\s*\n",
                  r"(?i)(tecnologias|ferramentas|frameworks|languages|linguagens)(\s*utilizadas)?:?\s*\n"],
        "education": [r"(?i)(formação|educação|academic)(\s*acadêmica)?:?\s*\n",
                     r"(?i)(graduação|curso superior|diploma|degree):?\s*\n"],
        "languages": [r"(?i)(idiomas|línguas|languages):?\s*\n"],
        "experience": [r"(?i)(experiência|experiências)(\s*profissional|profissionais)?:?\s*\n",
                      r"(?i)(histórico profissional|career history):?\s*\n"]
    }
    
    for section, patterns in keywords.items():
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
            if match:
                # Extrai o conteúdo após o cabeçalho até o próximo cabeçalho
                start = match.end()
                next_header = re.search(r"(?i)^[a-z\s]+:?\s*\n", text[start:], re.MULTILINE)
                end = start + next_header.start() if next_header else len(text)
                
                content = text[start:end].strip()
                sections[section] = parse_list_items(content)
                break
    
    return sections

def parse_list_items(content: str) -> List[str]:
    """Parseia itens de uma lista, seja com marcadores ou não"""
    if not content:
        return []
    
    # Tenta identificar itens marcados (com -, *, •, etc)
    items = re.findall(r"^[*\-•→⇒►◆◇○●■□]\s*(.+)$", content, re.MULTILINE)
    
    # Se não encontrou itens marcados, quebra por linhas não vazias
    if not items:
        items = [line.strip() for line in content.split('\n') if line.strip()]
    
    # Limpa cada item
    return [clean_item(item) for item in items if clean_item(item) != "Não especificado"]

def extract_data_analysis(
    resume_cv: str, job_id: str, resume_id: str, score: float
) -> Analysis:
    """Extrai dados estruturados do texto do currículo com fallbacks seguros"""
    
    # Tenta extrair dados do currículo formatado
    sections = extract_sections_from_text(resume_cv)
    
    # Constrói o modelo de dados com valores padrão seguros
    analysis_data = {
        "id": str(uuid.uuid4()),
        "job_id": job_id,
        "resum_id": resume_id,
        "name": sections.get("name") or "Não identificado",
        "skills": sections.get("skills") or ["Habilidades não especificadas"],
        "education": sections.get("education") or ["Formação não especificada"],
        "languages": sections.get("languages") or ["Idiomas não especificados"],
        "score": score,
    }
    
    # Validação final dos dados
    validation_rules = {
        "name": lambda x: isinstance(x, str) and len(x) >= 2,
        "skills": lambda x: isinstance(x, list) and len(x) > 0,
        "education": lambda x: isinstance(x, list) and len(x) > 0,
        "languages": lambda x: isinstance(x, list) and len(x) > 0,
    }
    
    for field, validator in validation_rules.items():
        if not validator(analysis_data.get(field)):
            if field == "name":
                analysis_data[field] = "Não identificado"
            else:
                analysis_data[field] = [f"{field.title()} não especificados"]
    
    # Limita o tamanho de cada lista para evitar dados excessivos
    for field in ["skills", "education", "languages"]:
        analysis_data[field] = analysis_data[field][:10]  # Limita a 10 itens por seção
    
    return Analysis(**analysis_data)

def clean_analysis_data(data: dict) -> dict:
    """Remove duplicatas e normaliza dados"""
    # Unifica nomenclaturas diferentes para o mesmo conceito
    if "Formação Acadêmica" in data and "Educação" in data:
        data["education"] = data.pop("Formação Acadêmica") + data.pop("Educação")
    
    if "Habilidades" in data and "Skills" in data:
        data["skills"] = data.pop("Habilidades") + data.pop("Skills")
    
    # Remove duplicatas e normaliza dados
    for key in ["skills", "education", "languages"]:
        if key in data and isinstance(data[key], list):
            # Normaliza (lowercase) antes de remover duplicatas
            normalized = [item.lower() for item in data[key]]
            unique_indices = []
            seen = set()
            
            for i, item in enumerate(normalized):
                if item not in seen:
                    seen.add(item)
                    unique_indices.append(i)
            
            # Usa os índices únicos para manter os itens originais (não normalizados)
            data[key] = [data[key][i] for i in unique_indices]
    
    return data