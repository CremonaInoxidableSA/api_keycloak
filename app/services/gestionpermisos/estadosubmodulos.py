from app.config.db import SessionLocal
from app.models.submodulos import Submodulos


def habilitar_submodulo(nombre: str):
    """
    Habilita un submódulo en la base de datos.
    """
    try:
        db = SessionLocal()
        
        submodulo = db.query(Submodulos).filter(
            Submodulos.nombre == nombre
        ).first()
        
        if not submodulo:
            db.close()
            raise Exception(f"El submódulo '{nombre}' no existe en la base de datos")
        
        if submodulo.habilitado:
            db.close()
            raise Exception(f"El submódulo '{nombre}' ya se encuentra habilitado")
        
        submodulo.habilitado = True
        db.commit()
        db.close()
        
        return {
            "mensaje": f"Submódulo '{nombre}' habilitado exitosamente",
            "nombre": nombre,
            "habilitado": True
        }
    
    except Exception as e:
        raise Exception(f"Error al habilitar submódulo: {str(e)}")


def deshabilitar_submodulo(nombre: str):
    """
    Deshabilita un submódulo en la base de datos.
    """
    try:
        db = SessionLocal()
        
        submodulo = db.query(Submodulos).filter(
            Submodulos.nombre == nombre
        ).first()
        
        if not submodulo:
            db.close()
            raise Exception(f"El submódulo '{nombre}' no existe en la base de datos")
        
        if not submodulo.habilitado:
            db.close()
            raise Exception(f"El submódulo '{nombre}' ya se encuentra deshabilitado")
        
        submodulo.habilitado = False
        db.commit()
        db.close()
        
        return {
            "mensaje": f"Submódulo '{nombre}' deshabilitado exitosamente",
            "nombre": nombre,
            "habilitado": False
        }
    
    except Exception as e:
        raise Exception(f"Error al deshabilitar submódulo: {str(e)}")
