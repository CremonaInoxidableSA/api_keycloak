import httpx
from app.config.db import SessionLocal
from app.models.submodulos import Submodulos


async def obtener_detalles_submodulo(submodulo_nombre: str):
    """
    Obtiene los detalles de un submódulo incluyendo:
    """
    
    try:
        db = SessionLocal()
        
        # Buscar el submódulo en la base de datos
        submodulo = db.query(Submodulos).filter(
            Submodulos.nombre == submodulo_nombre
        ).first()
        
        db.close()
        
        if not submodulo:
            raise Exception(f"El submódulo '{submodulo_nombre}' no existe en la base de datos")
        
        return {
            "nombre": submodulo.nombre,
            "modulo_padre": submodulo.modulo_padre,
            "path": submodulo.path,
            "icono": submodulo.icono
        }
    
    except Exception as e:
        raise Exception(f"Error al obtener detalles del submódulo: {str(e)}")
