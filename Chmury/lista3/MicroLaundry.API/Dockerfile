FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

COPY MicroLaundry.API/MicroLaundry.API.csproj MicroLaundry.API/
COPY MicroLaundry.Domain/MicroLaundry.Domain.csproj MicroLaundry.Domain/
COPY MicroLaundry.Interface/MicroLaundry.Interface.csproj MicroLaundry.Interface/
COPY Hotel.Infra.Bus/Hotel.Infra.Bus.csproj Hotel.Infra.Bus/
COPY Hotel.Common.Domain/Hotel.Common.Domain.csproj Hotel.Common.Domain/

RUN dotnet restore ./MicroLaundry.API/MicroLaundry.API.csproj

COPY . .

WORKDIR /src/MicroLaundry.API
RUN dotnet publish -c Release -o /app/publish

# Finalny obraz runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "MicroLaundry.API.dll"]
