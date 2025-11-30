# rag_system.py - Sistema RAG para Green Dream
import json
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re


@dataclass
class DocumentChunk:
    """Representa un fragmento de documento con su metadata"""

    content: str
    metadata: Dict[str, Any]
    source: str
    relevance_score: float = 0.0


class GreenDreamRAG:
    """Sistema RAG especializado para Green Dream ONG"""

    def __init__(self, knowledge_base_path: str = "green_dream_knowledge"):
        knowledge_base_path = os.path.join(
            os.path.dirname(__file__), "..", "knowledge_base"
        )
        self.knowledge_base_path = knowledge_base_path
        self.documents = []
        self.load_knowledge_base()

    def load_knowledge_base(self):
        """Carga toda la base de conocimiento desde archivos JSON"""
        try:
            # Cargar cursos
            cursos_path = os.path.join(self.knowledge_base_path, "cursos.json")
            if os.path.exists(cursos_path):
                with open(cursos_path, "r", encoding="utf-8") as f:
                    cursos = json.load(f)
                    for curso in cursos:
                        self.documents.append(
                            {
                                "content": self._format_curso(curso),
                                "metadata": curso,
                                "type": "curso",
                                "source": f"Curso: {curso['titulo']}",
                            }
                        )

            # Cargar artículos
            articulos_path = os.path.join(self.knowledge_base_path, "articulos.json")
            if os.path.exists(articulos_path):
                with open(articulos_path, "r", encoding="utf-8") as f:
                    articulos = json.load(f)
                    for articulo in articulos:
                        self.documents.append(
                            {
                                "content": self._format_articulo(articulo),
                                "metadata": articulo,
                                "type": "articulo",
                                "source": f"Artículo: {articulo['titulo']}",
                            }
                        )

            # Cargar revistas
            revistas_path = os.path.join(self.knowledge_base_path, "revistas.json")
            if os.path.exists(revistas_path):
                with open(revistas_path, "r", encoding="utf-8") as f:
                    revistas = json.load(f)
                    for revista in revistas:
                        self.documents.append(
                            {
                                "content": self._format_revista(revista),
                                "metadata": revista,
                                "type": "revista",
                                "source": f"Revista: {revista['titulo']}",
                            }
                        )

            print(f"✅ Base de conocimiento cargada: {len(self.documents)} documentos")

        except Exception as e:
            print(f"❌ Error cargando base de conocimiento: {e}")

    def _format_curso(self, curso: Dict) -> str:
        """Formatea un curso para búsqueda"""
        content = f"""
        CURSO: {curso['titulo']}
        Categoría: {curso['categoria']}
        Nivel: {curso['nivel']}
        Modalidad: {curso['modalidad']}
        Duración: {curso['duracion']}
        Edad objetivo: {curso['edad_objetivo']}
        Precio: {curso['precio']}

        DESCRIPCIÓN: {curso['descripcion']}

        OBJETIVOS:
        {' '.join([f'- {obj}' for obj in curso['objetivos']])}

        CONTENIDO:
        {' '.join([f'- {cont}' for cont in curso['contenido']])}

        TAGS: {', '.join(curso['tags'])}
        """
        return content.strip()

    def _format_articulo(self, articulo: Dict) -> str:
        """Formatea un artículo para búsqueda"""
        content = f"""
        ARTÍCULO: {articulo['titulo']}
        Categoría: {articulo['categoria']}
        Autor: {articulo['autor']}
        Fecha: {articulo['fecha_publicacion']}
        Público objetivo: {articulo['publico_objetivo']}
        Dificultad: {articulo['dificultad']}
        Tiempo de lectura: {articulo['tiempo_lectura']}

        RESUMEN: {articulo['resumen']}

        CONTENIDO: {articulo['contenido']}

        TAGS: {', '.join(articulo['tags'])}
        """
        return content.strip()

    def _format_revista(self, revista: Dict) -> str:
        """Formatea una revista para búsqueda"""
        contenido_destacado = " ".join(
            [f"- {item}" for item in revista["contenido_destacado"]]
        )
        content = f"""
        REVISTA: {revista['titulo']}
        Categoría: {revista['categoria']}
        Número: {revista['numero']}
        Fecha: {revista['fecha_publicacion']}
        Editor: {revista['editor']}
        Páginas: {revista['paginas']}
        Precio: {revista['precio']}

        RESUMEN: {revista['resumen']}

        CONTENIDO DESTACADO:
        {contenido_destacado}

        TEMAS PRINCIPALES: {', '.join(revista['temas_principales'])}
        """
        return content.strip()

    def search_simple(self, query: str, max_results: int = 3) -> List[DocumentChunk]:
        """Búsqueda simple basada en palabras clave (versión básica)"""
        query_lower = query.lower()
        query_words = re.findall(r"\w+", query_lower)

        results = []

        for doc in self.documents:
            content_lower = doc["content"].lower()
            score = 0

            # Calcular relevancia basada en coincidencias de palabras
            for word in query_words:
                if len(word) > 2:  # Ignorar palabras muy cortas
                    count = content_lower.count(word)
                    score += count * len(word)  # Palabras más largas tienen más peso

            if score > 0:
                chunk = DocumentChunk(
                    content=doc["content"],
                    metadata=doc["metadata"],
                    source=doc["source"],
                    relevance_score=score,
                )
                results.append(chunk)

        # Ordenar por relevancia y retornar los mejores
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:max_results]

    def get_recommendations_context(self, query: str) -> str:
        """Genera contexto para el asistente basado en la consulta"""
        # Buscar documentos relevantes
        relevant_docs = self.search_simple(query, max_results=3)

        if not relevant_docs:
            # Si no hay coincidencias por la consulta, devolver un resumen compacto
            # de la base de conocimiento para que el asistente siempre tenga datos
            # sobre Green Dream en lugar de decir que no hay información.
            summary_lines = [
                "🌱 **Resumen breve de la Base de Conocimiento Green Dream:**\n"
            ]
            # Mostrar hasta 5 títulos representativos
            for i, doc in enumerate(self.documents[:5], 1):
                meta = doc.get("metadata", {})
                title = (
                    meta.get("titulo")
                    or meta.get("nombre")
                    or doc.get("source", f"Doc {i}")
                )
                dtype = doc.get("type", "recurso")
                summary_lines.append(f"{i}. {title} ({dtype})\n")

            summary_lines.append(
                "\n💡 Usa esta información para hacer recomendaciones concretas sobre cursos, artículos y revistas de Green Dream."
            )
            return "\n".join(summary_lines)

        context = "🌱 **INFORMACIÓN DE GREEN DREAM DISPONIBLE:**\n\n"

        for i, doc in enumerate(relevant_docs, 1):
            context += f"**{i}. {doc.source}**\n"

            # Extraer información clave según el tipo
            metadata = doc.metadata

            if "titulo" in metadata:
                context += f"📋 **Título:** {metadata['titulo']}\n"

            if "categoria" in metadata:
                context += f"🏷️ **Categoría:** {metadata['categoria']}\n"

            if "nivel" in metadata:
                context += f"📊 **Nivel:** {metadata['nivel']}\n"

            if "modalidad" in metadata:
                context += f"💻 **Modalidad:** {metadata['modalidad']}\n"

            if "precio" in metadata:
                context += f"💰 **Precio:** {metadata['precio']}\n"

            if "url" in metadata:
                context += f"🔗 **URL:** {metadata['url']}\n"

            # Agregar descripción o resumen
            if "descripcion" in metadata:
                context += f"📝 **Descripción:** {metadata['descripcion']}\n"
            elif "resumen" in metadata:
                context += f"📝 **Resumen:** {metadata['resumen']}\n"

            context += "\n" + "-" * 50 + "\n\n"

        context += "\n💡 **INSTRUCCIONES PARA EL ASISTENTE:**\n"
        context += "- Usa esta información para hacer recomendaciones específicas y personalizadas\n"
        context += "- Incluye URLs cuando sean relevantes\n"
        context += "- Menciona precios, modalidades y niveles\n"
        context += "- Adapta las recomendaciones al perfil del joven consultante\n"

        return context
