using Hotel.Infra.Bus;
using MicroHotelService.Domain.DbEntities;
using Microsoft.Extensions.Logging;


namespace MicroHotelService.Interface.Repository
{
    public class HotelServiceRepository : Repository<HotelServiceSchedule>
    
    {
        public HotelServiceRepository(SupabaseService<HotelServiceSchedule> supabaseService, ILogger<Repository<HotelServiceSchedule>> logger) : base(supabaseService, logger)
        {
        }
    }


}
