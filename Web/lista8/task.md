## Lista 8 zadania 
1. Wykorzystując technologię WebSocket napisać prosty czat internetowy dostępny z poziomu przeglądarki. Można skorzystać z biblioteki Socket.IO lub napisać wszystko bezpośrednio w czystym WS. Jako dobre wprowadzenie warto zerknąć tutaj: [](https://socket.io/get-started/chat) 
2. Czat powinien posiadać poniższe funkcjonalności (im więcej tym lepiej):
    2. 1. W podstawkowej wersji jeden wspólny pokój dla wszystkich. W bardziej rozbudowanej powinien dostarczać wiele pokoi dyskusyjnych
    2. 2. Użytkownicy powinni być identyfikowani pseudonimem (nickiem). Pseudonim ustala się w momencie podłączenia się do czatu.
    2. 3. Użytkownik w dowolnym momencie może połączyć się z pokojem jak i rozłączyć. Odpowiedni komunikat powinien być wysłany do innych użytkowników pokoju.
      2. 4. Wiadomości od użytkowników powinny wyświetlać treść wiadomości oraz pseudonim i datę wysłania. Wiadomości obce wyświetlają się wyrównane do lewej strony, natomiast wiadomości nadawcy wyrównane do prawej strony. Zaproponować graficzną wizualizację wiadomości w postaci chmurek.
        2. 5. W momencie gdy dany użytkownik zaczyna pisać wiadomość to inni uczestnicy dyskusji widzą napis, że "{user} is typing...".
        2. 6. Na najwyższą ocenę wymagane jest możliwość wysyłania oprócz wiadomości tekstowej także zdjęcia.
3. Mile widziane dopisanie dodatkowych funkcjonalności nie wyszczególnionych powyżej.
