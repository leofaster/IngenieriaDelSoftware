# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras
import unittest
import cliente as cl
import moduloCliente as mc
import consumos as con
import productos as pr
import validacion
import database as db
import dbparams


def pedirFactura():
    if (pr.cantidadProductos() == 0):
        print "No hay ningun producto en el sistema."
        print "No se puede generar una factura."
        return
    
    
    print "Introduzca la informacion del cliente."
    idCliente = None
    
    while True:
        idCliente = int(validacion.validarNumero(' Cedula: '))        
        if (not mc.existeCliente(idCliente)):
            print " El cliente no se encuentra en el sistema."
        else:   
            if (mc.cantprodCliente(idCliente) == 0):
                print " El cliente no posee productos en el sistema."
            else:
                break  
            
    

    
    mc.listarProductos(idCliente)
    print "\nIntroduzca la informacion del producto."
    while True:
        numSerie = validacion.validarInput(' Numero de Serie: ')        
        if (not mc.poseeprodCliente(idCliente,numSerie)):
            print " El producto no corresponde a dicho cliente"
        else:
            break 
        
    print "Se procedera a la generacion de la factura."
    
    
    return Factura(idCliente,numSerie)
    
    

class Factura:
    def __init__(self, idCliente,idProducto):                   
        self.idProducto = idProducto
        self.cliente = mc.busquedaCliente(idCliente)
        self.mesFacturacion = self.buscarMes()
        self.anioFacturacion = self.buscarAnio()
        self.listaConsumos = self.buscarConsumos()
        self.listaCobrar = {}
        self.nombrePlan = ''
        self.totalPlan = 0
        self.totalPaquete = 0
        self.montoTotalCobrar = self.totalCobrar()

    def buscarCedula(self):
        try:
            conexion = db.operacion ("Buscamos la cedula del cliente",
                                    """SELECT cl.cedula FROM producto AS pr, cliente as cl 
                                       WHERE cl.cedula = pr.cedula AND numserie =\'%s\';""" %
                                       self.idProducto, dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
            resultado = conexion.execute()
            return str(resultado[0][0])
        except Exception, e:
            print "Error buscando la cedula del cliente", e
    
    def buscarMes(self):
        return str(raw_input("Por favor, introduzca el mes de facturacion "))
    
    def buscarAnio(self):
        return str(raw_input("Por favor, introduzca el año de facturacion "))

    def buscarConsumos(self):
        conexion = db.operacion("Buscamos todos los consumos asociados a un producto",
                             """ SELECT to_char(con.fecha, 'DD MM YYYY'), serv.nombreserv, con.cantidad
                                 FROM consume AS con, servicio AS serv 
                                 WHERE con.numserie = \'%s\'  AND to_number(to_char(con.fecha, 'MM'),'9999999') = %s 
                                 AND serv.codserv = con.codserv""" % (self.idProducto, self.mesFacturacion),
                                 dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
     
        return conexion.execute()

    def totalCobrar(self):
        conexion = db.operacion("Buscamos el codigo del plan asociado al producto",
                                """SELECT codplan FROM afilia WHERE numserie = \'%s\'""" % self.idProducto,
                                dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
        
        resultado = conexion.execute()
        
        if len(resultado) == 0:
            conexion = db.operacion("Buscamos el codigo del plan asociado al producto",
                                    """SELECT codplan FROM activa WHERE numserie = \'%s\'""" % self.idProducto,
                                    dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
            resultado = conexion.execute()

        codplan = resultado[0][0]

        #Buscamos la renta del plan que se va a cobrar al producto.      
        conexion = db.operacion("Buscamos la renta del plan que se va a cobrar al producto",
                                """SELECT renta_basica, nombreplan FROM plan WHERE codplan = %s""" % codplan,
                                dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
        resultado = conexion.execute()
        renta = int(resultado[0][0])
        
        self.nombrePlan = str(resultado[0][1])
        self.totalPlan = renta
        
        #Buscamos la suma de todos los consumos por servicio hechos por el producto en el año y mes introducidos por el usuario.
        #Lo guardamos en un diccionario donde la clave es el codigo del servicio.
        conexion = db.operacion("Buscamos la suma de todos los consumos por servicio",
                                """SELECT con.codserv, sum(con.cantidad) AS total FROM consume AS con 
                                WHERE con.numserie = \'%s\' AND 
                                to_char(con.fecha, 'MM YYYY') = \'%s\' GROUP BY (con.codserv)""" %
                                (self.idProducto, self.mesFacturacion + " " + self.anioFacturacion),
                                dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
       
        resultado = conexion.execute()
        
        totalConsumido = {}
        for row in resultado:
                totalConsumido[row[0]] = int(row[1])
        
        #Buscamos los servicios ofrecidos por el plan y la cantidad y tarifa ofrecidos por este. 
        #El resultado se guarda en un diccionario donde la clave es el codigo del servicio.
        
        conexion = db.operacion("Buscamos los servicios ofrecidos por el plan, ademas de la cantidad y tarifa ofrecidos por este",
                                """SELECT inc.codserv, inc.cantidad, inc.tarifa, serv.nombreserv FROM incluye AS inc, servicio AS serv 
                                WHERE inc.codplan =  %s and serv.codserv = inc.codserv;""" % codplan,
                                dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
        
        resultado = conexion.execute()       
         
        totalPlan = {}
        
        for row in resultado:
            totalPlan[row[0]] = [row[1], row[2], row[3]]
                
        #Se busca si el producto este asociado a algun paquete. De estarlo, las cantidades de servicio ofrecidas se agregan al
        #diccionario de los servicios ofrecidos por el plan.
        conexion = db.operacion("Paquetes a los que esta asociado un producto",
                                """SELECT codserv, cantidad, costo, nombreserv FROM contrata NATURAL JOIN contiene NATURAL JOIN servicio 
                                WHERE numserie = \'%s\'""" % self.idProducto,
                                dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
        
        resultado = conexion.execute()
        for row in resultado:
            codserv = row[0]
            if totalPlan.has_key(codserv):
                totalPlan[codserv][0] = totalPlan[codserv][0] + int(row[1])
            else:
                totalPlan[codserv] = [int(row[1]), row[2], row[3]]
        
        #Se busca el costo total de todos los paquetes a los que esta suscrito el producto. El resultado se almacena
        #en el total a cobrar.
        conexion = db.operacion("Costo total de todos los paquetes",
                                """SELECT sum(precio) FROM contrata NATURAL JOIN paquete 
                                WHERE numserie = \'%s\' GROUP BY(contrata.numserie)""" % self.idProducto,
                                dbparams.dbname,dbparams.dbuser,dbparams.dbpass)
        
        resultado = conexion.execute()
        if len(resultado) == 0:
            total = 0
        else:
            total = int(resultado[0][0])
        
        self.totalPaquete = total
        #Se verifica la suma de los consumos por servicio del producto, si excede el valor ofrecido por el plan/paquete
        #entonces se cobra lo indicado por el plan. En caso que el serivicio sea ofrecido por un paquete, se cobra por exceso
        #el costo del servicio.
        
        
        for con in totalConsumido.keys():
            consumido = totalConsumido[con]
            limite = totalPlan[con][0]
            self.listaCobrar[con] = [totalPlan[con][2], consumido, limite, 0]
            if consumido > limite:
                exceso = (consumido - limite) * totalPlan[con][1]
                total = total + exceso
                self.listaCobrar[con][3] = exceso
        
        print totalConsumido
        print totalPlan
        return total + renta
    
    def __str__(self):
        string = '\n{0:45}FACTURA\n'.format(' ') + str(self.cliente)
        string += '\n{4:45}SERVICIOS CONSUMIDOS\n{0:30} | {1:20} | {2:20} | {3:20}'.format('SERVICIO', 'TOTAL CONSUMIDO', 'LIMITE DEL PLAN', 'MONTO A COBRAR POR EXCESO',' ')
        for con in self.listaCobrar.keys():
            string += '\n{0:30} | {1:20} | {2:20} | {3:20}'.format \
                        (self.listaCobrar[con][0], str(self.listaCobrar[con][1]), str(self.listaCobrar[con][2]), str(self.listaCobrar[con][3]))
                    
        string += '\nMonto a cobrar por el plan ' + self.nombrePlan + ': ' + str(self.totalPlan)
        string += '\nMonto a cobrar por los paquetes afiliados: ' + str(self.totalPaquete)
        string += '\nTOTAL: ' + str(self.montoTotalCobrar)
        return string
if __name__ == '__main__':
    
    factura = pedirFactura()
    print factura