using Hotel.Common.Domain.Bus;
using MediatR;
using MicroReservation.Domain.Commands;
using MicroReservation.Domain.Events;
using MicroReservation.Interface.Repository;
using MicroReservation.Domain.DbEntities;
using MicroReservation.Interface.QueryHandlers;
using Microsoft.Extensions.Logging;

namespace MicroReservation.Interface.CommandsHandler
{
    public class CreateReservationCommandHandler : IRequestHandler<CreateReservationCommand, bool>
    {
        private readonly IEventBus _eventBus;
        private readonly ReservationRepository _reservationRepository;
        private readonly ILogger<CreateReservationCommandHandler> _logger;

        public CreateReservationCommandHandler(ReservationRepository reservationRepository, IEventBus eventBus, ILogger<CreateReservationCommandHandler> logger)
        {
            _reservationRepository = reservationRepository;
            _eventBus = eventBus;
            _logger = logger;
        }

        public async Task<bool> Handle(CreateReservationCommand request, CancellationToken cancellationToken)
        {
            _logger.LogInformation($"Requested CreateReservationCommand for {request.UserName} {request.StartDate} {request.EndDate} {request.NumberOfPeople}");
            var reservation = new Reservation(
                request.UserName,
                DateOnly.FromDateTime(request.StartDate),
                DateOnly.FromDateTime(request.EndDate),
                request.NumberOfPeople,
                request.Room
                );

            await _reservationRepository.InsertAsync(new List<Reservation>() { reservation });

            await _eventBus.Publish(new CreateReservationEvent(
                reservation.Id,
                reservation.Room,
                reservation.NumberOfPeople,
                reservation.StartDate.ToDateTime(TimeOnly.Parse("10:00 PM")),
                reservation.EndDate.ToDateTime(TimeOnly.Parse("10:00 PM")))
                );

            return true;
        }
    }
}
