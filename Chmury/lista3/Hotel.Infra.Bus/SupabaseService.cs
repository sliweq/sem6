using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Supabase;
using Supabase.Postgrest.Models;


namespace Hotel.Infra.Bus
{
    public class SupabaseService<T> where T : BaseModel, new()
    {
        private readonly Client _client;
        private readonly ILogger<SupabaseService<T>> _logger;


        public SupabaseService(IConfiguration configRoot, ILogger<SupabaseService<T>> logger)
        {
            _logger = logger;

            //IConfiguration configuration
            var url = configRoot["AmqpSettings:SUPABASE_URL"];
            var key = configRoot["AmqpSettings:SUPABASE_KEY"];

            //var url = Environment.GetEnvironmentVariable("SUPABASE_URL");
            //var key = Environment.GetEnvironmentVariable("SUPABASE_KEY");
            _client = new Client(url, key);
        }

        public async Task InitializeAsync()
        {
            await _client.InitializeAsync();
        }
        public Client GetClient()
        {
            return _client;
        }
    }
}
