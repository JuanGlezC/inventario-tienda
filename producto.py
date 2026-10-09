from dataclasses import dataclass
import uuid
from excepciones import NombreInvalidoError,SkuInvalidoError,StockInvalidoError,PrecioInvalidoError,CantidadInvalidaError,StockInsuficienteError
import re

@dataclass
class Producto:
    
    nombre:str
    sku:str
    stock:int
    precio:float
    id:str=""

    def __post_init__(self):
        
        if not self.id:
            self.id = str(uuid.uuid4())
        if not isinstance(self.nombre, str):
            raise NombreInvalidoError(f"El nombre debe ser un texto: {self.nombre!r}")
        self.nombre = self.nombre.strip()
        if not self.nombre:
            raise NombreInvalidoError("El nombre no puede estar vacío")
        if self.nombre.isdigit():
            raise NombreInvalidoError("El nombre no puede estar compuesto por numeros unicamente")
        if not isinstance(self.sku,str):
            raise SkuInvalidoError(f"El sku debe ser un string {self.sku}")
        
        codigo = self.sku.replace(" ", "").upper()
        if re.fullmatch(r"[A-Z]{3}-[0-9]{4}", codigo) is None:
            raise SkuInvalidoError(f"Código inválido: {codigo!r}")
        self.sku = codigo
        
        if not isinstance(self.stock,int):
            raise StockInvalidoError(f"El stock debe ser un numero entero: {self.stock}")
        if self.stock<0:
            raise StockInvalidoError(f"El stock no puede ser menor que 0: {self.stock}")
        if not isinstance(self.precio, (int, float)):
            raise PrecioInvalidoError(f"El precio debe ser un número: {self.precio}")
        if self.precio<=0:
            raise PrecioInvalidoError(f"Un precio no puede ser negativo o igual a 0: {self.precio}")
                
    def vender(self, cantidad):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise CantidadInvalidaError(f"La cantidad debe ser un entero mayor que 0: {cantidad!r}")
        if cantidad > self.stock:
            raise StockInsuficienteError(f"Stock insuficiente: hay {self.stock} y se piden {cantidad}")
        self.stock -= cantidad

    def reponer(self,cantidad):
        if not isinstance(cantidad,int) or cantidad <= 0:
            raise CantidadInvalidaError(f"La cantidad debe ser un entero mayor que 0: {cantidad!r}")
        self.stock += cantidad
