using MediatR;
using MicroHotelService.Domain.DTO;
using MicroHotelService.Domain.Queries;
using MicroHotelService.Domain.DbEntities;
using MicroHotelService.Interface.Repository;
using Microsoft.Extensions.Logging;

namespace MicroHotelService.Interface.QueryHandlers
{
    public class GetAvailableHotelBoyQueryHandler : IRequestHandler<GetAvailableHotelBoyQuery, List<HotelBoyDTO>>
    {
        private readonly HotelServiceRepository _hotelServiceRepository;
        private readonly ILogger<GetAvailableHotelBoyQueryHandler> _logger;

        public GetAvailableHotelBoyQueryHandler(HotelServiceRepository hotelServiceRepository, ILogger<GetAvailableHotelBoyQueryHandler> logger)
        {
            _hotelServiceRepository = hotelServiceRepository;
            _logger = logger;
        }

        public async Task<List<HotelBoyDTO>> Handle(GetAvailableHotelBoyQuery request, CancellationToken cancellationToken)
        {
            _logger.LogInformation($"Requested GetAvailableHotelBoy for date: {request.Date} for room: {request.Room}");

            var client = _hotelServiceRepository.Query();

            var startDateString = request.Date.ToString("yyyy-MM-dd");

            var hotelBoysResponse = await client
                .From<HotelServiceSchedule>()
                .Filter("date", Supabase.Postgrest.Constants.Operator.Equals, startDateString)
                .Get();

            var busyHotelBoys = hotelBoysResponse.Models
                .Select(r => r.HotelBoy)
                .Distinct()
                .ToList();

            var allHotelBoysIds = Enumerable.Range(1, 101);
            var avaliableHotelBoys = allHotelBoysIds
                .Where(id => !busyHotelBoys.Contains(id))
                .Select(id => new HotelBoyDTO(id))
                .ToList();
            if (avaliableHotelBoys.Count() == 0) {
                Random random = new Random();
                int randomIndex = random.Next(0, 101);
                return new List<HotelBoyDTO> { new HotelBoyDTO(randomIndex) };
            }

            return avaliableHotelBoys;

        }

    }
}
