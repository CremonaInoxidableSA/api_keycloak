import httpx
from app.config.db import SessionLocal
from app.models.modulos import Modulos


async def obtener_detalles_modulo(nombre_modulo: str):
    """
    Obtiene los detalles de un módulo incluyendo:
    - nombre del módulo
    - subdominio (desde BD)
    - path (desde BD)
    - icono (desde BD)
    
    Args:
        nombre_modulo: Nombre del módulo (ej: MODULO_USUARIOS)
    
    Returns:
        dict con estructura {nombre, subdominio, path, icono}
    
    Raises:
        Exception: Si el módulo no existe en la BD
    """
    
    try:
        db = SessionLocal()
        
        # Buscar el módulo en la base de datos
        modulo = db.query(Modulos).filter(
            Modulos.nombre == nombre_modulo
        ).first()
        
        db.close()
        
        if not modulo:
            raise Exception(f"El módulo '{nombre_modulo}' no existe en la base de datos")
        
        return {
            "nombre": modulo.nombre,
            "subdominio": modulo.subdominio,
            "path": modulo.path,
            "icono": modulo.icono
        }
    
    except Exception as e:
        raise Exception(f"Error al obtener detalles del módulo: {str(e)}")
