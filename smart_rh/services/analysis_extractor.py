import re
import uuid
import os
import logging
from typing import List
from pdfminer.high_level import extract_text
from docx import Document
from models.analysis import Analysis

logger = logging.getLogger(__name__)


def read_uploaded_file(file_path: str) -> str:
    """Extrai texto de arquivos PDF usando pdfminer"""
    try:
        return extract_text(file_path)
    except Exception as e:
        logger.error(f"Erro ao ler arquivo {file_path}: {str(e)}")
        raise RuntimeError(f"Não foi possível ler o arquivo PDF: {str(e)}")


def clean_item(item: str) -> str:
    """Limpeza mais tolerante"""
    cleaned = re.sub(r"[*\-•]", "", item).strip()
    return cleaned if cleaned else "Não especificado"


def extract_data_analysis(
    resum_cv: str, job_id: str, resum_id: str, score: float
) -> Analysis:
    """Extrai dados estruturados do texto do currículo com fallbacks seguros"""

    patterns = {
        "name": r"(?i)^##\s*Nome Completo\s*$\n(.+?)(?=\n##|\Z)",
        "skills": r"(?i)^##\s*Habilidades Técnicas\s*$\n((?:^-\s*.+$\n?)+)",
        "education": r"(?i)^##\s*Formação Acadêmica\s*$\n((?:^-\s*.+$\n?)+)",
        "languages": r"(?i)^##\s*Idiomas\s*$\n((?:^-\s*.+$\n?)+)",
    }

    data = {
        "id": str(uuid.uuid4()),
        "job_id": job_id,
        "resum_id": resum_id,
        "name": "Não identificado",
        "skills": ["Habilidades não especificadas"],
        "education": ["Formação não especificada"],
        "languages": ["Idiomas não especificados"],
        "score": score,
    }

    # Processamento com fallback
    for section, pattern in patterns.items():
        try:
            match = re.search(pattern, resum_cv, re.MULTILINE | re.DOTALL)
            if match:
                content = match.group(1).strip()

                if section == "name":
                    data[section] = clean_item(content)
                else:
                    data[section] = [
                        clean_item(line) for line in content.split("\n") if line.strip()
                    ]

            # Validação dos dados
            validation_rules = {
                "name": (str, lambda x: len(x) >= 3),
                "skills": (list, lambda x: True),
                "education": (list, lambda x: True),
            }

            for field, (dtype, validator) in validation_rules.items():
                value = data.get(field)
                if not isinstance(value, dtype) or not validator(value):
                    raise ValueError(f"Seção inválida ou vazia: {field}")

        except Exception as e:
            logger.error(f"Erro na seção {section}: {str(e)}")

    return Analysis(**data)


def get_pdf_paths(directory: str) -> List[str]:
    """Lista arquivos PDF com validação de diretório"""
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Diretório não encontrado: {directory}")

    if not os.path.isdir(directory):
        raise NotADirectoryError(f"Caminho não é um diretório: {directory}")

    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith(".pdf")
    ]


def read_docx(file_path: str) -> str:
    """Extrai texto de arquivos DOCX"""
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        logger.error(f"Erro ao ler DOCX: {str(e)}")
        raise RuntimeError(f"Falha ao ler arquivo DOCX: {str(e)}")


def clean_analysis_data(data: dict) -> dict:
    """Remove duplicatas e normaliza dados"""
    if "Formação Acadêmica" in data and "Educação" in data:
        data["Formação Acadêmica"].extend(data.pop("Educação"))

    for key in ["skills", "education", "languages"]:
        if key in data:
            data[key] = list(set(data[key]))

    return data
