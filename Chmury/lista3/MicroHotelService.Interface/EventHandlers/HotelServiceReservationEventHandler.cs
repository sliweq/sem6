using Hotel.Common.Domain.Bus;
using MediatR;
using MicroHotelService.Domain.Events;
using MicroHotelService.Domain.Commands;
using MicroHotelService.Domain.Queries;
using Microsoft.Extensions.Logging;

namespace MicroHotelService.Interface.EventHandlers
{
    public class HotelServiceReservationEventHandler : IEventHandler<CreateReservationEvent>
    {
        private readonly IMediator _mediator;
        private readonly ILogger<HotelServiceReservationEventHandler> _logger;


        public HotelServiceReservationEventHandler(IMediator mediator, ILogger<HotelServiceReservationEventHandler> logger)
        {
            _mediator = mediator;
            _logger = logger;
        }

        public async Task Handle(CreateReservationEvent @event)
        {
            _logger.LogInformation($"Handled CreateReservationEvent for {@event.StartDate} -> {@event.EndDate} : {@event.Room} room");

            var resonse = await _mediator.Send(new GetAvailableHotelBoyQuery(DateOnly.FromDateTime(@event.StartDate), @event.Room));
            if (resonse is null)
            {
                return;
            }
            var hotelBoy = resonse[0];

            await _mediator.Send(new CreateHotelServiceScheduleCommand(DateOnly.FromDateTime(@event.StartDate), hotelBoy.Id, @event.Room));
            return;
        }
    }
}
