
using Hotel.Common.Domain.Bus;
using Hotel.Infra.Bus;
using MediatR;
using MicroCuisine.Domain.Commands;
using MicroCuisine.Domain.DbEntities;
using MicroCuisine.Domain.DTO;
using MicroCuisine.Domain.Events;
using MicroCuisine.Domain.Queries;
using MicroCuisine.Interface.CommandsHandler;
using MicroCuisine.Interface.EventHandlers;
using MicroCuisine.Interface.QueryHandlers;
using MicroCuisine.Interface.Repository;

using Serilog;

Log.Logger = new LoggerConfiguration()
    .WriteTo.Console()
    .WriteTo.File("../Logs/logs-cuisine-.txt", rollingInterval: RollingInterval.Day)
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

builder.Services.AddSingleton<SupabaseService<CuisineSchedule>>();
builder.Services.AddScoped<CuisineRepository>();
//builder.Services.AddScoped(typeof(Repository<>));

builder.Services.AddSingleton<IEventBus, RabbitMQBus>();


builder.Services.AddTransient<IRequestHandler<CreateCuisineScheduleCommand, bool>, CreateCuisineScheduleCommandHandler>();
builder.Services.AddTransient<IRequestHandler<GetCuisineScheduleQuery, List<CuisineScheduleDTO>>, GetCuisineScheduleQueryHandler>();
builder.Services.AddTransient<CreateReservationEventHandler>();

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var eventBus = scope.ServiceProvider.GetRequiredService<IEventBus>();

    await eventBus.Subscribe<CreateReservationEvent, CreateReservationEventHandler>();
}

app.Run();

