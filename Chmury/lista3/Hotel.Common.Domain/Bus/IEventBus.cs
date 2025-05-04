using Hotel.Common.Domain.Commands;
using Hotel.Common.Domain.Events;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Hotel.Common.Domain.Bus
{
    public interface IEventBus
    {
        Task SendCommand<T>(T command) where T : Command;

        Task Publish<T>(T @event) where T : Event;

        Task Subscribe<T, TH>() where T : Event where TH : IEventHandler<T>;
    }
}
