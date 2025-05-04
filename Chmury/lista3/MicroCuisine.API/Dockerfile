FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

COPY MicroCuisine.API/MicroCuisine.API.csproj MicroCuisine.API/
COPY MicroCuisine.Domain/MicroCuisine.Domain.csproj MicroCuisine.Domain/
COPY MicroCuisine.Interface/MicroCuisine.Interface.csproj MicroCuisine.Interface/
COPY Hotel.Infra.Bus/Hotel.Infra.Bus.csproj Hotel.Infra.Bus/
COPY Hotel.Common.Domain/Hotel.Common.Domain.csproj Hotel.Common.Domain/

RUN dotnet restore ./MicroCuisine.API/MicroCuisine.API.csproj

COPY . .

WORKDIR /src/MicroCuisine.API
RUN dotnet publish -c Release -o /app/publish

# Finalny obraz runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "MicroCuisine.API.dll"]
