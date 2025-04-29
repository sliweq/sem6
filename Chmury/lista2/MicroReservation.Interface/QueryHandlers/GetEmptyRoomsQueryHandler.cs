using MediatR;
using MicroReservation.Domain.DTO;
using MicroReservation.Domain.Queries;
using MicroReservation.Domain.DbEntities;
using MicroReservation.Interface.Repository;
using Microsoft.Extensions.Logging;

namespace MicroReservation.Interface.QueryHandlers
{
    public class GetEmptyRoomsQueryHandler : IRequestHandler<GetEmptyRoomsQuery, List<RoomDTO>>
    {
        private readonly ReservationRepository _reservationRepository;
        private readonly ILogger<GetEmptyRoomsQueryHandler> _logger;

        public GetEmptyRoomsQueryHandler(ReservationRepository reservationRepository, ILogger<GetEmptyRoomsQueryHandler> logger)
        {
            _reservationRepository = reservationRepository;
            _logger = logger;
        }

        public async Task<List<RoomDTO>> Handle(GetEmptyRoomsQuery request, CancellationToken cancellationToken)
        {
            _logger.LogInformation($"Requested GetEmptyRoomsQuery for {request.StartTime} {request.EndTime}");
            var client = _reservationRepository.Query();

            var reservationsResponse = await client
                .From<Reservation>()
                .Filter("startDate", Supabase.Postgrest.Constants.Operator.LessThan, request.EndTime)
                .Filter("endDate", Supabase.Postgrest.Constants.Operator.GreaterThan, request.StartTime)
                .Get();

            var occupiedRoomIds = reservationsResponse.Models
                .Select(r => r.Room)
                .Distinct()
                .ToList();

            var allRoomIds = Enumerable.Range(1, 2001);

            var availableRooms = allRoomIds
                .Where(id => !occupiedRoomIds.Contains(id))
                .Select(id => new
                {
                    Id = id,
                    MaxCapacity = CalculateRoomCapacity(id)
                })
                .Where(room => room.MaxCapacity >= request.AmountOfPeople)
                .OrderBy(room => room.MaxCapacity)
                .ThenBy(room => room.Id)
                .Select(room => new RoomDTO(room.Id, room.MaxCapacity))
                .ToList();

            return availableRooms;
        }
        private int CalculateRoomCapacity(int roomId)
        {
            var mod = roomId % 10;
            return mod switch
            {
                5 => 5,
                4 => 4,
                3 or 6 => 3,
                _ => 2
            };
        }
    }
}
