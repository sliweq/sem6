FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

COPY MicroHotelService.API/MicroHotelService.API.csproj MicroHotelService.API/
COPY MicroHotelService.Domain/MicroHotelService.Domain.csproj MicroHotelService.Domain/
COPY MicroHotelService.Interface/MicroHotelService.Interface.csproj MicroHotelService.Interface/
COPY Hotel.Infra.Bus/Hotel.Infra.Bus.csproj Hotel.Infra.Bus/
COPY Hotel.Common.Domain/Hotel.Common.Domain.csproj Hotel.Common.Domain/

RUN dotnet restore ./MicroHotelService.API/MicroHotelService.API.csproj

COPY . .

WORKDIR /src/MicroHotelService.API
RUN dotnet publish -c Release -o /app/publish

# Finalny obraz runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "MicroHotelService.API.dll"]
