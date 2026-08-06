import httpx
from app.config.db import SessionLocal
from app.models.modulos import Modulos


async def obtener_detalles_modulo(modulo_nombre: str):
    """
    Obtiene los detalles de un módulo.
    """
    
    try:
        db = SessionLocal()
        
        # Buscar el módulo en la base de datos
        modulo = db.query(Modulos).filter(
            Modulos.nombre == modulo_nombre
        ).first()
        
        db.close()
        
        if not modulo:
            raise Exception(f"El módulo '{modulo_nombre}' no existe en la base de datos")
        
        return {
            "nombre": modulo.nombre,
            "subdominio": modulo.subdominio,
            "path": modulo.path,
            "icono": modulo.icono
        }
    
    except Exception as e:
        raise Exception(f"Error al obtener detalles del módulo: {str(e)}")
