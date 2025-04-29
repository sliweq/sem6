using MediatR;
using MicroReservation.Domain.DTO;
using MicroReservation.Domain.Queries;
using MicroReservation.Interface.Repository;

namespace MicroReservation.Interface.QueryHandlers
{
    public class GetReservationQueryHandler : IRequestHandler<GetReservationQuery, ReservationDTO>
    {
        private readonly ReservationRepository _dbcontext;

        public GetReservationQueryHandler(ReservationRepository dbcontext)
        {
            _dbcontext = dbcontext;
        }

        public async Task<ReservationDTO> Handle(GetReservationQuery request, CancellationToken cancellationToken)
        {
            // Lub bez async i zakomentośc coś tam
            var reservation = await _dbcontext.GetByIdAsync(request.Id);


            return new ReservationDTO(reservation.Id,reservation.UserName,
                reservation.StartDate.ToDateTime(TimeOnly.Parse("10:00 PM")),
                reservation.EndDate.ToDateTime(TimeOnly.Parse("10:00 PM")),
                reservation.NumberOfPeople, reservation.TimeOfReservation, reservation.Room);
            //return Task.FromResult(new ReservationDTO(reservation.Id, reservation.UserName, reservation.StartDate, reservation.EndDate, reservation.NumberOfPeople, reservation.TimeOfReservation));
        }
    }
}
