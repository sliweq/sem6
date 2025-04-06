using app5;

RunPublisher.Main(args);
RunPublisher.Main(args);
RunPublisher.Main(args);


var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello World!");

app.Run();
