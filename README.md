# Naše Duolingo liga

Pět hráčů, společný web a experimentální automatické měření XP každých 15 minut.

## Zveřejnění přes GitHub Pages

1. Na github.com vytvoř nový **veřejný** repozitář `duolingo-liga`.
2. Nahraj **obsah této složky**, včetně skryté složky `.github` (nejjednodušší je rozbalit ZIP a použít GitHub Desktop nebo git). Při nahrávání přes web zkontroluj, že `.github/workflows/update.yml` skutečně existuje.
3. V repozitáři otevři **Settings → Actions → General → Workflow permissions** a nastav **Read and write permissions**.
4. V **Actions → Aktualizovat XP → Run workflow** spusť první měření ručně. Zkontroluj jeho log. Pokud Duolingo blokuje přístup, workflow skončí chybou a automatický žebříček nebude fungovat.
5. V **Settings → Pages → Build and deployment** zvol **Deploy from a branch**, `main`, `/ (root)` a ulož.
6. Odkaz na web bude `https://TVUJ-GITHUB-UCET.github.io/duolingo-liga/`.

GitHub Actions se pokusí o aktualizaci každých 15 minut. GitHub nezaručuje přesný čas; plánované běhy mohou být opožděné nebo vynechané. U veřejných repozitářů mohou být plánované běhy po delší neaktivitě pozastavené.

## Jak se počítají XP

Při každém měření se ukládá `totalXp` veřejného profilu. Týdenní XP jsou rozdíl posledního a prvního měření v aktuálním týdnu podle času Praha. Po prvním měření ještě není možné spočítat přírůstek. Výsledky se nezačnou dopočítávat zpětně; první týden může být neúplný. Měření nejsou přímo oficiální týdenní XP z Duolinga.

## Upozornění

Použité rozhraní Duolinga je neoficiální a může být zablokováno. Duolingo v podmínkách omezuje automatizované získávání dat; před spuštěním si ověřte, že použití odpovídá aktuálním podmínkám a že všichni hráči souhlasí se zveřejněním jmen a výsledků. Do projektu nikdy nevkládejte hesla ani přihlašovací tokeny.

Profily se upravují v `players.json`. Snímky se ukládají v `data/history.json` a jsou ve veřejném repozitáři viditelné.
