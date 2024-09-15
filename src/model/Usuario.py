class Usuario:
    """
    Representa a un usuario del software
    """
    def __init__(self, nombre, contrasena):
        self.nombre = nombre
        self.contrasena = contrasena

    def __repr__(self):
        """
        Metodo para retornar los datos del usuario
        """
        return str(self.nombre)

    def es_Igual(self, comparar_con):
        """
        Compara el objeto actual, con otra instancia de la clase Usuario
        """
        assert(self.nombre == comparar_con.nombre)
        assert(self.contrasena == comparar_con.contrasena)