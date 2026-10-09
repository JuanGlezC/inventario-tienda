from producto import Producto
from excepciones import NombreInvalidoError,SkuInvalidoError,PrecioInvalidoError,StockInvalidoError,StockInsuficienteError,CantidadInvalidaError
import pytest

@pytest.fixture
def producto_valido():
    return Producto(nombre="camiseta",sku="ACC-1998",stock=10,precio=15.50)

def test_producto_valido_se_crea_correctamente(producto_valido):
    
    assert producto_valido.nombre=="camiseta"
    assert producto_valido.sku=="ACC-1998"
    assert producto_valido.stock==10
    assert producto_valido.precio==15.50

@pytest.mark.parametrize("nombre,sku,stock,precio,excepcion_esperada", [
    ("123","ACC-1999",10,15.50, NombreInvalidoError),
    ("camiseta","a-19",15,15.50, SkuInvalidoError),
    (1.0, "ACC-1999",10,15.50, NombreInvalidoError),
    ("camiseta","ACC-1999",10,"quince",PrecioInvalidoError),
    ("camiseta","ACC-1999",10,-15.50,PrecioInvalidoError),
    ("camiseta","ACC-1999",-2,15.50, StockInvalidoError),
    ("camiseta","ACC-1992",0,0,PrecioInvalidoError),
    ("","ACC-1992",12,14.0,NombreInvalidoError),
    ("camiseta","ACC-1991","5",12.0,StockInvalidoError),
    ("camiseta","ACC-1999",5.5,12.0,StockInvalidoError),
    ("camiseta","ACC-1999",None,12.0,StockInvalidoError),
    ("camiseta","ACC-1222",10,None,PrecioInvalidoError),
    ("camiseta",123,10,10.0,SkuInvalidoError),
    ("   ","ACC-1223",10,10.0,NombreInvalidoError),
    ("camiseta","ACC1223",10,10.0,SkuInvalidoError),
    ("camiseta","ACC-123344",10,10.0,SkuInvalidoError),
    ("camiseta","AC-1234",10,10.0,SkuInvalidoError)
])
def test_producto_invalido_lanza_excepcion_correcta(nombre, sku, stock,precio, excepcion_esperada):
    with pytest.raises(excepcion_esperada):
        Producto(nombre=nombre, sku=sku,stock=stock,precio=precio)

def test_producto_genera_id_automaticamente():
    producto = Producto(nombre="camiseta",sku="ACC-1992",stock=10,precio=12.0)
    assert producto.id != ""
    assert isinstance(producto.id, str)

def test_dos_productos_distintos_tienen_ids_distintos():
    producto1 = Producto(nombre="camiseta",sku="CAM-1223",stock=10,precio=12.0)
    producto2 = Producto(nombre="pantalon",sku="PNT-1227",stock=15,precio=14.0)
    assert producto1.id != producto2.id

def test_nombre_espacios_se_crea_correctamente():
    producto = Producto(nombre="   camiseta   ",sku="ACC-1992",stock=10,precio=15.0)
    assert producto.nombre=="camiseta"

def test_precio_entero_se_crea_correctamente():
    producto=Producto(nombre="camiseta",sku="ACC-1993",stock=10,precio=11)
    assert producto.precio==11

def test_sku_minusculas_se_crea_correctamente():
    producto=Producto(nombre="camiseta",sku=" acc-1992 ",stock=10,precio=12.0)
    assert producto.sku=="ACC-1992"

def test_stock_cero_se_crea_correctamente():
    producto=Producto(nombre="camiseta",sku="ABB-1235",stock=0,precio=11.0)
    assert producto.stock==0

def test_vender_reduce_stock():
    producto=Producto(nombre="camiseta",sku="ABB-1224",stock=2,precio=10.0)
    producto.vender(1)
    assert producto.stock==1

def test_reponer_aumenta_stock():
    producto=Producto(nombre="camiseta",sku="ABB-1223",stock=3,precio=10.0)
    producto.reponer(1)
    assert producto.stock==4

def test_stock_queda_a_cero():
    producto=Producto(nombre="camiseta",sku="ABB-1223",stock=3,precio=10.0)
    producto.vender(producto.stock)
    assert producto.stock==0

def test_stock_insuficiente():

    producto=Producto(nombre="camiseta",sku="ABB-1223",stock=3,precio=10.0)
    with pytest.raises(StockInsuficienteError):
        producto.vender(4)
    assert producto.stock==3

def test_cantidad_invalida_lanza_excepcion():
    producto=Producto(nombre="camiseta",sku="ABB-1223",stock=3,precio=10.0)
    with pytest.raises(CantidadInvalidaError):
        producto.reponer(0)
    assert producto.stock==3
   
@pytest.mark.parametrize("cantidad", [0, -1, 5.5, "3", None])
def test_vender_cantidad_invalida(cantidad):
    producto=Producto(nombre="camiseta",sku="ABB-1223",stock=3,precio=10.0)
    with pytest.raises(CantidadInvalidaError):
        producto.vender(cantidad)
    assert producto.stock==3

@pytest.mark.parametrize("cantidad", [0, -1, 5.5, "3", None])
def test_reponer_cantidad_invalida(cantidad):
    producto=Producto(nombre="camiseta",sku="ABB-1223",stock=3,precio=10.0)
    with pytest.raises(CantidadInvalidaError):
        producto.reponer(cantidad)
    assert producto.stock==3