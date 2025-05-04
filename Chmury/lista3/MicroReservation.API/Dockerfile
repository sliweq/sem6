FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

EXPOSE 80

COPY MicroReservation.API/MicroReservation.API.csproj MicroReservation.API/
COPY MicroReservation.Domain/MicroReservation.Domain.csproj MicroReservation.Domain/
COPY MicroReservation.Interface/MicroReservation.Interface.csproj MicroReservation.Interface/
COPY Hotel.Infra.Bus/Hotel.Infra.Bus.csproj Hotel.Infra.Bus/
COPY Hotel.Common.Domain/Hotel.Common.Domain.csproj Hotel.Common.Domain/

RUN dotnet restore ./MicroReservation.API/MicroReservation.API.csproj

COPY . .

WORKDIR /src/MicroReservation.API
RUN dotnet publish -c Release -o /app/publish

# Finalny obraz runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "MicroReservation.API.dll"]