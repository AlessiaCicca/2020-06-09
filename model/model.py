import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo=nx.Graph()
        self._idMap = {}
        self._idMapNome = {}
        self.dict={}
        self.nodi=[]
        self._solBest = []
        self._costBest = 0
        self.pesoo=0



    def creaGrafo(self,anno):
        self.nodi = DAO.getNodi(anno)
        self.grafo.add_nodes_from(self.nodi)
        for v in self.nodi:
            self._idMap[v.id] = v
        for v in self.nodi:
            self._idMapNome[f"{v.id} - {v.first_name} {v.last_name}"] = v
        self.addEdges(anno)
        return self.grafo

    def addEdges(self, anno):
        self.grafo.clear_edges()
        allEdges = DAO.getConnessioni(anno)
        for connessione in allEdges:
            nodo1 = self._idMap[connessione.id1]
            nodo2 = self._idMap[connessione.id2]
            if nodo1 in self.grafo.nodes and nodo2 in self.grafo.nodes:
                if self.grafo.has_edge(nodo1, nodo2) == False:
                    self.grafo.add_edge(nodo1, nodo2, weight=connessione.peso)



    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)
    def getAdiacenti(self,nomeDirettore):
        dizio={}
        direttore=self._idMapNome[nomeDirettore]
        for nodo in self.grafo.neighbors(direttore):
            dizio[nodo]=self.grafo[nodo][direttore]["weight"]
        dizioOrder=dict(sorted(dizio.items(), key=lambda item: item[1], reverse=True))
        return dizioOrder

    def getBestPaht(self,v0Nome,sogliaCondivisi):
        v0 = self._idMapNome[v0Nome]
        parziale = [v0]
        for v in self.grafo.neighbors(v0):
                parziale.append(v)
                self.ricorsione(parziale,sogliaCondivisi)
                parziale.pop()


    def ricorsione(self, parziale,sogliaCondivisi):
        # Controllo se parziale è una sol valida, ed in caso se è migliore del best

        if len(parziale) > self._costBest and self.peso(parziale,sogliaCondivisi):
            self._costBest = len(parziale)
            self.pesoo=self.calcolopeso(parziale,sogliaCondivisi)
            self._solBest = copy.deepcopy(parziale)
            return

        for v in self.grafo.neighbors(parziale[-1]):
            if v not in parziale:
                parziale.append(v)
                if self.peso(parziale, sogliaCondivisi):
                    self.ricorsione(parziale,sogliaCondivisi)
                    parziale.pop()

    def peso(self,listObject,soglia):
        somma=0
        for nodo1 in listObject:
            for nodo2 in listObject:
                if self.grafo.has_edge(nodo1,nodo2):
                    somma+=self.grafo[nodo1][nodo2]["weight"]
        if somma<=soglia:
            return True
        else:
            return False
    def calcolopeso(self,listObject,soglia):
        somma=0
        for nodo1 in listObject:
            for nodo2 in listObject:
                if self.grafo.has_edge(nodo1,nodo2):
                    somma+=self.grafo[nodo1][nodo2]["weight"]
        return somma
