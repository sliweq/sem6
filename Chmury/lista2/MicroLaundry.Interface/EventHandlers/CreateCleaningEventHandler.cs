using Hotel.Common.Domain.Bus;
using MediatR;
using MicroLaundry.Domain.Commands;
using MicroLaundry.Domain.Events;
using MicroLaundry.Domain.Queries;
using MicroLaundry.Interface.QueryHandlers;
using Microsoft.Extensions.Logging;

namespace MicroLaundry.Interface.EventHandlers
{
    public class CreateCleaningEventHandler : IEventHandler<CreateCleaningEvent>
    {
        private readonly IMediator _mediator;
        private readonly ILogger<CreateCleaningEventHandler> _logger; 

        public CreateCleaningEventHandler(IMediator mediator, ILogger<CreateCleaningEventHandler> logger)
        {
            _mediator = mediator;
            _logger = logger;
        }


        public async Task Handle(CreateCleaningEvent @event)
        {
            _logger.LogInformation($"Handled CreateCleaningEvent for {@event.StartDate} -> {@event.EndDate} : {@event.NumberOfPeople} people");

            var response = await _mediator.Send(new GetLaundryQuery(@event.StartDate,@event.EndDate));
            if (response is null)
            {
                return;
            }
            await _mediator.Send(new CreateLaundryCommand(response,@event.NumberOfPeople, @event.StartDate, @event.EndDate));
            return;
        }
    }

}
