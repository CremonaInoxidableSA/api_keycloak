import httpx
from app.config.db import SessionLocal
from app.models.submodulos import Submodulos


async def obtener_detalles_submodulo(nombre_submodulo: str):
    """
    Obtiene los detalles de un submódulo incluyendo:
    """
    
    try:
        db = SessionLocal()
        
        # Buscar el submódulo en la base de datos
        submodulo = db.query(Submodulos).filter(
            Submodulos.nombre == nombre_submodulo
        ).first()
        
        db.close()
        
        if not submodulo:
            raise Exception(f"El submódulo '{nombre_submodulo}' no existe en la base de datos")
        
        return {
            "nombre": submodulo.nombre,
            "modulo_padre": submodulo.modulo_padre,
            "path": submodulo.path,
            "icono": submodulo.icono
        }
    
    except Exception as e:
        raise Exception(f"Error al obtener detalles del submódulo: {str(e)}")
