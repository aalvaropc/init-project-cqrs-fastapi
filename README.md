# Proyecto Backend - Arquitectura Hexagonal con CQRS y Bundle-Contexts

Este proyecto es un ejemplo completo que incluye:

- **Arquitectura Hexagonal**  
- **CQRS (Command Query Responsibility Segregation)**
- **Dos contexts** (`users` y `auth`)
- **RabbitMQ** para manejo de comandos
- **FastAPI** para la capa de presentación (API)
- **SQLAlchemy** y **PostgreSQL** para la persistencia
- **Alembic** para migraciones
- **Pruebas unitarias** con `pytest` y `pytest-cov`

---

## Requerimientos

- Docker y Docker Compose
- Python 3.9+ (para desarrollo local sin Docker, opcional)

---

## Cómo usar

1. **Clonar este repositorio**:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd project
