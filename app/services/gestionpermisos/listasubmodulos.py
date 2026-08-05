import httpx
import asyncio

from app.services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from app.services.funcioneskeycloak.get_admin_token import get_admin_token

from app.config.db import SessionLocal
from app.models.submodulos import Submodulos

def obtener_datos_submodulos_db():
    """
    Obtiene todos los datos de submódulos de la base de datos.
    """
    try:
        db = SessionLocal()
        submodulos = db.query(Submodulos).all()
        db.close()
        
        submodulos_dict = {}
        for submodulo in submodulos:
            submodulos_dict[submodulo.nombre] = {
                "modulo_padre": submodulo.modulo_padre,
                "path": submodulo.path,
                "icono": submodulo.icono,
                "habilitado": submodulo.habilitado
            }
        
        return submodulos_dict
    
    except Exception as e:
        return {}

async def obtener_submodulos_realm(numero_pagina: int = 1, filtro: str = None):
    """
    Obtiene la lista de submódulos del realm que comienzan con "SUBMODULO_" con paginación y filtro.
    Combina datos de Keycloak con datos de la base de datos local.
    """
    
    if numero_pagina < 1:
        numero_pagina = 1
    
    submodulos_por_pagina = 10
    skip = (numero_pagina - 1) * submodulos_por_pagina
    
    try:
        token = await get_admin_token()
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        roles_url = f"{get_admin_base_url()}/roles"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                roles_url,
                headers=headers
            )
            
            response.raise_for_status()
        
        roles_data = response.json()
        
        submodulos_procesados = []
        
        for rol in roles_data:
            if not rol["name"].startswith("SUBMODULO_"):
                continue
            
            if filtro:
                nombre = rol.get("name", "").lower()
                filtro_lower = filtro.lower()
                
                if filtro_lower not in nombre:
                    continue
            
            submodulo_procesado = {
                "nombre": rol.get("name")
            }
            
            submodulos_procesados.append(submodulo_procesado)
        
        submodulos_db = await asyncio.to_thread(obtener_datos_submodulos_db)
        
        for submodulo in submodulos_procesados:
            nombre = submodulo["nombre"]
            if nombre in submodulos_db:
                submodulo["modulo_padre"] = submodulos_db[nombre]["modulo_padre"]
                submodulo["path"] = submodulos_db[nombre]["path"]
                submodulo["icono"] = submodulos_db[nombre]["icono"]
                submodulo["habilitado"] = submodulos_db[nombre]["habilitado"]
            else:
                submodulo["modulo_padre"] = ""
                submodulo["path"] = ""
                submodulo["icono"] = ""
                submodulo["habilitado"] = False
        
        submodulos_paginados = submodulos_procesados[skip:skip + submodulos_por_pagina]
        
        return submodulos_paginados, len(submodulos_procesados)
    
    except httpx.HTTPError as e:
        error_detail = str(e)
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = e.response.text
            except:
                pass
        raise Exception(f"Error al conectar con Keycloak: {error_detail}")
    except Exception as e:
        raise Exception(f"Error al obtener lista de submódulos: {str(e)}")
