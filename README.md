# Twilight AI – Lokale KI-Plattform

> **100 % lokal** – Keine API-Keys, keine externen Dienste.  
> Nutzt Ollama, Stable Diffusion, Whisper und Coqui TTS.

## Features
- 💬 Chat mit Kontext, RAG (PDF‑Upload) und Langzeitgedächtnis
- 🖼️ Bilder generieren (Stable Diffusion)
- 🎤 Sprache‑zu‑Text (Whisper) & Text‑zu‑Sprache (Coqui TTS)
- 🔐 Benutzerkonten mit JWT
- 📱 Responsives Web‑Interface (React)

## Schnellstart
1. `.env` aus `.env.example` erstellen (SECRET_KEY selbst generieren)
2. `docker-compose up -d` startet alle Container
3. **Einmalig** Modelle in Ollama laden:
   ```bash
   docker exec -it twilight_ollama ollama pull llama3.2:3b
   docker exec -it twilight_ollama ollama pull nomic-embed-text
