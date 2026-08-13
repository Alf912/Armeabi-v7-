"""Ninja Android ARMv7 - relationship indexer."""

class SesIndexer:
    def __init__(self):
        self.grafo_relaciones = {}
        self.errores_detectados = []

    def registrar_documento(self, id_documento, dependencias_citadas):
        id_limpia = id_documento.upper().strip()
        deps_limpias = [str(dep).upper().strip() for dep in dependencias_citadas]
        self.grafo_relaciones[id_limpia] = deps_limpias

    def escanear_bucles_circulares(self):
        self.errores_detectados = []
        estados = {nodo: 0 for nodo in self.grafo_relaciones}
        for nodo_raiz in self.grafo_relaciones:
            if estados[nodo_raiz] != 0:
                continue
            pila = [nodo_raiz]
            while pila:
                actual = pila[-1]
                if estados[actual] == 0:
                    estados[actual] = 1
                    for vecino in self.grafo_relaciones.get(actual, []):
                        if vecino not in estados:
                            continue
                        if estados[vecino] == 1:
                            self.errores_detectados.append(f"BUCLE_CIRCULAR: {actual} -> {vecino}")
                            return False
                        if estados[vecino] == 0:
                            pila.append(vecino)
                elif estados[actual] == 1:
                    estados[actual] = 2
                    pila.pop()
                else:
                    pila.pop()
        return True
