# Retoma a tradução automática PT-BR -> EN do portal (página inicial, explorador e livro).
# É retomável: o cache (i18n_portal_cache.json) guarda o que já foi traduzido.
# Requisitos: venv de tradução em D:\Claude\_toolchain\mt-venv (argostranslate + beautifulsoup4) e PC com memória livre
# (feche outros programas; as bibliotecas podem levar alguns minutos para carregar).
$r = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$p = "D:\Claude\_toolchain\mt-venv\Scripts\python.exe"
$env:PYTHONUTF8 = "1"
& $p -u "$r\source\portal\i18n_portal.py" "D:\Claude\Judo_BJJ\pipelines" "D:\Claude\Judo_BJJ\webapp\data.js" landing explorar livro *> "$r\source\portal\i18n_portal.log"
"Fim. Veja source\portal\i18n_portal.log; depois rode montar_portal.py não é necessário: os dicionários ficam em site\assets\i18n-*.js."
