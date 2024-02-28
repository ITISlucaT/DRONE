import provaFrame as pf
import os
# Verifica se il file esiste
if os.path.exists("circle_dimensions.txt"):
    # Rimuovi il file
    os.remove("circle_dimensions.txt")
pf.run()