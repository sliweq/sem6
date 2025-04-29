using MediatR;
using MicroLaundry.Domain.DbEntities;
using MicroLaundry.Domain.DTO;
using MicroLaundry.Domain.Queries;
using MicroLaundry.Interface.Repository;
using Microsoft.Extensions.Logging;


namespace MicroLaundry.Interface.QueryHandlers
{
    public class GetLaundryQueryHandler : IRequestHandler<GetLaundryQuery, List<LaundryDTO>>
    {
        private readonly LaundryRepository _laundryRepository;
        private readonly ILogger<GetLaundryQueryHandler> _logger;

        public GetLaundryQueryHandler(LaundryRepository laundryRepository, ILogger<GetLaundryQueryHandler> logger)
        {
            _laundryRepository = laundryRepository;
            _logger = logger;
        }

        public async Task<List<LaundryDTO>> Handle(GetLaundryQuery request, CancellationToken cancellationToken)
        {
            _logger.LogInformation($"Requested GetLaundryQuery for dates: {request.StartDate} -> {request.EndDate}");
            var client = _laundryRepository.Query();

            var startDateString = request.StartDate.ToString("yyyy-MM-dd");
            var endDateString = request.EndDate.ToString("yyyy-MM-dd");

            var laundryResponse = await client
                .From<Laundry>()
                .Filter("date", Supabase.Postgrest.Constants.Operator.GreaterThanOrEqual, startDateString)
                .Filter("date", Supabase.Postgrest.Constants.Operator.LessThanOrEqual, endDateString)
                .Get();

            var tmp = laundryResponse.Models
                .Select(room => new LaundryDTO(room.Id,room.Date,room.SheetsCount)).ToList();

            return tmp;
        }
    }

}
