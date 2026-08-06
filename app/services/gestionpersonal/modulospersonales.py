import asyncio
from app.config.db import SessionLocal
from app.models.modulos import Modulos


def obtener_datos_modulos_db(nombres_modulos: list[str]):
    """
    Obtiene los datos de módulos específicos de la base de datos.
    """
    try:
        db = SessionLocal()
        modulos = db.query(Modulos).filter(
            Modulos.nombre.in_(nombres_modulos),
            Modulos.habilitado == 1
        ).all()
        db.close()
        
        modulos_dict = {}
        for modulo in modulos:
            modulos_dict[modulo.nombre] = {
                "subdominio": modulo.subdominio,
                "path": modulo.path,
                "icono": modulo.icono
            }
        
        return modulos_dict
    
    except Exception as e:
        return {}


async def obtener_modulos_usuario(roles: list[str]):
    """
    Obtiene los módulos asignados al usuario basado en sus roles.
    """
    
    try:
        modulos_usuario = [rol for rol in roles if rol.startswith("MODULO_")]
        
        if not modulos_usuario:
            return {}
        
        modulos_db = await asyncio.to_thread(
            obtener_datos_modulos_db,
            modulos_usuario
        )
        
        resultado = {}
        for modulo_nombre in modulos_usuario:
            if modulo_nombre in modulos_db:
                db_data = modulos_db[modulo_nombre]
                resultado[modulo_nombre] = {
                    "url": f"{db_data['subdominio']}.intranetcreminox.com/{db_data['path']}",
                    "icono": db_data["icono"]
                }
        
        return resultado
    
    except Exception as e:
        raise Exception(f"Error al obtener módulos personales: {str(e)}")