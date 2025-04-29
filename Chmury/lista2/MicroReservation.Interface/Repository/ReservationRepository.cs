using Hotel.Infra.Bus;
using MicroReservation.Domain.DbEntities;
using Microsoft.Extensions.Logging;

namespace MicroReservation.Interface.Repository
{
    public class ReservationRepository : Repository<Reservation>
    {
        public ReservationRepository(SupabaseService<Reservation> supabaseService, ILogger<Repository<Reservation>> logger) : base(supabaseService, logger)
        {
        }
    }  
}
