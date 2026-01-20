# IntegriApp Backend - Sistema de Gestión de Rutas y Vehículos

API REST desarrollada con **FastAPI** y **PostgreSQL** para la gestión de vehículos, rutas y análisis de rendimiento.

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Docker** (versión 20.10 o superior)
- **Docker Compose** (versión 2.0 o superior)
- **Git** (para clonar el repositorio)

### Verificar instalación

```bash
docker --version
docker-compose --version
```

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd integriapp-test-backend
```

### 2. Configurar variables de entorno

**⚠️ IMPORTANTE:** Copia el archivo de ejemplo y configura tus variables de entorno:

```bash
cp .env.example .env
```

El archivo `.env` contiene las siguientes configuraciones:

```env
# Database
POSTGRES_USER=integriapp
POSTGRES_PASSWORD=integriapp
POSTGRES_DB=integriapp_db

# Database URL
DATABASE_URL=postgresql://integriapp:integriapp@localhost:5432/integriapp_db

# App
APP_NAME=IntegriApp
APP_VERSION=1.0.0
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000
```

> **Nota:** Puedes modificar estos valores según tus necesidades.

### 3. Levantar el proyecto

Con un solo comando:

```bash
docker-compose up -d
```

Esto hará lo siguiente:
- ✅ Construir la imagen de la aplicación FastAPI
- ✅ Levantar PostgreSQL en el puerto `5432`
- ✅ Levantar la API en el puerto `8000`
- ✅ Crear automáticamente las tablas en la base de datos

### 4. Verificar que todo está corriendo

```bash
docker-compose ps
```

Deberías ver algo como:

```
NAME                IMAGE              STATUS
integriapp-db       postgres:15        Up
integriapp-api      integriapp-api     Up
```

### 5. Acceder a la aplicación

- **API Base:** http://localhost:8000
- **Documentación Interactiva (Swagger):** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 📁 Estructura del Proyecto

```
integriapp-test-backend/
├── app/
│   ├── main.py                     # Aplicación principal FastAPI
│   ├── configuration/
│   │   └── configuration.py        # Configuración y variables de entorno
│   ├── core/
│   │   └── database.py             # Configuración de SQLAlchemy
│   ├── model/           
│   ├── schemas/                    # Esquemas Pydantic (DTOs)
│   ├── repository/               # Capa de acceso a datos
│   ├── service/                   # Lógica de negocio
│   └── controller/                # Endpoints REST
├── .env                            # Variables de entorno
├── .env.example                    # Ejemplo de variables de entorno
├── .dockerignore                   # Archivos ignorados por Docker
├── docker-compose.yml              # Orquestación de contenedores
├── Dockerfile                      # Imagen de la aplicación
├── requirements.txt                # Dependencias de Python
└── README.md                       # Este archivo
```

## 🛠️ Comandos Útiles

```

### Con Docker Compose

```bash
# Levantar servicios en segundo plano
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f app
docker-compose logs -f db

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (⚠️ elimina datos de la BD)
docker-compose down -v

# Reconstruir imágenes
docker-compose build --no-cache

# Reiniciar un servicio específico
docker-compose restart app
```

## 🧪 Probar la API

### 1. Health Check

```bash
curl http://localhost:8000/health
```

> **💡 Tip:** Es más fácil probar los endpoints usando la documentación interactiva en http://localhost:8000/docs

## 📊 Módulos Implementados

### 1. Módulo de Vehículos
- ✅ CRUD completo de vehículos
- ✅ Soft delete (desactivar en lugar de eliminar)

### 2. Módulo de Rutas
- ✅ Gestión de rutas (origen, destino, estatus)
- ✅ Búsqueda por estatus y unidad

### 3. Módulo de Redminiento
- ✅ En el ciclo de vida: Completed
- ✅ Registro de métricas: distancia, combustible
- ✅ Cálculo automático de rendimiento (km/litro)

## 🏗️ Arquitectura y Diseño

### Patrón de Capas (Similar a Spring Boot)

```
Controller (REST API)
    ↓
Service (Lógica de Negocio)
    ↓
Repository (Acceso a Datos)
    ↓
Model (Entidades de BD)
```

### Características Técnicas

- **Framework:** FastAPI (Python 3.14)
- **ORM:** SQLAlchemy 2.0
- **Base de Datos:** PostgreSQL 15
- **Validación:** Pydantic V2
- **Containerización:** Docker & Docker Compose
- **Documentación:** OpenAPI (Swagger/ReDoc)

## 🔧 Desarrollo Local (Sin Docker)

Si prefieres desarrollar sin Docker:


### 1. Crear base de datos

```bash
createdb -U postgres integriapp_db
```

### 2. Instalar dependencias de Python

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar .env

Asegúrate de que `DATABASE_URL` apunte a tu PostgreSQL local.

### 4. Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

## 🐛 Troubleshooting


### Error: "Could not connect to database"

**Solución:** Verifica que PostgreSQL esté corriendo:

```bash
docker-compose ps
docker-compose logs db
```

Si no está corriendo:

```bash
docker-compose up -d db
```

### Error: "Port 5432 already in use"

**Solución:** Ya tienes PostgreSQL corriendo localmente. Opciones:

1. Detener PostgreSQL local: `brew services stop postgresql`
2. Cambiar el puerto en `docker-compose.yml`: `"5433:5432"`

### La aplicación no recarga automáticamente

**Solución:** Verifica que el volumen esté montado correctamente en `docker-compose.yml`:

```yaml
volumes:
  - .:/app
```

### Resetear completamente el proyecto

```bash
# Detener todo y eliminar volúmenes
docker-compose down -v

# Eliminar imágenes
docker-compose down --rmi all

# Reconstruir desde cero
docker-compose build --no-cache
docker-compose up -d
```

## 📚 Documentación Adicional

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 📝 Notas Importantes

- 💾 **Persistencia:** Los datos de PostgreSQL se guardan en volúmenes Docker
- 🔄 **Hot Reload:** Los cambios en el código se reflejan automáticamente
- 📊 **Logging:** En modo `DEBUG=True` se muestran todas las queries SQL

## 🤝 Contribución

Este proyecto fue desarrollado como prueba técnica para IntegriApp.


---

### **Desarrollado Por Oscar Omar Arias Rodríguez 🐻**