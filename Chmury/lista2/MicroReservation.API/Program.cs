//var builder = WebApplication.CreateBuilder(args);
//var app = builder.Build();

//app.MapGet("/", () => "Hello World!");

//app.Run();
using Hotel.Common.Domain.Bus;
using Hotel.Infra.Bus;
using MediatR;
using MicroReservation.Domain.Commands;
using MicroReservation.Domain.DTO;
using MicroReservation.Domain.Queries;
using MicroReservation.Interface.QueryHandlers;
using MicroReservation.Interface.Repository;
using MicroReservation.Interface.CommandsHandler;
using MicroReservation.Domain.DbEntities;
using Serilog;

Log.Logger = new LoggerConfiguration()
    .WriteTo.Console()
    .WriteTo.File("../Logs/logs-reservations-.txt", rollingInterval: RollingInterval.Day)
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

builder.Services.AddControllers();

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddSingleton<SupabaseService<Reservation>>();
builder.Services.AddScoped<ReservationRepository>();
//builder.Services.AddScoped(typeof(Repository<>));


builder.Services.AddSingleton<IEventBus, RabbitMQBus>();



builder.Services.AddTransient<IRequestHandler<CreateReservationCommand, bool>, CreateReservationCommandHandler>();

builder.Services.AddTransient<IRequestHandler<GetEmptyRoomsQuery, List<RoomDTO>>, GetEmptyRoomsQueryHandler>();
builder.Services.AddTransient<IRequestHandler<GetReservationQuery, ReservationDTO>, GetReservationQueryHandler>();

var app = builder.Build();

//Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
