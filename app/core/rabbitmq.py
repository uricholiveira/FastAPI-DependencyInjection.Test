from aio_pika import ExchangeType, Message, connect


class RabbitMQManager:
    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        self.connection = await connect(self.url)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange('my_exchange', ExchangeType.DIRECT)

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def send_message(self, message: str, routing_key: str):
        if not self.connection:
            await self.connect()
        message = Message(body=message.encode())
        await self.exchange.publish(message, routing_key=routing_key)

    async def consume_messages(self, queue_name: str, callback):
        if not self.connection:
            await self.connect()
        queue = await self.channel.declare_queue(queue_name)
        await queue.bind(self.exchange, queue_name)
        await queue.consume(callback)
