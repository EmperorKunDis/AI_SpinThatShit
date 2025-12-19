---
**🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)
---

# 🔄 SpinThatShit

**Orquestación Autónoma de Agentes de IA para Desarrollo de Software**

Un sistema para gestionar múltiples agentes de IA (Claude Code CLI) que colaboran en el desarrollo de software. Cada agente tiene un rol específico y el sistema garantiza la continuidad del trabajo incluso cuando se alcanzan los límites de contexto.

---

## 🚀 Inicio Rápido

```bash
# Instalación
chmod +x install.sh
./install.sh

# Ejecutar
spinthatshit
# o más corto
sts
```

---

## 📋 Características

### Flujo de Trabajo Multi-Agente
- **Planner** - Analiza documentación, crea plan
- **Designer** - Diseña componentes UI/UX
- **Engineer** - Construye infraestructura y arquitectura
- **Developer** - Implementa funcionalidades
- **Reviewer** - Revisa calidad del código
- **Tester** - Prueba funcionalidad
- **Supervisor** - Identifica conflictos y problemas
- **Evolver** - Mejora el sistema mismo

### Gestión de Contexto
- Seguimiento automático del uso de contexto
- Traspaso al 50% del límite
- Continuidad del trabajo entre agentes

### Integración con Git
- Commit automático después de cada cambio
- Etiquetado de fases
- Auto-push a GitHub

### Auto-Evolución
- El sistema aprende de los errores
- Mejora automáticamente los prompts
- Añade nuevas verificaciones

---

## 📁 Estructura del Proyecto

Después de ejecutar, se crea la siguiente estructura en la carpeta de desarrollo:

```
your-project/
├── .spinstate/
│   ├── state.json          # Estado de orquestación
│   ├── journal.md          # Diario de todos los agentes
│   ├── plan.md             # Plan del proyecto
│   ├── checklist.md        # Lista de tareas
│   ├── architecture.md     # Arquitectura
│   ├── handoff.md          # Notas de traspaso
│   ├── status.txt          # Estado actual
│   ├── review.md           # Resultados de revisión
│   ├── test_report.md      # Resultados de pruebas
│   └── logs/               # Registros de todos los agentes
├── CLAUDE.md               # Instrucciones para Claude
└── ... (tu código)
```

---

## 🎯 Uso

### Modo Interactivo
```bash
spinthatshit
```

El sistema preguntará por:
1. Ruta de documentación
2. Ruta de carpeta de desarrollo

### Con Parámetros
```bash
spinthatshit --docs ./docs --dev ./src
```

### Reanudar
```bash
spinthatshit --resume
```

---

## ⚙️ Configuración

Archivo de configuración: `~/.spinthatshit/config.json`

```json
{
    "context_limit_percent": 50,
    "max_retries": 3,
    "agent_timeout_minutes": 30,
    "auto_push": true,
    "agents": {
        "workflow_order": ["planner", "designer", "engineer", ...],
        "enabled": {
            "designer": true,
            "tester": true
        }
    }
}
```

---

## 🔧 Requisitos

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS o Linux**

---

## 📖 Cómo Funciona

### 1. Inicialización
El sistema carga la documentación y el código existente, crea un plan.

### 2. Ejecución por Fases
Cada agente se ejecuta secuencialmente:
1. Carga el contexto desde journal.md
2. Realiza su trabajo
3. Hace commit de los cambios
4. Escribe en la lista de verificación
5. Traspasa al siguiente agente

### 3. Traspaso de Contexto
Cuando un agente alcanza el 50% de contexto:
1. Escribe el estado en handoff.md
2. Hace commit de todo
3. Termina
4. Un nuevo agente continúa

### 4. Recuperación
En caso de fallo:
1. Supervisor analiza el problema
2. Orchestrator ajusta las reglas
3. El agente se reinicia

### 5. Evolución
Después de completar el proyecto:
1. Evolver analiza qué funcionó
2. Ajusta los prompts de los agentes
3. Añade nuevas verificaciones

---

## 🎬 Ejemplo de Ejecución

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] FASE: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner completado (contexto: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] FASE: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Contexto al 52% - traspasando al siguiente agente
[14:35:48] [INFO] Reiniciando agente developer (intento 1/3)
...
```

---

## 🛑 Detener

- **Ctrl+C** - Detención segura, el estado se guarda
- Usa `--resume` para continuar

---

## 🐛 Solución de Problemas

### El agente está atascado
```bash
# Revisa los registros
cat your-project/.spinstate/logs/agent_*.log
```

### Errores en el código
El sistema tiene auto-recuperación, pero puedes:
1. Editar `.spinstate/checklist.md`
2. Añadir una nota a `.spinstate/journal.md`
3. Ejecutar de nuevo

### Desbordamiento de contexto
- Aumenta `context_limit_percent` en config.json
- Divide el proyecto en fases más pequeñas

---

## 📝 Consejos

1. **La documentación es clave** - Mejor documentación, mejores resultados
2. **Empieza con proyectos pequeños** - Aprende el sistema con un proyecto simple
3. **No revises cada paso** - Deja que los agentes trabajen
4. **Confía en los traspasos** - El sistema recuerda el contexto

---

## 🗑️ Desinstalación

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Licencia

MIT License - Uso libre

---

## 🤝 Creado para

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Dejamos que la IA trabaje mientras comemos pastel."* 🍰
