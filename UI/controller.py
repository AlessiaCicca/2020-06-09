import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        ann="200"
        for i in range(4,7):
            self._view.ddyear.options.append(ft.dropdown.Option(
                text=ann+str(i)))


    def handle_graph(self, e):
        grafo = self._model.creaGrafo( int(self._view.ddyear.value))
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumEdges()} archi."))
        direttori=grafo.nodes()
        for direttore in direttori:
            self._view.dddirector.options.append(ft.dropdown.Option(
                text=direttore))
        self._view.update_page()



    def handle_adiacenti(self, e):
        adiacenti=self._model.getAdiacenti(self._view.dddirector.value)
        self._view.txt_result.controls.append(ft.Text(f"REGISTI ADIACENTI A: {self._view.dddirector.value}"))
        for chiavi in adiacenti.keys():
            self._view.txt_result.controls.append(ft.Text(f"Nodo {chiavi}, #attoricondivisi={adiacenti[chiavi]}"))
        self._view.update_page()


    def handle_affini(self, e):
        self._model.getBestPaht(self._view.dddirector.value,int(self._view.txtAttoriCondivisi.value))
        print(self._model._solBest)
        sol=self._model._solBest
        cos=self._model._costBest
        pesoo=self._model.pesoo
        self._view.txt_result.controls.append(ft.Text(f"La soluzionione migliore ha lunghezza pari a {cos} e peso di {pesoo}:"))
        for nodo in sol:
            self._view.txt_result.controls.append(ft.Text(f"{nodo}"))
        self._view.update_page()