from typing import Optional
from app.config.db import SessionLocal
from app.models.modulos import Modulos

async def editar_modulo(
    modulo_nombre: str,
    subdominio: Optional[str] = None,
    path: Optional[str] = None,
    icono: Optional[str] = None
):
    """
    Edita un módulo existente en DB.
    """
    
    db = SessionLocal()
    
    try:
        modulo = db.query(Modulos).filter(
            Modulos.nombre == modulo_nombre
        ).first()
        
        if not modulo:
            db.close()
            raise Exception(f"El módulo '{modulo_nombre}' no existe en la base de datos")
        
        if subdominio is not None:
            modulo.subdominio = subdominio
        
        if path is not None:
            modulo.path = path
        else:
            modulo.path = ""
        
        if icono is not None:
            modulo.icono = icono
        
        db.commit()
        db.close()
        
        return {
            "detail": "Módulo actualizado exitosamente"
        }
    
    except Exception as e:
        db.close()
        raise Exception(str(e))
