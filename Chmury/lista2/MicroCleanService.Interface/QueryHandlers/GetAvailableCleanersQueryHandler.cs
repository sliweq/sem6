using MediatR;
using MicroCleanService.Domain.DbEntities;
using MicroCleanService.Domain.DTO;
using MicroCleanService.Domain.Queries;
using MicroCleanService.Interface.Repository;
using Microsoft.Extensions.Logging;

namespace MicroCleanService.Interface.QueryHandlers
{
    public class GetAvailableCleanersQueryHandler : IRequestHandler<GetAvailableCleanersQuery, List<CleanerDTO>>
    {
        private readonly CleaningSchedulesRepository _cleaningSchedulesRepository;
        private readonly ILogger<GetAvailableCleanersQueryHandler> _logger;


        public GetAvailableCleanersQueryHandler(CleaningSchedulesRepository cleaningSchedulesRepository, ILogger<GetAvailableCleanersQueryHandler> logger)
        {
            _cleaningSchedulesRepository = cleaningSchedulesRepository;
            _logger = logger;
        }
        public async Task<List<CleanerDTO>> Handle(GetAvailableCleanersQuery request, CancellationToken cancellationToken)
        {
            _logger.LogInformation($"Requested GetAvailableCleanersQuery for date: {request.Date} for room: {request.Room}");

            var client = _cleaningSchedulesRepository.Query();
            
            var startDateString = request.Date.ToString("yyyy-MM-dd");

            var hotelBoysResponse = await client
            .From<CleaningSchedule>()
            .Filter("date", Supabase.Postgrest.Constants.Operator.Equals, startDateString)
            .Filter("date", Supabase.Postgrest.Constants.Operator.Equals, startDateString)
            .Get();

            return new List<CleanerDTO>();
        }
    }
}
