# assistant_rag.py - Asistente con RAG integrado para Green Dream
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from chat_client import client
from rag_system import GreenDreamRAG


class AsistenteGreenDreamRAG:
    def __init__(self):
        # Sistema prompt especializado para Green Dream (más explícito)
        # Nota: este prompt fuerza al modelo a afirmar que conoce la base de Green Dream
        # y dar recomendaciones aunque no haya coincidencias exactas en el contexto RAG.
        self.system_prompt = (
            "Eres el asistente oficial de Green Dream — una ONG que promueve\n"
            "el desarrollo sostenible. Tu identidad y rol son claros: actúas como\n"
            "representante del proyecto, conoces la base de recursos de Green Dream\n"
            "(cursos, artículos y revistas) y debes usar esa información siempre que\n"
            "sea relevante.\n\n"
            "Reglas de comportamiento (obligatorias):\n"
            "1) Afirma que conoces recursos de Green Dream y que puedes ayudar.\n"
            "2) Si el contexto RAG contiene documentos relevantes, cítalos y proporciona\n"
            "   enlaces y detalles concretos.\n"
            "3) Si no hay documentos exactos en el contexto RAG, no digas \"no tengo\n"
            "   información\". En su lugar, ofrece recomendaciones plausibles, basadas\n"
            "   en la misión y recursos típicos de una ONG de sostenibilidad, y sugiere\n"
            "   cómo obtener información específica (por ejemplo, solicitar más\n"
            "   detalles para buscar en la base o pedir al usuario que consulte la web).\n"
            "4) Siempre muestra tono amable, práctico y orientado a la acción. Incluye\n"
            "   enlaces cuando los tengas y pasos concretos para seguir.\n\n"
            "Objetivos:\n"
            "- Recomendar cursos, artículos y revistas de Green Dream.\n"
            "- Adaptar las recomendaciones según perfil, intereses y nivel.\n"
            "- Proponer próximos pasos (inscribirse, contactar, voluntariado) cuando aplique.\n"
        )

        # Inicializa el historial con el mensaje del sistema y un saludo del asistente
        self.messages = [SystemMessage(content=self.system_prompt)]

        # Mensaje inicial del asistente: muestra confianza en la base de Green Dream
        greeting = (
            "¡Hola! 🌟 Soy el asistente virtual de Green Dream. "
            "Conozco nuestra base de recursos (cursos, artículos y revistas) y estoy aquí para ayudarte a encontrar formación, proyectos y formas de colaborar. "
            "Antes de recomendarte cursos, cuéntame: ¿sobre qué tema o tipo de curso te gustaría aprender? (por ejemplo: energía renovable, economía circular, reciclaje doméstico, agricultura urbana, etc.)"
        )
        self.messages.append(AssistantMessage(content=greeting))
        # Log útil para desarrollo: ver el saludo inicial en los logs del servidor
        print("🌱 Saludo inicial del asistente:", greeting)
        self.rag_system = GreenDreamRAG()

    def preguntar_con_rag(
        self,
        pregunta: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False,
        model: str = "gpt-4o",
    ):
        """
        Pregunta al modelo usando RAG para obtener información contextual específica de Green Dream
        Args:
            pregunta (str): La pregunta del usuario
            temperature (float): Parametro que controla la creatividad de la respuesta
            max_tokens (int): Número máximo de tokens en la respuesta
            stream (bool): Si se debe usar streaming para la respuesta (Streaming significa que la respuesta se muestra en tiempo real a medida que se genera)
            model (str): El modelo de lenguaje a utilizar
        """
        # 1. Obtener contexto relevante de la base de conocimiento
        contexto_rag = self.rag_system.get_recommendations_context(pregunta)

        # 1.a Añadir resumen de lo que contiene la base de conocimiento para que el
        # modelo sepa cuántos recursos hay y de qué tipo (esto ayuda cuando el
        # contexto RAG está vacío o es corto).
        try:
            total_docs = len(self.rag_system.documents)
            cursos = len([d for d in self.rag_system.documents if d.get("type") == "curso"]) if total_docs else 0
            articulos = len([d for d in self.rag_system.documents if d.get("type") == "articulo"]) if total_docs else 0
            revistas = len([d for d in self.rag_system.documents if d.get("type") == "revista"]) if total_docs else 0
            resumen_base = (
                f"BASE_DE_CONOCIMIENTO: total={total_docs}; cursos={cursos}; articulos={articulos}; revistas={revistas}."
            )
        except Exception:
            resumen_base = "BASE_DE_CONOCIMIENTO: información de recursos no disponible." 

        # 2. Construir prompt enriquecido con contexto y el resumen
        prompt_enriquecido = f"""
        {contexto_rag}

        {resumen_base}

        CONSULTA DEL JOVEN: {pregunta}

        Por favor, proporciona una respuesta personalizada usando la información específica de Green Dream mostrada arriba. Si no hay coincidencias exactas en la base, ofrece recomendaciones prácticas y pasos siguientes en lugar de indicar que no tienes información.
        """

        # 3. Construir mensajes para la petición
        user_msg = UserMessage(content=prompt_enriquecido)
        messages_for_request = list(self.messages) + [
            user_msg
        ]  # Crea una lista con el mensaje de rol sistema y rol usuario

        if stream:
            return self._process_streaming(
                messages_for_request, user_msg, temperature, max_tokens, model
            )
        else:
            return self._process_non_streaming(
                messages_for_request, user_msg, temperature, max_tokens, model
            )

    def _process_streaming(
        self, messages_for_request, user_msg, temperature, max_tokens, model
    ):
        """Procesa respuesta con streaming"""
        respuesta = ""
        try:
            stream_iter = client.complete(
                model=model,
                messages=messages_for_request,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            print("🌱 ", end="", flush=True)
            for event in stream_iter:
                if (
                    hasattr(event, "choices") and event.choices
                ):  # hasattr verifica que choices existe y no es None
                    choice = event.choices[0]
                    if hasattr(choice, "delta") and choice.delta:
                        if hasattr(choice.delta, "content") and choice.delta.content:
                            fragment = choice.delta.content
                            print(fragment, end="", flush=True)
                            respuesta += fragment
            print()
        except Exception as e:
            print(f"\n❌ Error en streaming: {e}")
            raise

        # Guardar en historial (solo la pregunta original, no el contexto RAG)
        original_user_msg = UserMessage(
            content=(
                user_msg.content.split("CONSULTA DEL JOVEN: ")[1]
                if "CONSULTA DEL JOVEN: " in user_msg.content
                else user_msg.content
            )
        )
        self.messages.append(
            original_user_msg
        )  # Guarda solo mensaje del usuario original
        self.messages.append(
            AssistantMessage(content=respuesta)
        )  # Guarda respuesta del asistente

        return respuesta

    def _process_non_streaming(
        self, messages_for_request, user_msg, temperature, max_tokens, model
    ):
        """Procesa respuesta sin streaming"""
        response = client.complete(
            model=model,
            messages=messages_for_request,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        assistant_content = response.choices[0].message.content

        # Guardar en historial (solo la pregunta original, no el contexto RAG)
        original_user_msg = UserMessage(
            content=(
                user_msg.content.split("CONSULTA DEL JOVEN: ")[1]
                if "CONSULTA DEL JOVEN: " in user_msg.content
                else user_msg.content
            )
        )
        self.messages.append(original_user_msg)
        self.messages.append(AssistantMessage(content=assistant_content))

        print("🌱", assistant_content)
        return assistant_content

    def _format_search_results(self, results, tipo):
        """Formatea los resultados de búsqueda"""
        if not results:
            return f"No se encontraron {tipo} en la base de conocimiento."

        formatted = f"🔍 **{tipo.upper()} ENCONTRADOS:**\n\n"

        for i, result in enumerate(results, 1):
            metadata = result.metadata
            formatted += f"**{i}. {metadata.get('titulo', 'Sin título')}**\n"

            if "categoria" in metadata:
                formatted += f"   🏷️ Categoría: {metadata['categoria']}\n"
            if "nivel" in metadata:
                formatted += f"   📊 Nivel: {metadata['nivel']}\n"
            if "modalidad" in metadata:
                formatted += f"   💻 Modalidad: {metadata['modalidad']}\n"
            if "precio" in metadata:
                formatted += f"   💰 Precio: {metadata['precio']}\n"
            if "url" in metadata:
                formatted += f"   🔗 URL: {metadata['url']}\n"

            formatted += f"   📝 {metadata.get('descripcion', metadata.get('resumen', 'Sin descripción'))}\n\n"

        return formatted

    def limpiar_historial(self):
        """Limpia el historial manteniendo solo el mensaje del sistema"""
        self.messages = [self.messages[0]]
        print("✅ Historial limpiado")

    def ver_historial(self):
        """Muestra el historial de conversación"""
        print("\n📝 **HISTORIAL DE CONVERSACIÓN GREEN DREAM:**")
        print("=" * 50)

    def pop_initial_greeting(self):
        """Devuelve y elimina el saludo inicial del asistente (si existe).

        Esto permite que la API entregue el saludo una sola vez al frontend al
        iniciar la conversación.
        """
        for i, mensaje in enumerate(self.messages):
            # comprobamos por tipo AssistantMessage importado arriba
            try:
                from azure.ai.inference.models import AssistantMessage as _AM
            except Exception:
                _AM = None

            if _AM is not None and isinstance(mensaje, _AM):
                saludo = getattr(mensaje, "content", None)
                # eliminar del historial para que no se vuelva a enviar
                self.messages.pop(i)
                return saludo

        return None
        for i, mensaje in enumerate(self.messages):
            tipo = type(mensaje).__name__
            contenido = getattr(mensaje, "content", "")

            if tipo == "SystemMessage":
                print(f"🌱 **Green Dream Sistema:** {contenido[:100]}...")
            elif tipo == "UserMessage":
                print(f"👤 **Joven:** {contenido}")
            elif tipo == "AssistantMessage":
                print(f"🌱 **Green Dream:** {contenido}")

            if i < len(self.messages) - 1:
                print("-" * 30)
        print("=" * 50)

    def estadisticas_conocimiento(self):
        """Muestra estadísticas de la base de conocimiento"""
        total_docs = len(self.rag_system.documents)
        cursos = len([d for d in self.rag_system.documents if d["type"] == "curso"])
        articulos = len(
            [d for d in self.rag_system.documents if d["type"] == "articulo"]
        )
        revistas = len([d for d in self.rag_system.documents if d["type"] == "revista"])

        print("📊 **ESTADÍSTICAS BASE DE CONOCIMIENTO GREEN DREAM:**")
        print("=" * 50)
        print(f"📚 Total de recursos: {total_docs}")
        print(f"🎓 Cursos disponibles: {cursos}")
        print(f"📰 Artículos: {articulos}")
        print(f"📖 Revistas: {revistas}")
        print("=" * 50)
