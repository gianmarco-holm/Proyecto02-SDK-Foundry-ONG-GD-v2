# assistant_rag.py - Asistente con RAG integrado para Green Dream
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from chat_client import client
from rag_system import GreenDreamRAG

class AsistenteGreenDreamRAG:
    def __init__(self):
        # Sistema prompt especializado para Green Dream
        self.system_prompt = """Eres un asistente experto de Green Dream, una ONG dedicada al desarrollo sostenible para jóvenes.

        Tu misión es:
        - Recomendar cursos, artículos y revistas específicos de Green Dream
        - Adaptar las recomendaciones al perfil, intereses y nivel de cada joven
        - Proporcionar información práctica y motivacional
        - Incluir siempre URLs y detalles específicos cuando estén disponibles
        - Fomentar la participación activa en sostenibilidad

        Características de tu personalidad:
        - Entusiasta y motivador
        - Conocedor profundo de Green Dream
        - Orientado a la acción
        - Empático con las necesidades de los jóvenes
        - Siempre propositivo y constructivo

        IMPORTANTE: Siempre usa la información específica de Green Dream que se te proporciona para hacer recomendaciones precisas y personalizadas.
        """

        self.messages = [SystemMessage(content=self.system_prompt)] #Inicializa el historial con el mensaje del sistema
        self.rag_system = GreenDreamRAG()
        
    def preguntar_con_rag(self, pregunta: str, temperature: float = 0.7, max_tokens: int = 1000, stream: bool = False, model: str = "gpt-4o"):
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
        
        # 2. Construir prompt enriquecido con contexto
        prompt_enriquecido = f"""
        {contexto_rag}

        CONSULTA DEL JOVEN: {pregunta}

        Por favor, proporciona una respuesta personalizada usando la información específica de Green Dream mostrada arriba.
        """
        
        # 3. Construir mensajes para la petición
        user_msg = UserMessage(content=prompt_enriquecido)
        messages_for_request = list(self.messages) + [user_msg] # Crea una lista con el mensaje de rol sistema y rol usuario
        
        if stream:
            return self._process_streaming(messages_for_request, user_msg, temperature, max_tokens, model)
        else:
            return self._process_non_streaming(messages_for_request, user_msg, temperature, max_tokens, model)
    
    def _process_streaming(self, messages_for_request, user_msg, temperature, max_tokens, model):
        """Procesa respuesta con streaming"""
        respuesta = ""
        try:
            stream_iter = client.complete(
                model=model,
                messages=messages_for_request,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            print("🌱 ", end="", flush=True)
            for event in stream_iter:
                if hasattr(event, "choices") and event.choices: #hasattr verifica que choices existe y no es None
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
        original_user_msg = UserMessage(content=user_msg.content.split("CONSULTA DEL JOVEN: ")[1] if "CONSULTA DEL JOVEN: " in user_msg.content else user_msg.content)
        self.messages.append(original_user_msg) #Guarda solo mensaje del usuario original
        self.messages.append(AssistantMessage(content=respuesta)) #Guarda respuesta del asistente
        
        return respuesta
    
    def _process_non_streaming(self, messages_for_request, user_msg, temperature, max_tokens, model):
        """Procesa respuesta sin streaming"""
        response = client.complete(
            model=model,
            messages=messages_for_request,
            temperature=temperature,
            max_tokens=max_tokens
        )
        assistant_content = response.choices[0].message.content
        
        # Guardar en historial (solo la pregunta original, no el contexto RAG)
        original_user_msg = UserMessage(content=user_msg.content.split("CONSULTA DEL JOVEN: ")[1] if "CONSULTA DEL JOVEN: " in user_msg.content else user_msg.content)
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
            
            if 'categoria' in metadata:
                formatted += f"   🏷️ Categoría: {metadata['categoria']}\n"
            if 'nivel' in metadata:
                formatted += f"   📊 Nivel: {metadata['nivel']}\n"
            if 'modalidad' in metadata:
                formatted += f"   💻 Modalidad: {metadata['modalidad']}\n"
            if 'precio' in metadata:
                formatted += f"   💰 Precio: {metadata['precio']}\n"
            if 'url' in metadata:
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
        cursos = len([d for d in self.rag_system.documents if d['type'] == 'curso'])
        articulos = len([d for d in self.rag_system.documents if d['type'] == 'articulo'])
        revistas = len([d for d in self.rag_system.documents if d['type'] == 'revista'])
        
        print("📊 **ESTADÍSTICAS BASE DE CONOCIMIENTO GREEN DREAM:**")
        print("=" * 50)
        print(f"📚 Total de recursos: {total_docs}")
        print(f"🎓 Cursos disponibles: {cursos}")
        print(f"📰 Artículos: {articulos}")
        print(f"📖 Revistas: {revistas}")
        print("=" * 50)