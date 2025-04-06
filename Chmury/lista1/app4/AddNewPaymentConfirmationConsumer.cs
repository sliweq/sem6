using Microsoft.Extensions.Logging;
using RabbitMQ.Client.Events;
using RabbitMQ.Client;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using domain4;
using System.Runtime.CompilerServices;

namespace app4
{
    class AddNewPaymentConfirmationConsumer
    {

        private readonly IChannel _channel;
        private readonly ILogger _logger;

        public AddNewPaymentConfirmationConsumer(IChannel channel, ILogger logger)
        {
            _channel = channel;
            _logger = logger;
        }

        async public void StartConsuming()
        {
            string qName = typeof(PaymentConfirmationEvent).Name; 
            await _channel.QueueDeclareAsync(queue: qName, durable: true, exclusive: false, autoDelete: false, arguments: null);

            var consumer = new AsyncEventingBasicConsumer(_channel);
            consumer.ReceivedAsync += (model, ea) =>
            {
                var body = ea.Body.ToArray();
                var message = Encoding.UTF8.GetString(body);
                LogInfo($"Recived new message from {qName}': {message}");

                return Task.CompletedTask;
            };

            await _channel.BasicConsumeAsync(queue: qName, autoAck: true, consumer: consumer);
            LogInfo("Started listening...");
        }
        public void Run()
        {
            StartConsuming();
            LogInfo("Started listening...");
            Console.ReadLine();


        }

        private void LogInfo(string data, [CallerMemberName] string methodName = "")
        {
            _logger.LogInformation("[{Method}] {Message}", methodName, data);
        }
    }
}
