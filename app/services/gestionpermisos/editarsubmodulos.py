from typing import Optional
from app.config.db import SessionLocal
from app.models.submodulos import Submodulos
from app.models.modulos import Modulos

async def editar_submodulo(
    submodulo_nombre: str,
    modulo_padre: Optional[str] = None,
    path: Optional[str] = None,
    icono: Optional[str] = None
):
    """
    Edita un submódulo existente en la base de datos.
    """
    
    db = SessionLocal()
    
    try:
        submodulo = db.query(Submodulos).filter(
            Submodulos.nombre == submodulo_nombre
        ).first()
        
        if not submodulo:
            db.close()
            raise Exception(f"El submódulo '{submodulo_nombre}' no existe en la base de datos")
        
        if modulo_padre is not None:
            modulo_padre_existente = db.query(Modulos).filter(
                Modulos.nombre == modulo_padre
            ).first()
            
            if not modulo_padre_existente:
                db.close()
                raise Exception(f"El módulo padre '{modulo_padre}' no existe en la base de datos")
        
        if modulo_padre is not None:
            submodulo.modulo_padre = modulo_padre
        
        if path is not None:
            submodulo.path = path
        else:
            submodulo.path = ""

        if icono is not None:
            submodulo.icono = icono
        
        db.commit()
        db.close()
        
        return {
            "detail": "Submódulo actualizado exitosamente"
        }
    
    except Exception as e:
        db.close()
        raise Exception(str(e))
