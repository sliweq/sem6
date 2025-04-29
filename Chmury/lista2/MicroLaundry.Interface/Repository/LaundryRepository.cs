using Hotel.Infra.Bus;
using MicroLaundry.Domain.DbEntities;
using Microsoft.Extensions.Logging;

namespace MicroLaundry.Interface.Repository
{
    public class LaundryRepository : Repository<Laundry>

    {
        public LaundryRepository(SupabaseService<Laundry> supabaseService, ILogger<Repository<Laundry>> logger) : base(supabaseService, logger)
        {
        }
    }
}
