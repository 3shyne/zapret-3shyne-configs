@echo off
chcp 65001 > nul
:: 65001 - UTF-8

cd /d "%~dp0"
call service.bat status_zapret
call service.bat check_updates
call service.bat load_game_filter
echo:

setlocal

set "BIN=%~dp0bin\"
set "LISTS=%~dp0lists\"
cd /d "%BIN%"

start "zapret: %~n0" /min "%BIN%winws.exe" ^
  --wf-tcp=80,443,2053,2083,2087,2096,8443,88,5222,5223,5228,%GameFilter% ^
  --wf-udp=443,19294-19344,50000-50100,1400,3478,596-599,4000-65535,%GameFilter% ^
  --filter-udp=443 ^
  --hostlist="%LISTS%list-general.txt" ^
  --hostlist-exclude="%LISTS%list-exclude.txt" ^
  --ipset-exclude="%LISTS%ipset-exclude.txt" ^
  --dpi-desync=fake ^
  --dpi-desync-repeats=11 ^
  --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" ^
  --new ^
  --filter-udp=19294-19344,50000-50100 ^
  --filter-l7=discord,stun ^
  --dpi-desync=fake ^
  --dpi-desync-repeats=6 ^
  --new ^
  --filter-tcp=2053,2083,2087,2096,8443 ^
  --hostlist-domains=discord.media ^
  --dpi-desync=fake,multisplit ^
  --dpi-desync-split-seqovl=681 ^
  --dpi-desync-split-pos=1 ^
  --dpi-desync-fooling=ts ^
  --dpi-desync-repeats=8 ^
  --dpi-desync-split-seqovl-pattern="%BIN%tls_3shyne_google_o.bin" ^
  --dpi-desync-fake-tls="%BIN%tls_3shyne_google_o.bin" ^
  --new ^
  --filter-tcp=443 ^
  --hostlist="%LISTS%list-google.txt" ^
  --ip-id=zero ^
  --dpi-desync=fake,multisplit ^
  --dpi-desync-split-seqovl=681 ^
  --dpi-desync-split-pos=1 ^
  --dpi-desync-fooling=ts ^
  --dpi-desync-repeats=8 ^
  --dpi-desync-split-seqovl-pattern="%BIN%tls_3shyne_google_o.bin" ^
  --dpi-desync-fake-tls="%BIN%tls_3shyne_google_o.bin" ^
  --new ^
  --filter-tcp=80,443 ^
  --hostlist="%LISTS%list-general.txt" ^
  --hostlist-exclude="%LISTS%list-exclude.txt" ^
  --ipset-exclude="%LISTS%ipset-exclude.txt" ^
  --dpi-desync=fake,multisplit ^
  --dpi-desync-split-seqovl=664 ^
  --dpi-desync-split-pos=1 ^
  --dpi-desync-fooling=ts ^
  --dpi-desync-repeats=8 ^
  --dpi-desync-split-seqovl-pattern="%BIN%tls_3shyne_max_v1.bin" ^
  --dpi-desync-fake-tls="%BIN%tls_3shyne_max_v1.bin" ^
  --new ^
  --filter-udp=443 ^
  --ipset="%LISTS%ipset-all.txt" ^
  --hostlist-exclude="%LISTS%list-exclude.txt" ^
  --ipset-exclude="%LISTS%ipset-exclude.txt" ^
  --dpi-desync=fake ^
  --dpi-desync-repeats=11 ^
  --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" ^
  --new ^
  --filter-tcp=80,443,%GameFilter% ^
  --ipset="%LISTS%ipset-all.txt" ^
  --hostlist-exclude="%LISTS%list-exclude.txt" ^
  --ipset-exclude="%LISTS%ipset-exclude.txt" ^
  --dpi-desync=fake,multisplit ^
  --dpi-desync-split-seqovl=664 ^
  --dpi-desync-split-pos=1 ^
  --dpi-desync-fooling=ts ^
  --dpi-desync-repeats=8 ^
  --dpi-desync-split-seqovl-pattern="%BIN%tls_3shyne_max_v1.bin" ^
  --dpi-desync-fake-tls="%BIN%tls_3shyne_max_v1.bin" ^
  --new ^
  --filter-udp=%GameFilter% ^
  --ipset="%LISTS%ipset-all.txt" ^
  --ipset-exclude="%LISTS%ipset-exclude.txt" ^
  --dpi-desync=fake ^
  --dpi-desync-repeats=10 ^
  --dpi-desync-any-protocol=1 ^
  --dpi-desync-fake-unknown-udp="%BIN%quic_initial_www_google_com.bin" ^
  --dpi-desync-cutoff=n4 ^
  --comment TELEGRAM SECTION ^
  --new ^
  --filter-tcp=80,443,88,5222,5223,5228,8443 ^
  --ipset="%LISTS%ipset-telegram.txt" ^
  --ipset-exclude="%LISTS%ipset-exclude.txt" ^
  --dpi-desync=fake,multisplit ^
  --dpi-desync-split-seqovl=681 ^
  --dpi-desync-split-pos=1 ^
  --dpi-desync-fooling=ts ^
  --dpi-desync-repeats=6 ^
  --dpi-desync-autottl=2 ^
  --dpi-desync-split-seqovl-pattern="%BIN%tls_3shine_ozon_v1.bin" ^
  --dpi-desync-fake-tls="%BIN%tls_3shine_ozon_v1.bin" ^
  --new ^
  --filter-udp=1400,3478 ^
  --ipset="%LISTS%ipset-telegram.txt" ^
  --ipset-exclude="%LISTS%ipset-exclude.txt" ^
  --filter-l7=stun ^
  --dpi-desync=fake ^
  --dpi-desync-repeats=6 ^
  --dpi-desync-autottl=2 ^
  --new ^
  --filter-udp=596-599,1400,3478,4000-65535 ^
  --ipset="%LISTS%ipset-telegram.txt" ^
  --ipset-exclude="%LISTS%ipset-exclude.txt" ^
  --dpi-desync=fake ^
  --dpi-desync-repeats=6 ^
  --dpi-desync-autottl=2 ^
  --dpi-desync-any-protocol=1 ^
  --dpi-desync-fake-unknown-udp="%BIN%quic_initial_vk_com.bin" ^
  --dpi-desync-cutoff=n4

endlocal
