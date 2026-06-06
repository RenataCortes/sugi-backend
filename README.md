# Sugi Backend API

Backend desarrollado con **FastAPI** para el sistema de gestión y motor de Inteligencia Artificial (RAG). Este proyecto utiliza una arquitectura limpia basada en capas (**API → Services → Repositories**) para garantizar la escalabilidad, el aislamiento de la lógica de negocio y la seguridad del sistema.

---

## Arquitectura del proyecto

El proyecto sigue una estructura modular por capas:

```text
├── main.py                     # Punto de arranque y configuración de CORS
├── app/
│   ├── api/                    # CAPA 1: Endpoints (Routers, Schemas y Dependencias)
│   ├── services/               # CAPA 2: Lógica de Negocio y Motor RAG (IA)
│   ├── repositories/           # CAPA 3: Acceso a Datos (SQL Server y Vector DB)
│   └── core/                   # Configuraciones Globales y Seguridad
```

## 🚀 Tecnologías Principales

### Framework

* FastAPI
* Uvicorn

### Base de Datos Relacional

* SQL Server
* SQLAlchemy
* Psycopg2

### Base de Datos Vectorial

* ChromaDB

### Orquestación de IA

* LangChain

### Seguridad

* JWT Tokens
* Passlib (Bcrypt)

---

## Configuración Local

Sigue estos pasos para levantar el entorno de desarrollo:

### 1. Clonar el repositorio e ingresar a la carpeta

```bash
git clone https://github.com/RenataCortes/sugi-backend.git
cd sugi-back
```

### 2. Crear y activar el entorno virtual (.venv)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto basándote en tus credenciales necesarias:

* Variables de Base de Datos
* JWT Secret Keys
* API Keys de LLMs
* Otras configuraciones requeridas para el proyecto

### 5. Arrancar el servidor de desarrollo

```bash
uvicorn main:app --reload
```

El servidor estará disponible en:

```text
http://127.0.0.1:8000
```

La documentación interactiva (Swagger) estará en:

```text
http://127.0.0.1:8000/docs
```

---

## Flujo de Trabajo (Git Flow)

Este proyecto utiliza **Git Flow** de manera estricta para la gestión de ramas. Toda funcionalidad debe desarrollarse en ramas independientes.

### Ramas principales

* **develop** → Rama de desarrollo (por defecto)
* **master** → Rama de producción

### Comandos básicos

#### Iniciar una nueva característica

```bash
git flow feature start nombre-de-la-funcion
```

#### Finalizar una característica y unirla a develop

```bash
git flow feature finish nombre-de-la-funcion
```
