from config import DIR_DB

def create_db_directory():
    try:
        if not DIR_DB.exists():
            DIR_DB.mkdir(parents=True)
            print(f'Directorio de la base de datos creado en: {DIR_DB}')
        else:
            raise Exception('El directorio de la base de datos ya existe.')

        return True
    except Exception as e:
        raise Exception(f'Error al crear el directorio de la base de datos: {e}')