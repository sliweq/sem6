using Hotel.Common.Domain.Bus;
using Hotel.Infra.Bus;
using MediatR;
using MicroHotelService.Domain.Commands;
using MicroHotelService.Domain.DbEntities;
using MicroHotelService.Domain.DTO;
using MicroHotelService.Domain.Events;
using MicroHotelService.Domain.Queries;
using MicroHotelService.Interface.CommandsHandler;
using MicroHotelService.Interface.EventHandlers;
using MicroHotelService.Interface.QueryHandlers;
using MicroHotelService.Interface.Repository;


using Serilog;

Log.Logger = new LoggerConfiguration()
    .WriteTo.Console()
    .WriteTo.File("../Logs/logs-hotelservice-.txt", rollingInterval: RollingInterval.Day)
    .CreateLogger();

Log.Information("Starting api reservation");
var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog();

IConfigurationBuilder confBuilder = new ConfigurationBuilder()
    .SetBasePath(Path.Combine(Directory.GetCurrentDirectory(), ".."))
    .AddJsonFile("appsettings.json", false, true);

IConfigurationRoot root = confBuilder.Build();

builder.Services.AddSingleton<IConfiguration>(root);


builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(typeof(Program).Assembly));


builder.Services.AddSingleton<SupabaseService<HotelServiceSchedule>>();
builder.Services.AddScoped<HotelServiceRepository>();
//builder.Services.AddScoped(typeof(Repository<>));


builder.Services.AddSingleton<IEventBus, RabbitMQBus>();

builder.Services.AddTransient<IRequestHandler<CreateHotelServiceScheduleCommand, bool>, CreateHotelServiceScheduleCommandHandler>();
builder.Services.AddTransient<IRequestHandler<GetAvailableHotelBoyQuery, List<HotelBoyDTO>>, GetAvailableHotelBoyQueryHandler>();
builder.Services.AddTransient<CreateReservationEventHandler>();

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var eventBus = scope.ServiceProvider.GetRequiredService<IEventBus>();

    await eventBus.Subscribe<CreateReservationEvent, CreateReservationEventHandler>();
}

app.Run();

