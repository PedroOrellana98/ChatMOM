#!/usr/bin/env python
import pika
from threading import Thread
import time

class TH_server(Thread):

    def __init__ (self, num):
        Thread.__init__(self)
        self.num = num
    
    def run(self):

        def callback(ch, method, properties, body):

            print("                                   %s" % body.decode())

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='servidor')
        channel.basic_consume(queue='servidor', on_message_callback=callback, auto_ack=True)

        print('\n En linea \n')
        channel.start_consuming()



class TH_send(Thread):

    def __init__ (self, num):
        Thread.__init__(self)
        self.num = num
    
    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        
        def Enviar(canal,mensage):

            canal.basic_publish(exchange='', routing_key='hello', body= mensage)

        def Salir(conectar):
            conectar.close()

        while True:

            time.sleep(1)
            b = input("")

            if b == 'salir':
                Enviar(channel,"\n Cliente salio de la conversacion.")
                Salir(connection)
                print("Salio de la conversacion")
            else:
                Enviar(channel, b)

# criando thread
servidor = TH_server(1)
servidor.start()

envio = TH_send(1)
envio.start()