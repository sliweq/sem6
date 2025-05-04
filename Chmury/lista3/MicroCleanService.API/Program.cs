using Hotel.Common.Domain.Bus;
using Hotel.Infra.Bus;
using MediatR;
using MicroCleanService.Domain.Commands;
using MicroCleanService.Domain.DbEntities;
using MicroCleanService.Domain.Events;
using MicroCleanService.Interface.CommandsHandler;
using MicroCleanService.Interface.Repository;
using MicroCleanService.Interface.EventHandlers;
using Serilog;

Log.Logger = new LoggerConfiguration()
    .WriteTo.Console()
    .WriteTo.File("../Logs/logs-cleanservice-.txt", rollingInterval: RollingInterval.Day)
    .CreateLogger();

Log.Information("Starting api reservation");
var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog();

IConfigurationBuilder confBuilder = new ConfigurationBuilder()
    .AddEnvironmentVariables();
    // .SetBasePath(Path.Combine(Directory.GetCurrentDirectory(), ".."))
    // .AddJsonFile("appsettings.json", false, true)

IConfigurationRoot root = confBuilder.Build();

builder.Services.AddSingleton<IConfiguration>(root);


builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(typeof(Program).Assembly));

builder.Services.AddSingleton<SupabaseService<CleaningSchedule>>();
builder.Services.AddScoped<CleaningSchedulesRepository>();
//builder.Services.AddScoped(typeof(Repository<>));

builder.Services.AddSingleton<IEventBus, RabbitMQBus>();

builder.Services.AddTransient<IRequestHandler<CreateCleaningScheduleCommand, bool>, CreateCleaningScheduleCommandHandler>();


builder.Services.AddTransient<CreateReservationEventHandler>();

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var eventBus = scope.ServiceProvider.GetRequiredService<IEventBus>();

    await eventBus.Subscribe<CreateReservationEvent, CreateReservationEventHandler>();
}

app.Run();
