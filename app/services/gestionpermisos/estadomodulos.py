from app.config.db import SessionLocal
from app.models.modulos import Modulos


def habilitar_modulo(nombre: str):
    """
    Habilita un módulo en la base de datos.
    """
    try:
        db = SessionLocal()
        
        modulo = db.query(Modulos).filter(
            Modulos.nombre == nombre
        ).first()
        
        if not modulo:
            db.close()
            raise Exception(f"El módulo '{nombre}' no existe en la base de datos")
        
        if modulo.habilitado:
            db.close()
            raise Exception(f"El módulo '{nombre}' ya se encuentra habilitado")
        
        modulo.habilitado = True
        db.commit()
        db.close()
        
        return {
            "detail": f"Módulo '{nombre}' habilitado exitosamente"
        }
    
    except Exception as e:
        raise Exception(f"Error al habilitar módulo: {str(e)}")


def deshabilitar_modulo(nombre: str):
    """
    Deshabilita un módulo en la base de datos.
    """
    try:
        db = SessionLocal()
        
        modulo = db.query(Modulos).filter(
            Modulos.nombre == nombre
        ).first()
        
        if not modulo:
            db.close()
            raise Exception(f"El módulo '{nombre}' no existe en la base de datos")
        
        if not modulo.habilitado:
            db.close()
            raise Exception(f"El módulo '{nombre}' ya se encuentra deshabilitado")
        
        modulo.habilitado = False
        db.commit()
        db.close()
        
        return {
            "detail": f"Módulo '{nombre}' deshabilitado exitosamente"
        }
    
    except Exception as e:
        raise Exception(f"Error al deshabilitar módulo: {str(e)}")
