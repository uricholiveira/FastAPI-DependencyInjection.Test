from app.core.rabbitmq import RabbitMQManager


class RabbitMqTest:
    @staticmethod
    async def test_message():
        message = "Hello World!"

        rabbitmq = RabbitMQManager(url="amqp://guest:guest@localhost/")
        await rabbitmq.connect()

        await rabbitmq.send_message(message=message, routing_key="black")
