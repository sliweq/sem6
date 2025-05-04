FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

COPY MicroCleanService.API/MicroCleanService.API.csproj MicroCleanService.API/
COPY MicroCleanService.Domain/MicroCleanService.Domain.csproj MicroCleanService.Domain/
COPY MicroCleanService.Interface/MicroCleanService.Interface.csproj MicroCleanService.Interface/
COPY Hotel.Infra.Bus/Hotel.Infra.Bus.csproj Hotel.Infra.Bus/
COPY Hotel.Common.Domain/Hotel.Common.Domain.csproj Hotel.Common.Domain/


RUN dotnet restore ./MicroCleanService.API/MicroCleanService.API.csproj

COPY . .

WORKDIR /src/MicroCleanService.API
RUN dotnet publish -c Release -o /app/publish

# Finalny obraz runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "MicroCleanService.API.dll"]
