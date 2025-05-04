using Hotel.Common.Domain.Bus;
using MediatR;
using MicroHotelService.Domain.Commands;
using MicroHotelService.Domain.DbEntities;
using MicroHotelService.Interface.Repository;
using Microsoft.Extensions.Logging;

namespace MicroHotelService.Interface.CommandsHandler
{
    public class CreateHotelServiceScheduleCommandHandler : IRequestHandler<CreateHotelServiceScheduleCommand, bool>
    {
        private readonly IEventBus _eventBus;
        private readonly HotelServiceRepository _hotelServiceRepository;
        private readonly ILogger<CreateHotelServiceScheduleCommandHandler> _logger;

        public CreateHotelServiceScheduleCommandHandler(HotelServiceRepository hotelServiceRepository, IEventBus eventBus, ILogger<CreateHotelServiceScheduleCommandHandler> logger)
        {
            _logger = logger;
            _hotelServiceRepository = hotelServiceRepository;
            _eventBus = eventBus;
        }

        public async Task<bool> Handle(CreateHotelServiceScheduleCommand request, CancellationToken cancellationToken)
        {
            _logger.LogInformation($"Requested CreateHotelServiceScheduleCommand for {request.Date} room: {request.Room} hotelboy: {request.HotelBoy}");

            var hotelServiceSchedule = new HotelServiceSchedule(
                request.Date,
                request.HotelBoy,
                request.Room
            );

            await _hotelServiceRepository.InsertAsync(new List<HotelServiceSchedule>() { hotelServiceSchedule });

            // opcjonlanie publikowanie eventu o utworzeniu Schedule idk why

            return true;

        }
    }
}
