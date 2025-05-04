using Hotel.Common.Domain.Bus;
using Hotel.Infra.Bus;
using MediatR;
using MicroLaundry.Domain.Commands;
using MicroLaundry.Domain.DbEntities;
using MicroLaundry.Domain.DTO;
using MicroLaundry.Domain.Events;
using MicroLaundry.Domain.Queries;
using MicroLaundry.Interface.CommandsHandler;
using MicroLaundry.Interface.EventHandlers;
using MicroLaundry.Interface.QueryHandlers;
using MicroLaundry.Interface.Repository;
using Serilog;

Log.Logger = new LoggerConfiguration()
    .WriteTo.Console()
    .WriteTo.File("../Logs/logs-laundry-.txt", rollingInterval: RollingInterval.Day)
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

builder.Services.AddSingleton<SupabaseService<Laundry>>();
builder.Services.AddScoped<LaundryRepository>();
//builder.Services.AddScoped(typeof(Repository<>));


builder.Services.AddSingleton<IEventBus, RabbitMQBus>();

builder.Services.AddTransient<IRequestHandler<CreateLaundryCommand, bool>, CreateLaundryCommandHandler>();
builder.Services.AddTransient<IRequestHandler<GetLaundryQuery, List<LaundryDTO>>, GetLaundryQueryHandler>();


builder.Services.AddTransient<CreateCleaningEventHandler>();

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var eventBus = scope.ServiceProvider.GetRequiredService<IEventBus>();

    await eventBus.Subscribe<CreateCleaningEvent, CreateCleaningEventHandler>();
}

app.Run();

